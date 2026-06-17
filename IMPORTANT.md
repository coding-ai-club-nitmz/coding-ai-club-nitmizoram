# 🚨 IMPORTANT PROJECT GUIDELINES 🚨

Please read this document carefully before managing events or modifying the Google Sheets integration.

## 1. Creating a New Event (CRUCIAL)
When you want to host a new event and start accepting registrations, you MUST follow these exact steps:

1. **Update `data.py`**: Add your new event to the `EVENT_DATA` list in `data.py` and set `"registration_open": True`.
2. **Create the Spreadsheet**: Go to your specific Google Drive Folder (`1dbs15E1SaMtgPZNYRKWvCR7dnfIA5Q16`). Right-click and create a new, blank Google Sheet.
3. **Name it Exactly the Same**: You **MUST name the spreadsheet exactly the same as the event title** you put in `data.py`. 
   - *Example:* If your event title in `data.py` is `Samyuga - Prarambh`, the spreadsheet name must be exactly `Samyuga - Prarambh`. 
   - *Why?* The script searches the folder for a file with that exact name. If there is a typo, space mismatch, or capitalization difference, the bot will not find it and the registration will fail.

## 2. Storage Quota Limits
Free-tier Google Cloud Service Accounts (the "Automator" bot) are heavily restricted by Google and usually have **0 bytes** of Drive storage.
- The bot **cannot** create new spreadsheets from scratch because it instantly hits a "Quota Exceeded" error. 
- This is why you must manually create the blank spreadsheet first (as mentioned above). Because YOU created it, it uses your personal Google Drive storage, and the bot is freely allowed to *edit* it.

## 3. Google Drive Folder Access
The Automator bot operates securely and can only see what you explicitly share with it.
- **Check Access**: Ensure that your Google Drive Folder is shared with the bot's email address (`website-datasaving@website-automator-499710.iam.gserviceaccount.com`).
- It must be given **Editor** permissions. If it only has "Viewer" access, or if the folder isn't shared, it cannot type the student registrations into the sheets.

## 4. Hosting Warning (Vercel)
This application uses Python's `threading.Thread` to send data to Google Sheets in the background. This ensures the website feels lightning-fast for the student clicking "Submit".
- **VPS / Normal Servers (Safe)**: If you host this on AWS, Render, DigitalOcean, or Hostinger VPS, background threads work perfectly.
- **Vercel / Serverless (Danger)**: If you deploy this to Vercel, Vercel completely freezes the server the exact millisecond the success page loads. This means your background thread will be frozen and killed before it finishes sending data to Google Sheets! 
   - *Fix for Vercel:* If you MUST use Vercel, you need to remove the background threading in `app.py` and run the Google Sheets function normally, so the script waits for Google to confirm the save before loading the Success page.
