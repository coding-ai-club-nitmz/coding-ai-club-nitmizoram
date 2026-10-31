# Copyright (c) 2026 Coding & AI Club, NIT Mizoram. All Rights Reserved.
import os
import re
import time
import random
import threading
from datetime import datetime, timezone, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread

# IST Timezone for accurate Indian Standard Time in Google Sheets logs
IST = timezone(timedelta(hours=5, minutes=30))

# Global thread lock to prevent race conditions during concurrent writing within a single process
sheets_api_lock = threading.Lock()

# --- GLOBAL CACHES (Massive Speedup for Synchronous Syncs) ---
# These stay active in memory across multiple requests on the server
_gspread_client = None
_drive_service = None
_spreadsheet_cache = {}      # Maps event_name -> spreadsheet_id
_headers_initialized = set() # Set of spreadsheet_ids that already have headers checked

def get_google_clients(creds_file):
    """Initializes Google API clients once and caches them globally to save 1-2 seconds per request."""
    global _gspread_client, _drive_service
    if _gspread_client is None or _drive_service is None:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Vercel / Production Deployment Check
        client_email = os.environ.get('GOOGLE_CLIENT_EMAIL')
        private_key = os.environ.get('GOOGLE_PRIVATE_KEY')
        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        
        if client_email and private_key:
            project_id = os.environ.get('GOOGLE_PROJECT_ID')
            if not project_id and '@' in client_email:
                project_id = client_email.split('@')[1].split('.')[0]
            if not project_id:
                project_id = "website-automator"
            creds_info = {
                "type": "service_account",
                "project_id": project_id,
                "private_key": private_key.replace('\\n', '\n'),
                "client_email": client_email,
                "token_uri": "https://oauth2.googleapis.com/token"
            }
            creds = service_account.Credentials.from_service_account_info(creds_info, scopes=scopes)
        elif creds_json:
            import json
            creds_info = json.loads(creds_json)
            creds = service_account.Credentials.from_service_account_info(creds_info, scopes=scopes)
        elif creds_file and os.path.exists(creds_file):
            creds = service_account.Credentials.from_service_account_file(creds_file, scopes=scopes)
        else:
            raise FileNotFoundError("Google Credentials missing. Check GOOGLE_CLIENT_EMAIL and GOOGLE_PRIVATE_KEY in .env")
            
        _drive_service = build('drive', 'v3', credentials=creds)
        _gspread_client = gspread.authorize(creds)
    return _gspread_client, _drive_service

def sanitize_for_sheet(value):
    """
    Sanitizes values entered into the spreadsheet cells:
    1. Prevents Spreadsheet Formula Injection (CSV Injection)
    2. Prevents script/HTML injection attacks
    """
    if not value:
        return ""
    value_str = str(value).strip()
    
    # Escape leading characters to prevent Spreadsheet Formula / CSV Injection
    if value_str and value_str[0] in ('=', '+', '-', '@', '\t', '\r'):
        value_str = "'" + value_str
        
    # Strip HTML and script tags
    value_str = re.sub(r'<[^>]*>', '', value_str)
    return value_str

