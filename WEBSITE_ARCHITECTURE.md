# Website Architecture & Security Blueprint

This document details the end-to-end flow, concurrency design, backup mechanisms, and layered threat protections implemented on this website.

---

## 1. Environment Configuration (`.env`)

To activate the Google Sheets & Drive synchronization, configure the following keys in your local `.env` file:

```env
# 1. The unique ID of the Google Drive Folder where spreadsheets will reside.
# Copy this from the folder URL in your browser: https://drive.google.com/drive/folders/YOUR_FOLDER_ID
GOOGLE_DRIVE_FOLDER_ID=your-google-drive-folder-id

# 2. The filename of your Google Cloud Service Account JSON credentials.
# Put this file in the project root directory (e.g. named credentials.json) and enter its name here.
GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json
```

### How to obtain the Service Account Credentials File:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a project.
3. Enable the **Google Sheets API** and **Google Drive API** in the API Library.
4. Go to **IAM & Admin** > **Service Accounts** and click **Create Service Account**.
5. Give it a name, click **Done**, click on the newly created service account, and go to the **Keys** tab.
6. Click **Add Key** > **Create New Key** (choose JSON format). This downloads the JSON key file.
7. Move that downloaded file to your project root (e.g., `/home/dilip_sahu/website/credentials.json`) and configure `GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json` in your `.env`.

---

## 2. Request Data Flow (Level 0 to Level 4)

Here is the step-by-step path of a candidate submission:

1. **Level 0: User Submission**
   * The candidate inputs details (Name, Roll ID, Email, Phone, Branch, Degree, Year, Event, and Skills/Motivation) into the `/register` web form and submits it.

2. **Level 1: Backend Sanitization**
   * The Flask request handler processes the POST request.
   * Special sanitization filters clean the inputs:
     * HTML and Script tags are stripped to block cross-site scripting (XSS) injection.
     * Special characters (`=`, `+`, `-`, `@`) at the start of any input are escaped with a single quote (`'`) to block spreadsheet formula execution.

3. **Level 2: Log Backup (Local Fail-Safe)**
   * The server outputs a structured `EVENT REGISTRATION BACKUP: ...` log line to `stdout` containing the entire candidate record. This log serves as an immutable backup database captured by your cloud host.

4. **Level 3: Decoupled Processing (No Lag)**
   * Flask spawns a background daemon thread (`background_sync_worker`) carrying the registration payload.
   * The main Flask worker process immediately returns the `register_success.html` confirmation page to the browser. The page loads in **under 50 milliseconds**, keeping the site responsive.

5. **Level 4: Locked API Sync & Error Recovery**
   * The background thread attempts to acquire the `sheets_api_lock` (ensuring thread safety).
   * The thread authenticates via the Service Account JSON file.
   * It checks the target Google Drive folder. If a sheet with the event's name does not exist, it creates it, moves it to the folder, grants editor permissions to `coding.club@nitmz.ac.in`, writes columns, and releases the lock.
   * It appends the candidate row.
   * **Error Management**: If the Google API returns a rate limit error (HTTP 429) or network lag occurs, the thread sleeps on a randomized exponential delay (`2s`, `4s`, `8s` + jitter) and retries up to 5 times.

---

## 3. Layered Security & Safety Controls

| Threat | Impact | Defensive Control |
| :--- | :--- | :--- |
| **Spreadsheet Formula Injection** | Rogue inputs like `=HYPERLINK(...)` execute commands or extract data when administrators open the sheet in Excel/Google Sheets. | **Input Escaping**: Leading `=, +, -, @` characters are prepended with a single quote (`'`), converting them into harmless string literals. |
| **HTML / Script Injection** | Bad actors enter `<script>` tags, causing XSS execution on notice boards or contact logs. | **Tag Stripping**: Regex parser strips out all HTML elements and brackets from registration variables. |
| **Race Conditions (Double Sheets)** | Under high concurrency, two requests check if a sheet exists at the same millisecond. Both see it's missing and create duplicate sheets. | **Global API Lock**: A `threading.Lock()` synchronizes all search, create, and append calls, forcing threads to execute sequentially. |
| **API Rate Limits (HTTP 429)** | Google limits Sheet edits to 60/minute, causing write failures under peak registration hours. | **Exponential Backoff with Jitter**: Background threads automatically retry on a sliding delay window, smoothing out requests. |
| **System Outage / Key Loss** | Complete failure to connect to Google (e.g. key revoked, internet down). | **Console Log Backups**: Full details are written to standard logger before sync is attempted, allowing 100% data recovery from server logs. |
