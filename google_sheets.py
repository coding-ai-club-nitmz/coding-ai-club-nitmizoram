import os
import re
import time
import random
import threading
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread

# Global thread lock to prevent race conditions during concurrent writing
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
            creds_info = {
                "type": "service_account",
                "project_id": "website-automator-499710",
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
    if value_str and value_str[0] in ('=', '+', '-', '@'):
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
        return {"status": "error", "message": "Credentials not found. Please set GOOGLE_CLIENT_EMAIL and GOOGLE_PRIVATE_KEY in your .env"}

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
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([
                timestamp, ip_address, name, roll, email, phone, branch, degree, year, skills
            ])
            
            return {"status": "success", "isNew": is_new, "spreadsheetId": spreadsheet_id}
        
    except Exception as e:
        error_msg = str(e)
        if "Quota exceeded" in error_msg or "403" in error_msg:
            return {"status": "fatal_error", "message": f"CRITICAL: Spreadsheet '{event_name}' does not exist and the bot does not have storage quota to create it. Please manually create a blank spreadsheet named '{event_name}' in your Google Drive folder."}
        return {"status": "error", "message": error_msg}

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