def sync_registration_to_folder(name, roll, email, phone, branch, degree, year, event_name, skills, ip_address=""):
    folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
    creds_file = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE')
    client_email = os.environ.get('GOOGLE_CLIENT_EMAIL')
    private_key = os.environ.get('GOOGLE_PRIVATE_KEY')
    creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    
    if not folder_id:
        return {"status": "skipped", "message": "GOOGLE_DRIVE_FOLDER_ID is not configured."}
        
    if not (client_email and private_key) and not creds_json and (not creds_file or not os.path.exists(creds_file)):
        return {"status": "skipped", "message": "Credentials not found. Please set GOOGLE_CLIENT_EMAIL and GOOGLE_PRIVATE_KEY in your .env"}

    try:
        # Sanitize all form inputs before processing
        name = sanitize_for_sheet(name)
        roll = sanitize_for_sheet(roll)
        email = sanitize_for_sheet(email)
        phone = sanitize_for_sheet(phone)
        branch = sanitize_for_sheet(branch)
        degree = sanitize_for_sheet(degree)
        year = sanitize_for_sheet(year)
        event_name = sanitize_for_sheet(event_name)
        skills = sanitize_for_sheet(skills)
        
        # Load API clients globally (instant if already loaded)
        gspread_client, drive_service = get_google_clients(creds_file)
        
        try:
            with sheets_api_lock:
                is_new = False
                spreadsheet_id = _spreadsheet_cache.get(event_name)
            
            # If not in cache, query Google Drive API (Takes ~1 second)
            if not spreadsheet_id:
                query = f"name = '{event_name}' and '{folder_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false"
                results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
                files = results.get('files', [])
                
                if files:
                    spreadsheet_id = files[0]['id']
                else:
                    # Create new spreadsheet
                    ss = gspread_client.create(event_name)
                    spreadsheet_id = ss.id
                    is_new = True
                    
                    # Move to folder and set permissions
                    file_meta = drive_service.files().get(fileId=spreadsheet_id, fields='parents').execute()
                    previous_parents = ",".join(file_meta.get('parents', []))
                    
                    drive_service.files().update(
                        fileId=spreadsheet_id, addParents=folder_id, removeParents=previous_parents, fields='id, parents'
                    ).execute()
                    
                    try:
                        permission = {'type': 'user', 'role': 'writer', 'emailAddress': 'coding.club@nitmz.ac.in'}
                        drive_service.permissions().create(fileId=spreadsheet_id, body=permission, fields='id').execute()
                    except Exception as share_err:
                        print(f"Warning: Failed to share spreadsheet with coding.club: {share_err}")
                
                # Save to cache so next registrations are instant!
                _spreadsheet_cache[event_name] = spreadsheet_id
                
            # Open spreadsheet using cached ID
            ss = gspread_client.open_by_key(spreadsheet_id)
            sheet = ss.sheet1
            
            # Prevent Duplicate Registrations (Check Roll Number in Column 4)
            try:
                existing_rolls = sheet.col_values(4) # Column D is Roll Number
                # Skip header, compare case-insensitive
                if any(roll.upper() == r.upper() for r in existing_rolls[1:]):
                    return {"status": "duplicate", "message": f"Roll number {roll} is already registered."}
            except Exception:
                pass # If sheet is empty or error fetching columns, proceed normally
                
            # Check if we need to write headers (cached to avoid slow API read calls)
            if spreadsheet_id not in _headers_initialized:
                try:
                    if not sheet.row_values(1):
                        sheet.append_row([
                            "Timestamp", "IP Address", "Full Name", "Roll Number", 
                            "Email Address", "Phone Number", "Branch/Department", 
                            "Degree Programme", "Academic Year", "Skills & Motivation"
                        ])
                except Exception:
                    pass
                _headers_initialized.add(spreadsheet_id)
                
            # Append data row (Fastest operation)
            timestamp = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([
                timestamp, sanitize_for_sheet(ip_address), name, roll, email, phone, branch, degree, year, skills
            ])
            
            return {"status": "success", "isNew": is_new, "spreadsheetId": spreadsheet_id}
        
        finally:
            pass
            
    except Exception as e:
        error_msg = str(e)
        if "Quota exceeded" in error_msg or "403" in error_msg:
            return {"status": "fatal_error", "message": f"CRITICAL: Spreadsheet '{event_name}' does not exist and the bot does not have storage quota to create it. Please manually create a blank spreadsheet named '{event_name}' in your Google Drive folder."}
        print(f"Error syncing registration: {e}")
        return {"status": "error", "message": "A database synchronization error occurred. Please contact coding.club@nitmz.ac.in if this persists."}

def background_sync_worker(name, roll, email, phone, branch, degree, year, event_name, skills, ip_address=""):
    max_retries = 5
    base_delay = 2.0  # seconds
    
    for attempt in range(max_retries):
        res = sync_registration_to_folder(
            name=name, roll=roll, email=email, phone=phone, branch=branch, 
            degree=degree, year=year, event_name=event_name, skills=skills, ip_address=ip_address
        )
        
        if res["status"] == "success":
            print(f"Sync success on attempt {attempt + 1}")
            return res
        elif res["status"] == "duplicate":
            print(f"Duplicate registration detected for {roll}")
            return res
        elif res["status"] == "skipped":
            print(f"Sync skipped: {res.get('message')}")
            return res
        elif res["status"] == "fatal_error":
            print(f"FATAL ERROR: {res.get('message')}")
            return res  # Stop retrying immediately for permanent errors
        else:
            error_message = res.get('message', '')
            print(f"Sync attempt {attempt + 1} failed: {error_message}")
            if attempt < max_retries - 1:
                delay = (base_delay ** attempt) + random.uniform(0.5, 1.5)
                time.sleep(delay)
            else:
                print("Max retries reached. Sync failed.")

