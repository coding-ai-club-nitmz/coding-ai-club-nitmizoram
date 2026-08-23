#  Coding & AI Club Website — NIT Mizoram

Welcome to the official portal of the **Coding & AI Club** at the **National Institute of Technology Mizoram (राष्ट्रीय प्रौद्योगिकी संस्थान, मिज़ोरम)**. 

This website serves as a modern, high-performance, and responsive hub to showcase club innovations, core values, announcements, active members, resources, and technical projects.

---

##  Key Features

*   **100% Data-Driven Architecture**: Managed entirely via central data structures. Zero HTML knowledge required to update the site.
*   **Google Sheets Automation Engine**: Fully integrated backend that automatically normalizes user data, verifies duplicates, and syncs event registrations directly to secure Google Drive Spreadsheets in real-time.
*   **Dynamic Notice Board**: A custom horizontal slider showcasing the 3 latest announcements side-by-side with smooth horizontal scrolling for more. Includes context-aware `/notices/<id>` detail routing.
*   **Context-Aware Communication**: Smart pre-filled join/inquiry forms that auto-load custom subject titles and template messages depending on the notice, project contribution, or contact option clicked.
*   **Premium Visual Experience**: Harmony of HSL primary-navy and modern typography with absolute responsiveness on all device viewports. Includes dynamic glassmorphism UI overlays.
*   **Production & SEO Optimized**: Features high-fidelity dynamic Open Graph previews, custom dynamic meta tags for search engine bots, and valid `sitemap.xml` & `robots.txt` configurations.

---

##  Technology Stack

*   **Backend**: Python / Flask (3.0+)
*   **Database Integration**: Google Drive & Google Sheets API (`gspread`, `google-api-python-client`)
*   **Frontend**: Vanilla HTML5, CSS3, Jinja2 template engine
*   **Dev Server**: Werkzeug / Gunicorn
*   **Deployment Support**: Pre-configured for Vercel and Render (with `Procfile` and `vercel.json`)

---

##  Quick Start & Local Development

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.
You will also need to set up a Google Cloud Service Account and configure your `.env` file for database syncing.

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/coding-ai-club-nitmz/coding-ai-club-nitmizoram.git
cd coding-ai-club-nitmizoram

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Development Server
```bash
python app.py
```
The server will start running at **`http://127.0.0.1:8000/`**. 

> [!NOTE]  
> The development server includes dynamic **no-cache HTTP headers**, meaning any changes you make to the templates or stylesheet will show up instantly on page refresh.

---

##  Project Structure

```bash
├── app.py              # Main Flask application (Route definitions & data formatting)
├── data.py             # Central Data Store (Single source of truth for all content)
├── google_sheets.py    # Google API Engine (Handles Drive queries, Sheets append, Cache)
├── static/             # Static assets folder (Flask default)
│   ├── style.css       # Global CSS variables, layouts, and responsive media queries
│   └── images/         # Static logos, avatars, and event graphics
├── templates/          # Jinja2 HTML Templates
│   ├── base.html       # Shell structure, dynamic SEO headers, Navbar, and Footer
│   ├── index.html      # Homepage (Centered welcome & Horizontal Notice Board)
│   ├── register.html   # Live Event Registration form with data validation
│   └── ...             # Other modular UI pages
```

---

##  Deployment

The repository is pre-configured for rapid production deployment:
*   **Vercel**: Simply connect the repository to Vercel. Be sure to configure `GOOGLE_CLIENT_EMAIL` and `GOOGLE_PRIVATE_KEY` in the Vercel Dashboard Environment Variables. The `vercel.json` configuration handles serverless routing automatically.
*   **Render / VPS**: Uses the pre-configured `Procfile` to run a production-grade WSGI server via `gunicorn`.

---

##  License
Copyright (c) 2026 Coding & AI Club, NIT Mizoram. **All Rights Reserved.**

This repository and its contents are proprietary. You may not use, copy, modify, distribute, or reproduce this software without explicit prior written permission from the copyright holders. 

Built by the **Coding & AI Club Web Team, NIT Mizoram**.
