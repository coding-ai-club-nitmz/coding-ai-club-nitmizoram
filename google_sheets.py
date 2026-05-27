import os
import re
import time
import random
import threading
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread

# Global thread lock to prevent race conditions during concurrent Drive lookup/creation and Sheets writing
sheets_api_lock = threading.Lock()

def sanitize_for_sheet(value):
    """
    Sanitizes values entered into the spreadsheet cells:
    1. Prevents Spreadsheet Formula Injection (CSV Injection) by prefixing leading 
       special characters (=, +, -, @) with a single quote.
    2. Prevents script/HTML injection attacks by stripping raw HTML tags.
    """
    if not value:
        return ""
    value_str = str(value).strip()
    
    # Escape leading characters to prevent Spreadsheet Formula / CSV Injection
    if value_str and value_str[0] in ('=', '+', '-', '@'):
        value_str = "'" + value_str
        
    # Strip HTML and script tags to prevent HTML/XSS injection
    value_str = re.sub(r'<[^>]*>', '', value_str)
    return value_str

def sync_registration_to_folder(name, roll, email, phone, branch, degree, year, event_name, skills):
    """
    Connects directly to Google Drive and Google Sheets APIs:
    1. Authenticates using the credentials file configured in GOOGLE_SERVICE_ACCOUNT_FILE.
    2. Searches the Google Drive Folder (GOOGLE_DRIVE_FOLDER_ID) for a spreadsheet named `event_name`.
    3. If found, appends the sanitized candidate registration details.
    4. If not found, creates the spreadsheet, moves it into the folder, limits sharing to
       coding.club@nitmz.ac.in, initializes headers, and then appends candidate details.
    """
    folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')
    creds_file = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE')
    
    if not folder_id or not creds_file:
        return {"status": "skipped", "message": "GOOGLE_DRIVE_FOLDER_ID or GOOGLE_SERVICE_ACCOUNT_FILE is not configured."}
        
    if not os.path.exists(creds_file):
        return {"status": "error", "message": f"Credentials file not found at path: {creds_file}"}

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
        
        # Load API scopes
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = service_account.Credentials.from_service_account_file(creds_file, scopes=scopes)
        
        # Initialize Google Client services
        drive_service = build('drive', 'v3', credentials=creds)
        gspread_client = gspread.authorize(creds)
        
        with sheets_api_lock:
            # Find if spreadsheet for eventName already exists in the target folder
            query = f"name = '{event_name}' and '{folder_id}' in parents and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false"
            results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = results.get('files', [])
            
            is_new = False
            if files:
                spreadsheet_id = files[0]['id']
                ss = gspread_client.open_by_key(spreadsheet_id)
                sheet = ss.sheet1
            else:
                # Create new spreadsheet
                ss = gspread_client.create(event_name)
                spreadsheet_id = ss.id
                is_new = True
                
                # Move the new spreadsheet file to the target Google Drive folder
                file_meta = drive_service.files().get(fileId=spreadsheet_id, fields='parents').execute()
                previous_parents = ",".join(file_meta.get('parents', []))
                
                drive_service.files().update(
                    fileId=spreadsheet_id,
                    addParents=folder_id,
                    removeParents=previous_parents,
                    fields='id, parents'
                ).execute()
                
                # Share access only with coding.club@nitmz.ac.in as editor
                try:
                    permission = {
                        'type': 'user',
                        'role': 'writer',
                        'emailAddress': 'coding.club@nitmz.ac.in'
                    }
                    drive_service.permissions().create(
                        fileId=spreadsheet_id,
                        body=permission,
                        fields='id'
                    ).execute()
                except Exception as share_err:
                    print(f"Warning: Failed to share spreadsheet with coding.club@nitmz.ac.in: {share_err}")
                    
                # Populate headers
                sheet = ss.sheet1
                sheet.append_row([
                    "Timestamp", 
                    "Full Name", 
                    "Roll Number", 
                    "Email Address", 
                    "Phone Number", 
                    "Branch/Department", 
                    "Degree Programme", 
                    "Academic Year", 
                    "Skills & Motivation"
                ])
                
            # Append data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([
                timestamp,
                name,
                roll,
                email,
                phone,
                branch,
                degree,
                year,
                skills
            ])
            
            return {"status": "success", "isNew": is_new, "spreadsheetId": spreadsheet_id}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def background_sync_worker(name, roll, email, phone, branch, degree, year, event_name, skills):
    """
    Runs in a background thread to prevent blocking the Flask request-response lifecycle.
    Implements a retry mechanism with exponential backoff to handle Google API rate limits (HTTP 429)
    and temporary network glitches.
    """
    max_retries = 5
    base_delay = 2.0  # seconds
    
    for attempt in range(max_retries):
        res = sync_registration_to_folder(
            name=name,
            roll=roll,
            email=email,
            phone=phone,
            branch=branch,
            degree=degree,
            year=year,
            event_name=event_name,
            skills=skills
        )
        
        if res["status"] == "success":
            print(f"Background sync success on attempt {attempt + 1}: spreadsheetId={res.get('spreadsheetId')}")
            return
            
        elif res["status"] == "skipped":
            # Credentials are not configured, no need to retry
            print(f"Background sync skipped: {res.get('message')}")
            return
            
        else:
            error_message = res.get('message', '')
            print(f"Background sync attempt {attempt + 1} failed: {error_message}")
            
            if attempt < max_retries - 1:
                # Exponential backoff with random jitter to prevent collision
                delay = (base_delay ** attempt) + random.uniform(0.5, 1.5)
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Registration sync failed.")