def sync_team_registration_to_folder(ip_address, event_name, team_name, track, l_name, l_roll, l_email, l_phone, m2_name, m2_roll, m2_email, m3_name, m3_roll, m3_email, m4_name, m4_roll, m4_email):
    folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
    creds_file = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE')
    client_email = os.environ.get('GOOGLE_CLIENT_EMAIL')
    private_key = os.environ.get('GOOGLE_PRIVATE_KEY')
    creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    
    if not folder_id:
        return {"status": "skipped", "message": "GOOGLE_DRIVE_FOLDER_ID is not configured."}
        
    try:
        # Sanitize all form inputs
        s = sanitize_for_sheet
        t_name, t_track, l_n, l_r, l_e, l_p = s(team_name), s(track), s(l_name), s(l_roll), s(l_email), s(l_phone)
        m2_n, m2_r, m2_e = s(m2_name), s(m2_roll), s(m2_email)
        m3_n, m3_r, m3_e = s(m3_name), s(m3_roll), s(m3_email)
        m4_n, m4_r, m4_e = s(m4_name), s(m4_roll), s(m4_email)
        
        gspread_client, drive_service = get_google_clients(creds_file)
        
        try:
            with sheets_api_lock:
                is_new = False
                spreadsheet_id = _spreadsheet_cache.get(event_name)
            
            if not spreadsheet_id:
                query = f"name = '{event_name}' and '{folder_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false"
                results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
                files = results.get('files', [])
                
                if files:
                    spreadsheet_id = files[0]['id']
                else:
                    ss = gspread_client.create(event_name)
                    spreadsheet_id = ss.id
                    is_new = True
                    
                    file_meta = drive_service.files().get(fileId=spreadsheet_id, fields='parents').execute()
                    previous_parents = ",".join(file_meta.get('parents', []))
                    
                    drive_service.files().update(
                        fileId=spreadsheet_id, addParents=folder_id, removeParents=previous_parents, fields='id, parents'
                    ).execute()
                    
                    try:
                        permission = {'type': 'user', 'role': 'writer', 'emailAddress': 'coding.club@nitmz.ac.in'}
                        drive_service.permissions().create(fileId=spreadsheet_id, body=permission, fields='id').execute()
                    except Exception: pass
                
                _spreadsheet_cache[event_name] = spreadsheet_id
                
            ss = gspread_client.open_by_key(spreadsheet_id)
            sheet = ss.sheet1
            
            # Check Duplicates across all roll numbers
            try:
                existing_rolls = []
                try: existing_rolls.extend(sheet.col_values(6)[1:]) # Leader Roll
                except Exception: pass
                try: existing_rolls.extend(sheet.col_values(10)[1:]) # M2 Roll
                except Exception: pass
                try: existing_rolls.extend(sheet.col_values(13)[1:]) # M3 Roll
                except Exception: pass
                try: existing_rolls.extend(sheet.col_values(16)[1:]) # M4 Roll
                except Exception: pass
                
                existing_rolls = [r.upper() for r in existing_rolls if r.strip()]
                
                submitted_rolls = [l_r, m2_r, m3_r, m4_r]
                submitted_rolls = [r.upper() for r in submitted_rolls if r.strip()]
                
                for s_roll in submitted_rolls:
                    if s_roll in existing_rolls:
                        return {"status": "duplicate", "message": f"Registration Denied: A participant may only register for one team. Our records indicate that roll number {s_roll} is already associated with an existing team."}
            except Exception: pass
                
            if spreadsheet_id not in _headers_initialized:
                try:
                    if not sheet.row_values(1):
                        sheet.append_row([
                            "Timestamp", "IP Address", "Team Name", "Track/Domain", "Leader Name", "Leader Roll", "Leader Email", "Leader Phone", 
                            "Member 2 Name", "Member 2 Roll", "Member 2 Email", "Member 3 Name", "Member 3 Roll", "Member 3 Email", 
                            "Member 4 Name", "Member 4 Roll", "Member 4 Email"
                        ], value_input_option="USER_ENTERED")
                except Exception: pass
                _headers_initialized.add(spreadsheet_id)
                
            timestamp = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([
                timestamp, sanitize_for_sheet(ip_address), 
                sanitize_for_sheet(team_name), sanitize_for_sheet(track),
                sanitize_for_sheet(l_name), sanitize_for_sheet(l_roll), sanitize_for_sheet(l_email), sanitize_for_sheet(l_phone),
                sanitize_for_sheet(m2_name), sanitize_for_sheet(m2_roll), sanitize_for_sheet(m2_email),
                sanitize_for_sheet(m3_name), sanitize_for_sheet(m3_roll), sanitize_for_sheet(m3_email),
                sanitize_for_sheet(m4_name), sanitize_for_sheet(m4_roll), sanitize_for_sheet(m4_email)
            ], value_input_option="USER_ENTERED")
            
            return {"status": "success", "isNew": is_new, "spreadsheetId": spreadsheet_id}
        
        finally:
            pass
            
    except Exception as e:
        print(f"Error syncing team registration: {e}")
        return {"status": "error", "message": "A database synchronization error occurred. Please contact coding.club@nitmz.ac.in if this persists."}

