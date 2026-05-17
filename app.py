from flask import Flask, render_template, send_from_directory, request
import os
from data import TEAM_DATA, PROJECT_DATA, EVENT_DATA, RESOURCE_DATA, STATS_DATA, GLOBAL_DATA, ANNOUNCEMENTS, ABOUT_DATA, CONTACT_PAGE_DATA, HOME_DATA
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
print("DIAGNOSTIC - templates contents:", os.listdir(template_dir))
app = Flask(__name__, static_folder=static_dir, static_url_path='', template_folder=template_dir)

# Context processor makes 'global_data' available in every template
@app.context_processor
def inject_global_data():
    return dict(global_data=GLOBAL_DATA)

# Configure caching based on request type: prevent caching for dynamic templates in development, but cache in production
@app.after_request
def add_header(response):
    # Check if the request is for a static asset
    is_static = (
        request.endpoint == 'static' or 
        request.path.startswith('/images/') or 
        request.path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.woff', '.woff2', '.ttf'))
    )
    
    # Check if running in production on Vercel
    is_vercel = os.environ.get('VERCEL') == '1'
    
    if is_static:
        # Cache static files in the browser for both local and production (24 hours)
        # "must-revalidate" combined with a max-age tells the browser to cache files locally.
        response.headers["Cache-Control"] = "public, max-age=86400, must-revalidate"
        response.headers.pop("Pragma", None)
        response.headers.pop("Expires", None)
    elif is_vercel:
        # In production on Vercel, cache HTML pages at Vercel's global CDN Edge permanently (until next deployment).
        # We tell the browser to cache pages locally for 5 minutes (max-age=300) to prevent log spam from prefetch hovers.
        # The CDN serves the cached page instantly (s-maxage=31536000) and revalidates in the background (stale-while-revalidate=60).
        # This reduces loading time from 300ms/100ms down to 10-20ms (CDN speed) globally!
        response.headers["Cache-Control"] = "public, max-age=300, s-maxage=31536000, stale-while-revalidate=60"
        response.headers.pop("Pragma", None)
        response.headers.pop("Expires", None)
    else:
        # During local development, force browser to reload dynamic templates without caching
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

@app.route('/')
def index():
    # Only show 'featured' notices on the home page
    featured_notices = [n for n in ANNOUNCEMENTS if n.get('featured')]
    return render_template('index.html', stats=STATS_DATA, notices=featured_notices, home=HOME_DATA)

@app.route('/notices')
def notices():
    return render_template('notices.html', notices=ANNOUNCEMENTS)

@app.route('/notices/<id>')
def notice_detail(id):
    notice = next((n for n in ANNOUNCEMENTS if n['id'] == id), None)
    if notice:
        return render_template('notice_detail.html', notice=notice)
    return render_template('404.html'), 404

@app.route('/about')
def about():
    return render_template('about.html', about=ABOUT_DATA)

@app.route('/events')
def events():
    return render_template('events.html', events=EVENT_DATA)

@app.route('/teams')
def teams():
    return render_template('teams.html', 
                           mentors=TEAM_DATA['mentors'], 
                           guiders=TEAM_DATA['guiders'], 
                           core=TEAM_DATA['core'])

@app.route('/credits')
def credits():
    return render_template('credits.html', 
                           web_team=TEAM_DATA['web_team'], 
                           volunteers=TEAM_DATA['volunteers'])

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECT_DATA)

@app.route('/resources')
def resources():
    return render_template('resources.html', resources=RESOURCE_DATA)

@app.route('/contact')
def contact():
    return render_template('contact.html', contact=CONTACT_PAGE_DATA)

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/diagnostic')
def diagnostic():
    try:
        files = os.listdir(template_dir)
        return {
            "template_dir": template_dir,
            "exists": os.path.exists(template_dir),
            "files": files
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

# Fallback for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Using 0.0.0.0 makes it reachable from Docker/Vercel environments
    app.run(host='0.0.0.0', port=8000, debug=False)
