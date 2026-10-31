# Copyright (c) 2026 Coding & AI Club, NIT Mizoram. All Rights Reserved.
import socket

# --- IPv4 Workaround for College Network Timeout Issues ---
# Forces Python to use IPv4 instead of IPv6 to prevent Google API timeouts
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [res for res in responses if res[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

from flask import Flask, render_template, send_from_directory, request, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os
import importlib
import time
import re
import data
import threading
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from google_sheets import background_sync_worker

# IST Timezone Helper (NIT Mizoram is in IST, while Vercel servers run in UTC)
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST).replace(tzinfo=None)

def get_client_ip():
    """Extracts and validates client IP address, guarding against header injection attacks."""
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip:
        ip = ip.split(',')[0].strip()
        if not re.match(r'^[0-9a-fA-F:.]+$', ip):
            ip = request.remote_addr or 'unknown'
    return ip or 'unknown'

# Load environment variables
load_dotenv()


template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

# Initialize Security Headers (Talisman)
csp = {
    'default-src': ["'self'"],
    'script-src': ["'self'", "'unsafe-inline'"],
    'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
    'font-src': ["'self'", "https://fonts.gstatic.com"],
    'img-src': ["'self'", "data:", "https://ui-avatars.com"]
}
talisman = Talisman(app, content_security_policy=csp, force_https=False)

# Initialize Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://"
)

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
    return dict(global_data=data.GLOBAL_DATA, common_dropdowns=data.COMMON_DROPDOWNS, stats_data=data.STATS_DATA, now=get_ist_now())

# Configure caching based on request type: prevent caching for dynamic templates in development, but cache in production
@app.after_request
def add_header(response):
    # Dynamic and time-sensitive routes must never be cached by CDN or browser
    is_dynamic = (
        request.path == '/attendance' or 
        request.path.startswith('/apply/') or 
        request.path.startswith('/register')
    )
    
    # Check if the request is for a static asset
    is_static = (
        request.endpoint == 'static' or 
        request.path.startswith('/static/') or 
        request.path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.woff', '.woff2', '.ttf'))
    )
    
    # Check if running in production on Vercel
    is_vercel = os.environ.get('VERCEL') == '1'
    
    if is_dynamic:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    elif is_static:
        # Cache static files in the browser (configured in data.py)
        cache_age = data.SYSTEM_CONFIG.get("static_cache_max_age", 180)
        response.headers["Cache-Control"] = f"public, max-age={cache_age}, must-revalidate"
        response.headers.pop("Pragma", None)
        response.headers.pop("Expires", None)
    elif is_vercel:
        # In production on Vercel, cache static informational HTML pages at Vercel's global CDN Edge
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
    return render_template('index.html', notices=featured_notices, home=data.HOME_DATA)

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
                           mentors=data.TEAM_DATA.get('mentors', []), 
                           founding=data.TEAM_DATA.get('founding', []),
                           core=data.TEAM_DATA.get('core', []),
                           coordinators=data.TEAM_DATA.get('coordinators', []))

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=data.PROJECT_DATA)

@app.route('/resources')
def resources():
    return render_template('resources.html', resources=data.RESOURCE_DATA)

@app.route('/collaborate')
def collaborate():
    return render_template('collaborate.html', collaborate=data.COLLABORATE_DATA)

@app.route('/contact')
def contact():
    return render_template('contact.html', contact=data.CONTACT_PAGE_DATA)

