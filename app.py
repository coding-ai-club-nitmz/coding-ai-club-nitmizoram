# Copyright (c) 2026 Coding & AI Club, NIT Mizoram. All Rights Reserved.
import socket

# --- IPv4 Workaround for College Network Timeout Issues ---
# Forces Python to use IPv4 instead of IPv6 to prevent Google API timeouts
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [res for res in responses if res[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

from flask import Flask, render_template, send_from_directory, request
import os
import importlib
import time
import data
import threading
from dotenv import load_dotenv
from google_sheets import background_sync_worker

# Load environment variables
load_dotenv()


template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)

# Initialize data modification time tracker
last_data_mtime = os.path.getmtime(os.path.join(app.root_path, 'data.py'))

@app.before_request
def reload_data_if_modified():
    global last_data_mtime
    try:
        data_path = os.path.join(app.root_path, 'data.py')
        mtime = os.path.getmtime(data_path)
        if mtime != last_data_mtime:
            importlib.reload(data)
            last_data_mtime = mtime
            time_diff = time.time() - mtime
            threshold = data.SYSTEM_CONFIG.get("data_reload_threshold_seconds", 180)
            was_updated_in_last_threshold = time_diff < threshold
            print(f"data.py reloaded dynamically! Updated in last {threshold}s: {was_updated_in_last_threshold}")
    except Exception as e:
        print(f"Failed to dynamically reload data.py: {e}")

# Context processor makes 'global_data' available in every template
@app.context_processor
def inject_global_data():
    return dict(global_data=data.GLOBAL_DATA)

# Configure caching based on request type: prevent caching for dynamic templates in development, but cache in production
@app.after_request
def add_header(response):
    # Check if the request is for a static asset
    is_static = (
        request.endpoint == 'static' or 
        request.path.startswith('/static/') or 
        request.path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.woff', '.woff2', '.ttf'))
    )
    
    # Check if running in production on Vercel
    is_vercel = os.environ.get('VERCEL') == '1'
    
    if is_static:
        # Cache static files in the browser (configured in data.py)
        # "must-revalidate" combined with a max-age tells the browser to cache files locally.
        cache_age = data.SYSTEM_CONFIG.get("static_cache_max_age", 180)
        response.headers["Cache-Control"] = f"public, max-age={cache_age}, must-revalidate"
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
    featured_notices = [n for n in data.ANNOUNCEMENTS if n.get('featured')]
    return render_template('index.html', stats=data.STATS_DATA, notices=featured_notices, home=data.HOME_DATA)

@app.route('/notices')
def notices():
    return render_template('notices.html', notices=data.ANNOUNCEMENTS)

@app.route('/notices/<id>')
def notice_detail(id):
    notice = next((n for n in data.ANNOUNCEMENTS if n['id'] == id), None)
    if notice:
        return render_template('notice_detail.html', notice=notice)
    return render_template('404.html'), 404

@app.route('/about')
def about():
    return render_template('about.html', about=data.ABOUT_DATA)

@app.route('/events')
def events():
    return render_template('events.html', events=data.EVENT_DATA)

@app.route('/teams')
def teams():
    return render_template('teams.html', 
                           mentors=data.TEAM_DATA['mentors'], 
                           guiders=data.TEAM_DATA['guiders'], 
                           core=data.TEAM_DATA['core'])

@app.route('/credits')
def credits():
    return render_template('credits.html', 
                           web_team=data.TEAM_DATA['web_team'], 
                           volunteers=data.TEAM_DATA['volunteers'])

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=data.PROJECT_DATA)

@app.route('/resources')
def resources():
    return render_template('resources.html', resources=data.RESOURCE_DATA)

@app.route('/contact')
def contact():
    return render_template('contact.html', contact=data.CONTACT_PAGE_DATA)

@app.route('/join')
def join():
    return render_template('join.html', join_data=data.JOIN_PAGE_DATA)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').upper()
        roll = request.form.get('roll', '').upper()
        email = request.form.get('email', '').lower()
        
        # Format phone number
        phone = request.form.get('phone', '')
        import re
        phone = re.sub(r'\D', '', phone)
        if len(phone) >= 12 and phone.startswith('91'):
            phone = phone[2:]
        elif len(phone) >= 11 and phone.startswith('0'):
            phone = phone[1:]
        phone = phone[:10]
        
        branch = request.form.get('branch', '').upper()
        degree = request.form.get('degree', '').upper()
        year = request.form.get('year', '').upper()
        event_name = request.form.get('eventName', '') # Don't uppercase event name because it's used for file matching
        skills = request.form.get('skills', '').upper()
        
        # Capture the user's IP Address (handles Vercel/Cloudflare proxies too)
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_address:
            ip_address = ip_address.split(',')[0].strip()
        
        # Log complete candidate details locally as an immutable backup log
        app.logger.info(
            f"EVENT REGISTRATION BACKUP: name={name}, roll={roll}, email={email}, "
            f"phone={phone}, branch={branch}, degree={degree}, year={year}, "
            f"event={event_name}, skills={skills}, ip={ip_address}"
        )
        
        # Synchronous Google Sheets sync (Safe for Vercel/Serverless)
        res = background_sync_worker(name, roll, email, phone, branch, degree, year, event_name, skills, ip_address)
        
        if res and res.get("status") == "duplicate":
            return render_template('register_duplicate.html', name=name, event_name=event_name)
            
        return render_template('register_success.html', name=name, event_name=event_name)
    
    return render_template('register.html', events=data.EVENT_DATA)




@app.route('/robots.txt')
def robots():
    return send_from_directory(app.root_path, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.root_path, 'sitemap.xml')

# Fallback for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Using 0.0.0.0 makes it reachable from Docker/Vercel environments
    app.run(host='0.0.0.0', port=8000, debug=False)
