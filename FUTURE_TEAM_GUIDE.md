#  Future Web Team Guide — Coding & AI Club

Hey there, future Web Team!  Welcome to the maintenance and development manual for the **Coding & AI Club NIT Mizoram** website. 

This guide describes how the website functions, how to make instant content updates, and the design tokens you must follow to keep the site looking premium.

---

##  The Single Source of Truth: `data.py`

To update almost *anything* on the website (text, images, links, announcements, or team members), **you do not need to edit any HTML files**. Simply modify [data.py](./data.py).

Here is a breakdown of the key data structures in `data.py`:

### 1. Club Global Meta (`GLOBAL_DATA`)
Controls the official club name, tagline, Hindi institute tagline, copyright, and global social media URLs.
```python
GLOBAL_DATA = {
    "club_name": "Coding & AI Club",
    "tagline": "Code . Create . Collaborate",
    "hindi_name": "राष्ट्रीय प्रौद्योगिकी संस्थान, मिज़ोरम",
    "copyright": " 2026 Coding & AI Club",
    "social": {
        "email": "coding.club@nitmz.ac.in",
        "instagram": "https://www.instagram.com/codingclub_nitmz",
        "linkedin": "https://www.linkedin.com/company/coding-club-nit-mizoram/"
    }
}
```

### 2. Notices & Announcements (`ANNOUNCEMENTS`)
A list of notice dictionaries. 
*   **To display a notice on the Home Page**: Set `"featured": True`.
*   **To link a button**: Set `"link"` to a path (e.g. `"/events"`, `"/join"`).
*   **To prefill the Join/Inquiry form**: Include a `"prefill"` object containing `"topic"` and `"message"`.
*   **No link action needed**: Set `"link": None`.

```python
{
    "id": "core-team-recruitment",
    "featured": True,
    "title": "Core Team Recruitment 2026",
    "date": "May 16, 2026",
    "summary": "We are currently recruiting for core team positions. Apply now!",
    "content": "Full description of the recruitment drive goes here...",
    "link": "/join",
    "prefill": {
        "topic": "Core Team Application - Coding & AI Club",
        "message": "Hello Coding & AI Club,\n\nI want to apply for the Core Team position. Here are my details..."
    },
    "link_text": "Join Us"
}
```

### 3. Core Team & Members (`TEAM_DATA`)
Organized by category lists (`mentors`, `guiders`, `core`, `web_team`, `volunteers`). To add a member, append a new dictionary:
```python
{"name": "Alice Smith", "role": "Developer", "badge": "Core", "image": "images/alice.jpg"}
```
> [!NOTE]  
> Store all member photographs in `static/images/`. The templates will automatically resolve local paths relative to the static directory or keep external URLs as is.
> 
> [!TIP]  
> If a member's photograph is not ready or missing, the template will automatically fall back to initial letters from the UI Avatar service, or you can specify it directly: `"https://ui-avatars.com/api/?name=Alice+Smith&background=random&color=fff&size=200"`.

---

##  Design & CSS System

All design rules are centralized in [static/style.css](./static/style.css). To maintain the website's professional and cohesive aesthetic, **always use the predefined CSS variables**:

### Brand Color Tokens
*   `--primary`: `#0a1f44` (Deep Premium Navy)
*   `--secondary`: `#002d62` (Royal Accent)
*   `--accent`: `#8ab4f8` (High-visibility ice blue link/highlight)
*   `--bg-light`: `#f8fafd` (Soft canvas tint)

### Layout Rules
1.  **Notice Cards Grid (Homepage)**: Controlled by a responsive slider styling inside `index.html`. It limits desktop display to **exactly 3 cards in one row**. If there are more, it smoothly scrolls horizontally without wrapping.
2.  **Generic Cards (`.team-card`, `.event-card`)**:
    *   Titles (`h3`) should have `font-family: 'Rajdhani', sans-serif;` with a bold weight of `700`.
    *   Descriptions (`p`) should have a standard line-height of `1.5` and `margin-bottom: 10px` to maintain optimal text readability.

---

##  Professional Email Integration

To protect our official email against automated spam-bots, we direct users through the local `/join` form instead of rendering direct `mailto` links on card CTAs.

Once the user completes the pre-filled form on `/join` and clicks submit, the website constructs a professional `mailto` query string combining their inputs and redirects them to their mail client:
```javascript
window.location.href = `mailto:coding.club@nitmz.ac.in?subject=${encodeURIComponent(topic)}&body=${body}`;
```
This keeps spam harvesters from scraping the address directly while providing structured, context-aware emails for club organizers to easily filter and review!

---

##  Search Engine Optimization (SEO) & Open Graph

The base shell [templates/base.html](./templates/base.html) features dynamic metadata tags:
*   **Search Tags**: Every page inherits SEO tags (`meta name="description"`). For individual announcements, the template automatically injects the **Notice Summary** as the description tag, boosting Google search indexing relevance.
*   **Open Graph previews**: Pre-configured with Facebook, WhatsApp, and LinkedIn preview parameters. Sharing links on social media will automatically load the club logo, custom page title, and structured description.

---

##  Flask Development Server Operations

### Disabling Cache for Instant Updates
To prevent the browser from caching CSS/HTML modifications during local testing, we have added an `after_request` filter in `app.py`:
```python
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
```
This guarantees that **every refresh reflects your latest modifications instantly**.

### Adding a New Route
To create a new page:
1.  Add a route in [app.py](./app.py):
    ```python
    @app.route('/my-page')
    def my_page():
        return render_template('my_page.html')
    ```
2.  Create your new template inside `templates/my_page.html` by extending base:
    ```html
    {% extends "base.html" %}
    {% block title %}My New Page – {{ global_data.club_name }}{% endblock %}
    {% block content %}
        <section class="section">
            <h2>Welcome to my new page</h2>
        </section>
    {% endblock %}
    ```
3. Add the link in navigation header in `templates/base.html`.

---

##  Google Sheets Registration Backend

The website features a fully automated Google Sheets backend for live event registrations. 
When creating a new event, future teams **must** follow these steps:
1. Create a blank Google Sheet in the designated Club Google Drive folder.
2. Name the Sheet **exactly** matching the `event_name` value submitted in the frontend form.
3. The backend `google_sheets.py` script will automatically locate the sheet, format the headers, normalize the user data (capitalization, phone sanitization), and append the rows.
4. **Duplicate Prevention:** The backend automatically checks Column 4 (Roll Number) to prevent students from registering multiple times.

*Note: Never expose the `GOOGLE_CLIENT_EMAIL` or `GOOGLE_PRIVATE_KEY` in the public repository. Always use Vercel Environment Variables for production.*

---

### Automated GitHub CI Pipeline

To prevent broken or syntax-faulty code from being merged into production, we have set up an automated **GitHub Action workflow** located at `.github/workflows/ci.yml`.

Whenever code is pushed or a Pull Request is opened on `main` or `master` branches, the pipeline automatically:
1. Installs Python and dependencies.
2. Compiles `app.py` and `data.py` to ensure zero syntax errors.
3. Tests Flask application imports successfully.
4. Performs code style linting via `flake8`.

Always verify that the GitHub Actions run shows green checkmarks before merging any pull requests!

Good luck! Keep pushing the boundaries of code and creativity! 