@app.route('/join')
def join():
    return render_template('join.html', join_data=data.JOIN_PAGE_DATA)

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute", error_message="You are submitting too fast. Please wait a minute before trying again.")
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').upper()
        roll = request.form.get('roll', '').upper()
        email = request.form.get('email', '').lower()
        
        # Format phone number
        phone = request.form.get('phone', '')
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
        
        if not name or not roll or not email or not phone:
            return render_template('register_error.html', name=name, event_name=event_name, error_msg="Missing required fields. Please fill out the form completely.")
        
        # Capture the user's IP Address (handles Vercel/Cloudflare proxies too)
        ip_address = get_client_ip()
        
        # Log complete candidate details locally as an immutable backup log
        app.logger.info(
            f"EVENT REGISTRATION BACKUP: name={name}, roll={roll}, email={email}, "
            f"phone={phone}, branch={branch}, degree={degree}, year={year}, "
            f"event={event_name}, skills={skills}, ip={ip_address}"
        )
        
        res = background_sync_worker(name, roll, email, phone, branch, degree, year, event_name, skills, ip_address)
        
        event_data = next((e for e in data.EVENT_DATA if e['title'] == event_name), {})
        whatsapp_link = event_data.get('whatsapp_group_link')
        whatsapp_text = event_data.get('whatsapp_group_text', 'Join Whatsapp Group')
        
        if res and res.get("status") == "success":
            return render_template('register_success.html', name=name, event_name=event_name, whatsapp_link=whatsapp_link, whatsapp_text=whatsapp_text)
        elif res and res.get("status") == "duplicate":
            return render_template('register_duplicate.html', name=name, event_name=event_name)
        else:
            error_msg = res.get("message", "A network or server error occurred.") if res else "A network or server error occurred."
            return render_template('register_error.html', name=name, event_name=event_name, error_msg=error_msg)
    
    return render_template('register.html', events=data.EVENT_DATA)

def process_team_registration(request, event_title):
    if request.method == 'POST':
        ip_address = get_client_ip()
        
        team_name = request.form.get('team_name', '').upper()
        track = request.form.get('track', '')
        
        l_name = request.form.get('l_name', '').upper()
        l_roll = request.form.get('l_roll', '').upper()
        l_email = request.form.get('l_email', '').lower()
        
        if not team_name or not l_name or not l_roll or not l_email:
            return render_template('register_error.html', name=l_name, event_name=event_title, error_msg="Missing required fields for the Team Leader. Please fill out the form completely.")
        
        l_phone = request.form.get('l_phone', '')
        l_phone = re.sub(r'\D', '', l_phone)
        if len(l_phone) >= 12 and l_phone.startswith('91'): l_phone = l_phone[2:]
        elif len(l_phone) >= 11 and l_phone.startswith('0'): l_phone = l_phone[1:]
        l_phone = l_phone[:10]
        
        m2_name = request.form.get('m2_name', '').upper()
        m2_roll = request.form.get('m2_roll', '').upper()
        m2_email = request.form.get('m2_email', '').lower()
        
        m3_name = request.form.get('m3_name', '').upper()
        m3_roll = request.form.get('m3_roll', '').upper()
        m3_email = request.form.get('m3_email', '').lower()
        
        m4_name = request.form.get('m4_name', '').upper()
        m4_roll = request.form.get('m4_roll', '').upper()
        m4_email = request.form.get('m4_email', '').lower()

        # Check for duplicate roll numbers within the submitted team
        team_rolls = [r for r in [l_roll, m2_roll, m3_roll, m4_roll] if r.strip()]
        if len(team_rolls) != len(set(team_rolls)):
            return render_template('register_error.html', name=l_name, event_name=event_title, error_msg="Duplicate roll numbers found within the team. Each member must have a unique enrollment number.")

        # Import locally to avoid circular dependency issues at top level
        from google_sheets import background_sync_team_worker
        
        res = background_sync_team_worker(
            ip_address, event_title, team_name, track, 
            l_name, l_roll, l_email, l_phone, 
            m2_name, m2_roll, m2_email, 
            m3_name, m3_roll, m3_email, 
            m4_name, m4_roll, m4_email
        )
        
        if res and res.get("status") == "success":
            return render_template('register_success.html', name=l_name, event_name=event_title)
        elif res and res.get("status") == "duplicate":
            return render_template('register_duplicate.html', name=l_name, event_name=event_title, duplicate_msg=res.get("message"))
        else:
            error_msg = res.get("message", "A network or server error occurred.") if res else "A network or server error occurred."
            return render_template('register_error.html', name=l_name, event_name=event_title, error_msg=error_msg)

@app.route('/register/<event_id>', methods=['GET', 'POST'])
@limiter.limit("5 per minute", error_message="You are submitting too fast. Please wait a minute before trying again.")
def register_team_event(event_id):
    team_event = data.TEAM_EVENTS.get(event_id)
    if not team_event:
        return render_template('404.html'), 404
        
    event_title = team_event["title"]
    form_type = team_event["form_type"]
    
    if request.method == 'POST':
        return process_team_registration(request, event_title)
        
    return render_template('register_team.html', form_type=form_type, event_title=event_title, submit_url=f'/register/{event_id}')

