# Coding & AI Club Web Platform — NIT Mizoram

Official web application repository of the **Coding & AI Club** at the **National Institute of Technology Mizoram (राष्ट्रीय प्रौद्योगिकी संस्थान, मिज़ोरम)**.

Official Portal: [coding-ai-club-nitmizoram.vercel.app](https://coding-ai-club-nitmizoram.vercel.app)

---

## Executive Overview

This repository houses the production source code for the Coding & AI Club's digital platform. Designed as a high-performance, data-driven web application, it serves as the official portal for student activities, competitive programming initiatives, hackathons, open-source projects, and administrative utilities.

The platform is engineered with a strict separation of concerns, separating content management from presentation logic. All site content is driven by structured data objects, allowing seamless updates without template modification.

---

## Technical Architecture & Feature Specification

### 1. Data-Driven Content Management
- **Single Source of Truth**: Managed entirely through central data structures (`data.py`), decoupling content from HTML/CSS layout templates.
- **Dynamic Hot-Reloading**: Backend automatically detects modifications to the data module and reloads application state during development without requiring server restarts.

### 2. Google Drive & Sheets Integration Engine
- **Automated Registration Synchronization**: Backend form handlers sanitize student submissions, normalize field formats, and synchronize records directly to designated Google Spreadsheets via Google Cloud Service Accounts.
- **Security & Injection Defenses**: Implements formula escaping (protecting against CSV/Excel formula execution attacks) and XSS HTML tag stripping.
- **Concurrency Control**: Process thread locking (`sheets_api_lock`) prevents race conditions during concurrent user submissions.

### 3. Student Portal & Member Utilities (`/portal`)
- **Attendance Verification (`/attendance`)**: Time-restricted attendance recording for club workshops and technical sessions using Indian Standard Time (IST).
- **Certificate Verification System (`/verify`)**: Online credential verification engine allowing students, recruiters, and institutions to validate official event certificates.
- **Direct Calendar Integration**: Generates Google Calendar event creation URLs and `.ics` iCalendar files for upcoming events.

### 4. Interactive Frontend Experience
- **Filterable Showcase**: Client-side filtering for technical projects by domain (`AI & ML`, `Web Systems`, `Open Roles`).
- **Glassmorphism Toast Notifications**: Asynchronous user feedback banners replacing standard browser alerts.
- **Offline / Network Detection**: Automatic network status monitoring (`online`/`offline` event listeners) to safeguard form submissions during poor connectivity.

### 5. Production & Search Engine Optimization
- **Structured Data (Schema.org)**: Injected JSON-LD `EducationalOrganization` metadata for Google Search snippet indexing.
- **Dynamic Meta Tags**: Automated Open Graph (`og:`) and Twitter Card previews customized per page and notice item.

---

## Technology Stack

- **Backend Framework**: Python 3.12 / Flask (3.0+)
- **WSGI / App Server**: Gunicorn / Werkzeug
- **Spreadsheet Integration**: `gspread`, `google-api-python-client`, `google-auth`
- **Frontend Layer**: Vanilla HTML5, CSS3 (Custom Variables, Flexbox/Grid), Jinja2 Templating
- **Security & Headers**: `Flask-Talisman` (Content Security Policy), `Flask-Limiter` (Rate Limiting)
- **Quality Assurance**: `unittest`, `flake8`, `htmlhint`
- **Continuous Integration / Deployment**: GitHub Actions (`.github/workflows/ci-cd.yml`), Vercel / Gunicorn

---

## Local Development & Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ (for HTMLHint validation)
- Google Cloud Service Account JSON credentials (for Google Sheets sync)

### Setup Procedure

1. **Clone Repository**:
   ```bash
   git clone https://github.com/coding-ai-club-nitmz/coding-ai-club-nitmizoram.git
   cd coding-ai-club-nitmizoram
   ```

2. **Initialize Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_DRIVE_FOLDER_ID=your-google-drive-folder-id
   GOOGLE_CLIENT_EMAIL=your-service-account-email@project.iam.gserviceaccount.com
   GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   ```

5. **Run Local Server**:
   ```bash
   python app.py
   ```
   The local application will be accessible at `http://127.0.0.1:8000/`.

---

## Directory Structure

```text
├── app.py                      # Main Flask application & route controllers
├── data.py                     # Central data store (Single source of truth)
├── google_sheets.py            # Google API engine & spreadsheet synchronization
├── requirements.txt            # Python dependencies
├── Procfile                    # Production Gunicorn configuration
├── vercel.json                 # Vercel serverless routing & header rules
├── robots.txt                  # Search engine crawler directives
├── sitemap.xml                 # XML Sitemap for search indexing
├── .htmlhintrc                 # HTMLHint linting configuration
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Automated CI/CD testing & deployment workflow
├── static/
│   ├── style.css               # Global CSS stylesheet & design tokens
│   └── images/                 # Logos, graphics, and asset media
├── templates/
│   ├── base.html               # Master shell template with SEO headers & navbar
│   ├── index.html              # Homepage template
│   ├── portal.html             # Student portal dashboard
│   ├── verify.html             # Certificate verification template
│   └── ...                     # Sub-page templates
└── tests/
    ├── test_routes.py          # Route & integration test cases
    └── test_sanitization.py    # XSS & CSV formula injection test cases
```

---

## Continuous Integration & Deployment Pipeline

This repository incorporates a GitHub Actions CI/CD Pipeline (`.github/workflows/ci-cd.yml`):

1. **Quality Gate (`test-and-lint` Job)**:
   Triggered on every push or pull request to `main` or `development` branches. Executes:
   - Python compilation check (`app.py`, `data.py`, `google_sheets.py`).
   - Flake8 code syntax and import verification.
   - HTMLHint template structural validation.
   - Unit test execution (`tests/test_routes.py`, `tests/test_sanitization.py`).

2. **Gated Deployment (`deploy` Job)**:
   Executes deployment on Vercel Production only when all test cases pass on `main`.

---

## Technical Governance & Maintenance Documentation

- [FUTURE_TEAM_GUIDE.md](./FUTURE_TEAM_GUIDE.md): Technical maintenance manual for future web team coordinators.
- [WEBSITE_ARCHITECTURE.md](./WEBSITE_ARCHITECTURE.md): Architectural blueprint and security specification.
- [IMPORTANT.md](./IMPORTANT.md): Operational guidelines for event management and Google Drive permissions.

---

## License & Intellectual Property

Copyright (c) 2026 Coding & AI Club, NIT Mizoram. **All Rights Reserved.**

This repository and its contents are proprietary property of the Coding & AI Club, National Institute of Technology Mizoram. Unauthorized copying, distribution, or reproduction of this software or its components is strictly prohibited.