def background_sync_team_worker(ip_address, event_name, team_name, track, l_name, l_roll, l_email, l_phone, m2_name, m2_roll, m2_email, m3_name, m3_roll, m3_email, m4_name, m4_roll, m4_email):
    max_retries = 5
    base_delay = 2.0
    
    for attempt in range(max_retries):
        res = sync_team_registration_to_folder(
            ip_address, event_name, team_name, track, l_name, l_roll, l_email, l_phone, m2_name, m2_roll, m2_email, m3_name, m3_roll, m3_email, m4_name, m4_roll, m4_email
        )
        if res["status"] in ["success", "duplicate", "skipped", "fatal_error"]:
            return res
        else:
            if attempt < max_retries - 1:
                time.sleep((base_delay ** attempt) + random.uniform(0.5, 1.5))
            else:
                return res

def sync_dynamic_registration_to_folder(form_id, form_data, submission, ip_address):
    folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
    creds_file = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE')
    client_email = os.environ.get('GOOGLE_CLIENT_EMAIL')
    private_key = os.environ.get('GOOGLE_PRIVATE_KEY')
    creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    
    if not folder_id:
        return {"status": "skipped", "message": "GOOGLE_DRIVE_FOLDER_ID is not configured."}
        
    try:
        gspread_client, drive_service = get_google_clients(creds_file)
        sheet_name = form_data.get('sheet_name', form_data['title'])
        
        try:
            with sheets_api_lock:
                is_new = False
                spreadsheet_id = _spreadsheet_cache.get(sheet_name)
            
            if not spreadsheet_id:
                query = f"name = '{sheet_name}' and '{folder_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false"
                results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
                files = results.get('files', [])
                
                if files:
                    spreadsheet_id = files[0]['id']
                else:
                    ss = gspread_client.create(sheet_name)
                    spreadsheet_id = ss.id
                    is_new = True
                    
                    file_meta = drive_service.files().get(fileId=spreadsheet_id, fields='parents').execute()
                    previous_parents = ",".join(file_meta.get('parents', []))
                    
                    drive_service.files().update(
                        fileId=spreadsheet_id, addParents=folder_id, removeParents=previous_parents, fields='id, parents'
                    ).execute()
                    
                    try:
                        permission = {'type': 'user', 'role': 'writer', 'emailAddress': 'coding.club@nitmz.ac.in'}
                        drive_service.permissions().create(fileId=spreadsheet_id, body=permission, fields='id').execute()
                    except Exception: pass
                
                _spreadsheet_cache[sheet_name] = spreadsheet_id
                
            ss = gspread_client.open_by_key(spreadsheet_id)
            sheet = ss.sheet1
            
            headers = ["Timestamp", "IP Address"]
            for field in form_data['fields']:
                headers.append(field.replace('-comp', ''))
            
            # Check Duplicates
            dup_field = form_data.get('duplicate_check_field')
            if dup_field and dup_field in headers:
                try:
                    col_index = headers.index(dup_field) + 1
                    existing_vals = sheet.col_values(col_index)
                    dup_val = submission.get(dup_field, '')
                    if dup_val and any(dup_val.strip().upper() == r.strip().upper() for r in existing_vals[1:]):
                        return {"status": "duplicate", "message": f"{dup_field} '{dup_val}' is already registered."}
                except Exception: pass
                
            if spreadsheet_id not in _headers_initialized:
                try:
                    if not sheet.row_values(1):
                        sheet.append_row(headers, value_input_option="USER_ENTERED")
                except Exception: pass
                _headers_initialized.add(spreadsheet_id)
                
            timestamp = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
            row_data = [timestamp, sanitize_for_sheet(ip_address)]
            for field in form_data['fields']:
                base_name = field.replace('-comp', '')
                val = submission.get(base_name, '')
                row_data.append(sanitize_for_sheet(val))
                
            sheet.append_row(row_data, value_input_option="USER_ENTERED")
            
            return {"status": "success", "isNew": is_new, "spreadsheetId": spreadsheet_id}
        
        finally:
            pass
            
    except Exception as e:
        print(f"Error syncing dynamic registration: {e}")
        return {"status": "error", "message": "A database synchronization error occurred. Please contact coding.club@nitmz.ac.in if this persists."}

