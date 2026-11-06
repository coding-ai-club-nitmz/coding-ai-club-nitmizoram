# Future Web Team Maintenance & Technical Manual

Welcome to the technical maintenance manual for the **Coding & AI Club Web Platform (NIT Mizoram)**. This guide details software architecture, content management procedures, design token specifications, and database operations for incoming web team coordinators and core developers.

---

## 1. Central Data Store: `data.py`

The website is engineered around a data-driven architecture. **Content updates do not require HTML modifications.** All textual content, notice board items, team profiles, event schedules, and certificate records are managed within [data.py](./data.py).

### Core Data Structures in `data.py`

#### A. Global Club Metadata (`GLOBAL_DATA`)
Stores official branding, institutional name, copyright notice, and social contact endpoints:
```python
GLOBAL_DATA = {
    "club_name": "Coding & AI Club",
    "tagline": "Code . Create . Collaborate",
    "hindi_name": "राष्ट्रीय प्रौद्योगिकी संस्थान, मिज़ोरम",
    "copyright": "© 2026 Coding & AI Club",
    "social": {
        "email": "coding.club@nitmz.ac.in",
        "instagram": "https://www.instagram.com/codingclub_nitmz",
        "linkedin": "https://www.linkedin.com/company/coding-club-nit-mizoram/"
    }
}
```

#### B. Announcements & Notice Board (`ANNOUNCEMENTS`)
Contains official announcements and notice items:
- `"featured": True`: Displays item on homepage notice slider.
- `"link"`: Specifies action URL (e.g. `"/events"`, `"/join"`).
- `"prefill"`: Configures pre-populated topic and body text for application forms.

#### C. Leadership & Core Committee (`TEAM_DATA`)
Categorized lists (`mentors`, `founding`, `core`, `coordinators`). To add a team member:
```python
{"name": "Student Name", "role": "Position Title", "badge": "Lead", "image": "images/filename.jpg"}
```
> [!NOTE]  
> Store local member images in `static/images/`. If a photograph is unavailable, use UI Avatars URL format: `"https://ui-avatars.com/api/?name=First+Last&background=random&color=fff&size=200"`.

#### D. Student Portal & Certificate Records (`CERTIFICATES_DATA`)
Stores verified credential records for the `/verify` portal:
```python
CERTIFICATES_DATA = {
    "CERT-2026-INV-028": {
        "cert_id": "CERT-2026-INV-028",
        "student_name": "Student Name",
        "roll": "BT24CS028",
        "event_title": "Innovaite 2026 AI/ML Challenge",
        "issue_date": "August 26, 2026",
        "role": "Certificate of Merit",
        "status": "Official & Verified"
    }
}
```

---

## 2. Design Tokens & Stylesheet Standards

All visual styles and CSS custom properties are centralized in [static/style.css](./static/style.css).

### CSS Design Tokens
- `--primary`: `#0a1f44` (Navy Primary)
- `--secondary`: `#102a56` (Navy Secondary)
- `--accent`: `#8ab4f8` (Ice Blue Highlight)
- `--bg`: `#f4f6f9` (Canvas Background)
- `--bg-card`: `#ffffff` (Card Surface)

### Typography Rules
- **Headings (`h1`, `h2`, `h3`)**: Enforce `font-family: 'Rajdhani', sans-serif; font-weight: 700;`.
- **Body Text**: Enforce `font-family: 'Noto Sans', sans-serif; line-height: 1.7;`.

---

## 3. Google Drive Spreadsheet Backend Operations

The registration engine ([google_sheets.py](./google_sheets.py)) synchronizes student submissions directly to Google Drive.

### Event Spreadsheet Setup Protocol
1. Create a blank Google Sheet in the shared Google Drive folder (`GOOGLE_DRIVE_FOLDER_ID`).
2. Title the sheet **exactly matching** the event `title` in `data.py` (e.g. `24 Hours Hackathon`).
3. Verify that the Service Account email (`GOOGLE_CLIENT_EMAIL`) has **Editor** permissions on the folder.
4. The backend automatically initializes headers, sanitizes student inputs, escapes CSV formula injections, and appends rows.

---

## 4. Continuous Integration & Quality Assurance

Automated quality control is executed on every GitHub commit via `.github/workflows/ci-cd.yml`:

```bash
# Execute local unit test suite
python -m unittest discover -s tests

# Execute HTML template validation
npx htmlhint "**/*.html" --config .htmlhintrc

# Execute Flake8 syntax checks
flake8 . --count --select=E9,F63,F7,F82
```

Always ensure local tests pass before merging pull requests into `main`.

---

## Intellectual Property & License

Copyright (c) 2026 Coding & AI Club, NIT Mizoram. **All Rights Reserved.**
