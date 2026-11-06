# System Architecture & Security Blueprint

This document details request execution flows, concurrency design, database synchronization mechanisms, and threat mitigations implemented on the Coding & AI Club Web Platform (NIT Mizoram).

---

## 1. Environment Configuration (`.env`)

Google Sheets and Google Drive synchronization requires the following environment variables:

```env
# Google Drive Folder ID where event spreadsheets reside
GOOGLE_DRIVE_FOLDER_ID=your-google-drive-folder-id

# Service Account Email Address
GOOGLE_CLIENT_EMAIL=your-service-account-email@project.iam.gserviceaccount.com

# Service Account Private Key (RSA)
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
```

### Service Account Provisioning Procedure
1. Access the Google Cloud Console (`console.cloud.google.com`).
2. Select or create an institutional project.
3. Enable **Google Sheets API** and **Google Drive API** in the API Library.
4. Navigate to **IAM & Admin** > **Service Accounts** and create a Service Account.
5. Generate a JSON Key for the Service Account.
6. Configure `GOOGLE_CLIENT_EMAIL` and `GOOGLE_PRIVATE_KEY` in environment variables or host secret managers.

---

## 2. Request Data Pipeline

Candidate form submissions follow a 4-layer execution pipeline:

1. **Layer 0: User Submission**
   - User inputs academic and contact credentials on `/register`, `/register/<event_id>`, or `/apply/<form_id>`.

2. **Layer 1: Input Sanitization & Threat Filtering**
   - Handlers strip script and HTML tags (`re.sub(r'<[^>]*>', '', value)`) to block Cross-Site Scripting (XSS).
   - Handlers escape leading `=, +, -, @` characters with a single quote (`'`) to block CSV/Spreadsheet formula execution attacks.

3. **Layer 2: Console Fail-Safe Logging**
   - Server writes a structured `EVENT REGISTRATION BACKUP: ...` log line to `stdout` before initiating remote network calls. This serves as an immutable backup log captured by host log managers.

4. **Layer 3: Synchronous API Synchronization**
   - Handler invokes `sync_registration_to_folder` under thread lock (`sheets_api_lock`) to serialize API requests.
   - Queries Google Drive API for an existing sheet matching the exact event title.
   - Appends student data row.
   - **Fault Tolerance**: If Google API rate limits (HTTP 429) or transient network errors occur, the backend retries up to 5 times with exponential backoff (`2s`, `4s`, `8s` + jitter) before failing gracefully.

---

## 3. Threat Matrix & Security Controls

| Vulnerability / Threat | Risk & Potential Impact | Defensive Control Implemented |
| :--- | :--- | :--- |
| **CSV / Formula Injection** | Rogue inputs like `=HYPERLINK(...)` execute commands when administrators open Google Sheets. | **Leading Character Escaping**: `=, +, -, @` characters are prepended with `'`, converting them into string literals. |
| **Cross-Site Scripting (XSS)** | Injection of `<script>` tags causing execution in browser viewports. | **HTML Tag Stripping**: Regex parser removes all HTML tags and angle brackets. |
| **Race Conditions (Duplicate Spreadsheets)** | Simultaneous requests creating duplicate event spreadsheets. | **Global API Lock**: `threading.Lock()` synchronizes search, creation, and row append calls sequentially. |
| **API Rate Limiting (HTTP 429)** | Exceeding Google Sheets write limits (60/min) causing request dropouts. | **Exponential Backoff**: Automatic retry loop over a sliding delay window with randomized jitter. |
| **Header Injection Attacks** | Spoofed `X-Forwarded-For` HTTP headers corrupting client IP logs. | **Regex IP Validation**: `get_client_ip()` validates IP syntax before logging. |

---

## Technical Governance & Copyright

Copyright (c) 2026 Coding & AI Club, NIT Mizoram. **All Rights Reserved.**