def background_dynamic_sync_worker(form_id, form_data, submission, ip_address):
    max_retries = 5
    base_delay = 2.0
    
    for attempt in range(max_retries):
        res = sync_dynamic_registration_to_folder(form_id, form_data, submission, ip_address)
        if res["status"] in ["success", "duplicate", "skipped", "fatal_error"]:
            return res
        else:
            if attempt < max_retries - 1:
                time.sleep((base_delay ** attempt) + random.uniform(0.5, 1.5))
            else:
                return res

def mark_attendance(roll_number, attendance_config):
    """
    Checks if a roll number exists in the registration sheet.
    If found, adds today's date as a column header (if not already present) and marks TRUE for that student.
    If not found, returns not_registered status.
    """
    folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
    creds_file = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE')
    
    if not folder_id:
        return {"status": "error", "message": "GOOGLE_DRIVE_FOLDER_ID is not configured."}
    
    try:
        gspread_client, drive_service = get_google_clients(creds_file)
        sheet_name = attendance_config.get('sheet_name')
        
        # Find the spreadsheet
        with sheets_api_lock:
            spreadsheet_id = _spreadsheet_cache.get(sheet_name)
        
        if not spreadsheet_id:
            query = f"name = '{sheet_name}' and '{folder_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false"
            results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = results.get('files', [])
            
            if files:
                spreadsheet_id = files[0]['id']
                _spreadsheet_cache[sheet_name] = spreadsheet_id
            else:
                return {"status": "error", "message": f"Registration sheet '{sheet_name}' not found. Please contact the admin."}
        
        ss = gspread_client.open_by_key(spreadsheet_id)
        sheet = ss.sheet1
        
        # Get all data to find the roll number
        all_data = sheet.get_all_values()
        if not all_data:
            return {"status": "not_registered"}
        
        headers = all_data[0]
        
        # Find Roll Number column
        roll_col_name = attendance_config.get('roll_column', 'Roll Number')
        roll_col_idx = None
        for i, h in enumerate(headers):
            if h.strip().upper() == roll_col_name.strip().upper():
                roll_col_idx = i
                break
        
        if roll_col_idx is None:
            return {"status": "error", "message": f"Column '{roll_col_name}' not found in the sheet."}
        
        # Find the row with matching roll number
        roll_upper = roll_number.strip().upper()
        target_row = None
        student_name = None
        for row_idx, row in enumerate(all_data[1:], start=2):  # start=2 because sheets are 1-indexed + header
            if roll_col_idx < len(row) and row[roll_col_idx].strip().upper() == roll_upper:
                target_row = row_idx
                # Try to get the student's name (usually the column before roll number, or first data col after Timestamp/IP)
                name_col_idx = None
                for ni, nh in enumerate(headers):
                    if 'name' in nh.lower() and 'team' not in nh.lower():
                        name_col_idx = ni
                        break
                if name_col_idx is not None and name_col_idx < len(row):
                    student_name = row[name_col_idx]
                break
        
        if target_row is None:
            return {"status": "not_registered"}
        
        # Today's date as column header in IST
        today_str = datetime.now(IST).strftime("%d-%b-%Y")
        
        # Check if today's date column already exists
        date_col_idx = None
        for i, h in enumerate(headers):
            if h.strip() == today_str:
                date_col_idx = i + 1  # 1-indexed for gspread
                break
        
        if date_col_idx is None:
            # Add new column header for today's date
            date_col_idx = len(headers) + 1
            sheet.update_cell(1, date_col_idx, today_str)
        
        # Check if already marked
        try:
            current_val = sheet.cell(target_row, date_col_idx).value
            if current_val and current_val.strip().upper() == "TRUE":
                return {"status": "already_marked", "name": student_name or roll_number}
        except Exception:
            pass
        
        # Mark attendance as TRUE
        sheet.update_cell(target_row, date_col_idx, "TRUE")
        
        return {"status": "success", "name": student_name or roll_number}
        
    except Exception as e:
        print(f"Error marking attendance: {e}")
        return {"status": "error", "message": "Unable to record attendance at this time due to a database error. Please try again shortly."}

def background_attendance_worker(roll_number, attendance_config):
    max_retries = 3
    base_delay = 2.0
    
    for attempt in range(max_retries):
        res = mark_attendance(roll_number, attendance_config)
        if res["status"] in ["success", "already_marked", "not_registered", "skipped"]:
            return res
        else:
            if attempt < max_retries - 1:
                time.sleep((base_delay ** attempt) + random.uniform(0.5, 1.5))
            else:
                return res


