# Operational Guidelines & Event Synchronization Protocol

This document outlines mandatory operational protocols for event managers, web coordinators, and executive members of the Coding & AI Club, NIT Mizoram when initiating new events or managing spreadsheet databases.

---

## 1. Event Initiation & Spreadsheet Naming Conventions

When launching a new event, workshop, or competition, execute the following procedure:

1. **Register Event in `data.py`**:
   Add a dictionary entry to the `EVENT_DATA` list in `data.py` with `"registration_open": True` and specify the exact `title` string.

2. **Initialize Google Spreadsheet**:
   Navigate to the designated Google Drive Folder configured under `GOOGLE_DRIVE_FOLDER_ID`. Create a new blank Google Sheet.

3. **Exact String Match Requirement**:
   The Google Sheet **must be named identically to the `title` string specified in `data.py`**.
   - *Example*: If the event title in `data.py` is `"Samyuga - Prarambh"`, the Google Sheet title must be `"Samyuga - Prarambh"`.
   - *Technical Rationale*: The backend search queries the Google Drive API for a file matching the exact string name. Any discrepancy in spelling, spacing, or capitalization will prevent the synchronization engine from locating the target file, resulting in form submission failures.

---

## 2. Service Account Storage Quotas

Google Cloud Service Accounts operating under default quota tiers are restricted from creating new files directly within root accounts due to zero-byte default storage allocations.
- **Protocol**: Spreadsheets must be created manually by an authorized club administrator within the shared Google Drive folder.
- **Result**: Because the spreadsheet is created within the administrator's personal or institutional Drive storage quota, the Service Account requires only **Editor** permissions to append user records.

---

## 3. Google Drive Permission Delegation

The Service Account operates under principle of least privilege:
- Ensure the Google Drive folder (`GOOGLE_DRIVE_FOLDER_ID`) is explicitly shared with the Service Account email address (`GOOGLE_CLIENT_EMAIL`).
- Assign **Editor** role permissions to the Service Account. Assigning "Viewer" permissions will result in write authorization failures.

---

## 4. Serverless Execution & Synchronous Processing

The backend executes database synchronization synchronously within Flask request handlers to guarantee complete data delivery before rendering success confirmation pages.
- **Serverless Compatibility**: This synchronous execution ensures full compatibility with serverless execution environments (such as Vercel) by completing API requests before function freezing occurs.
- **User Interface Handling**: Web forms feature progress overlays that inform users during active database synchronization.
