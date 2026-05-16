#  Coding & AI Club Website — NIT Mizoram

Welcome to the official portal of the **Coding & AI Club** at the **National Institute of Technology Mizoram (राष्ट्रीय प्रौद्योगिकी संस्थान, मिज़ोरम)**. 

This website serves as a modern, high-performance, and responsive hub to showcase club innovations, core values, announcements, active members, resources, and technical projects.

---

##  Key Features

*   **100% Data-Driven Architecture**: Managed entirely via central data structures. Zero HTML knowledge required to update the site.
*   **Dynamic Notice Board**: A custom horizontal slider showcasing the 3 latest announcements side-by-side with smooth horizontal scrolling for more. Includes context-aware `/notices/<id>` detail routing.
*   **Context-Aware Communication**: Smart `mailto:` links that auto-inject formalized subject lines depending on the specific notice or card clicked.
*   **Premium Visual Experience**: Harmony of HSL primary-navy and modern typography with absolute responsiveness on all device viewports.
*   **Production & SEO Optimized**: Features high-fidelity dynamic Open Graph previews, custom dynamic meta tags for search engine bots, and valid `sitemap.xml` & `robots.txt` configurations.

---

## ️ Technology Stack

*   **Backend**: Python / Flask (3.0+)
*   **Frontend**: Vanilla HTML5, CSS3, Jinja2 template engine
*   **Dev Server**: Werkzeug / Gunicorn
*   **Deployment Support**: Pre-configured for Vercel and Render (with `Procfile` and `vercel.json`)

---

##  Quick Start & Local Development

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/coding-ai-club-nitmz/website.git
cd website

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
├── app.py              # Main Flask application (Route definitions & Context processors)
├── data.py             # Central Data Store (Single source of truth for all content)
├── style.css           # Global CSS variables, layouts, and responsive media queries
├── templates/          # Jinja2 HTML Templates
│   ├── base.html       # Shell structure, dynamic SEO headers, Navbar, and Footer
│   ├── index.html      # Homepage (Centered welcome & Horizontal Notice Board)
│   ├── about.html      # Mission, Scope, and Core Values
│   ├── events.html     # Gallery of Club Hackathons & Quizzes
│   ├── teams.html      # Members, Mentors, and Faculty profiles
│   ├── projects.html   # Innovations showcase & Interactive contribution page
│   ├── notices.html    # Notice Board List view
│   ├── notice_detail.html # Single Notice Deep-Link detail page
│   └── contact.html    # Connect cards & NIT physical address
├── images/             # Static logos, avatars, and event graphics
├── robots.txt          # SEO Crawling rules
└── sitemap.xml         # SEO search index paths
```

---

##  Deployment

The repository is pre-configured for rapid production deployment:
*   **Vercel**: Simply connect the repository to Vercel. The `vercel.json` configuration handles serverless routing automatically.
*   **Render / Heroku**: Uses the pre-configured `Procfile` to run a production-grade WSGI server via `gunicorn` with high-concurrency workers.

---

##  License
This project is built and maintained by the **Coding & AI Club Web Team, NIT Mizoram**. All rights reserved.