@app.route('/apply/<form_id>', methods=['GET', 'POST'])
@limiter.limit("5 per minute", error_message="You are submitting too fast. Please wait a minute before trying again.")
def apply_form(form_id):
    form_data = data.DYNAMIC_FORMS.get(form_id)
    if not form_data:
        return render_template('404.html'), 404
    
    # Check registration deadline
    deadline_str = form_data.get('registration_deadline')
    if deadline_str:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
        if get_ist_now() > deadline:
            return render_template('register_error.html', name="User", event_name=form_data['title'], error_msg="Registration for this event has closed. The deadline was " + deadline.strftime("%d %b %Y, %I:%M %p") + ".")
        
    redirect_url = form_data.get('redirect_url')
    if redirect_url:
        return redirect(redirect_url, code=302)

    if request.method == 'POST':
        import re
        submission = {}
        for field in form_data['fields']:
            base_name = field.replace('-comp', '')
            safe_name = base_name.lower().replace(' ', '_').replace('?', '').replace('-', '_').replace('&', 'and').replace('/', '_')
            submission[base_name] = request.form.get(safe_name, '')
            
        ip_address = get_client_ip()
            
        from google_sheets import background_dynamic_sync_worker
        res = background_dynamic_sync_worker(form_id, form_data, submission, ip_address)
        
        # Try to find a name field to display in the success page
        name_val = "User"
        for key in submission:
            if 'name' in key.lower():
                name_val = submission[key]
                break
        if name_val == "User" and submission:
            name_val = list(submission.values())[0]
            
        event_name = form_data['title']
        
        whatsapp_link = form_data.get('whatsapp_group_link')
        whatsapp_text = form_data.get('whatsapp_group_text', 'Join Whatsapp Group')
        
        if res and res.get("status") == "success":
            return render_template('register_success.html', name=name_val, event_name=event_name, whatsapp_link=whatsapp_link, whatsapp_text=whatsapp_text)
        elif res and res.get("status") == "duplicate":
            duplicate_msg = res.get("message", "You have already registered.")
            return render_template('register_duplicate.html', name=name_val, event_name=event_name, duplicate_msg=duplicate_msg)
        else:
            error_msg = res.get("message", "A network or server error occurred.") if res else "A network or server error occurred."
            return render_template('register_error.html', name=name_val, event_name=event_name, error_msg=error_msg)
            
    return render_template('dynamic_form.html', form_id=form_id, form_data=form_data)





@app.route('/attendance', methods=['GET', 'POST'])
@limiter.limit("10 per minute", error_message="You are submitting too fast. Please wait a minute before trying again.")
def attendance():
    att_config = data.ATTENDANCE_CONFIG
    
    # Check time window using Indian Standard Time (IST)
    now = get_ist_now()
    start_str = att_config.get('start_time')
    end_str = att_config.get('end_time')
    
    time_open = True
    if start_str and end_str:
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
        if now < start_time or now > end_time:
            time_open = False
    
    if request.method == 'POST' and time_open:
        roll = request.form.get('roll', '').strip().upper()
        
        if not roll:
            return render_template('attendance.html', att_config=att_config, time_open=time_open, error="Please enter your Roll Number.")
        
        from google_sheets import background_attendance_worker
        res = background_attendance_worker(roll, att_config)
        
        if res and res["status"] == "success":
            return render_template('attendance.html', att_config=att_config, time_open=time_open, success=True, student_name=res.get("name", roll))
        elif res and res["status"] == "already_marked":
            return render_template('attendance.html', att_config=att_config, time_open=time_open, already_marked=True, student_name=res.get("name", roll))
        elif res and res["status"] == "not_registered":
            return render_template('attendance.html', att_config=att_config, time_open=time_open, not_registered=True)
        else:
            error_msg = res.get("message", "An unexpected error occurred.") if res else "An unexpected error occurred."
            return render_template('attendance.html', att_config=att_config, time_open=time_open, error=error_msg)
    
    return render_template('attendance.html', att_config=att_config, time_open=time_open)


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
