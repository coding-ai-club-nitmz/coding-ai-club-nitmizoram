from flask import Flask, render_template, send_from_directory
import os
from data import TEAM_DATA, PROJECT_DATA, EVENT_DATA, RESOURCE_DATA, STATS_DATA, GLOBAL_DATA, ANNOUNCEMENTS, ABOUT_DATA, CONTACT_PAGE_DATA, HOME_DATA

app = Flask(__name__, static_folder='.', static_url_path='', template_folder='templates')

# Context processor makes 'global_data' available in every template
@app.context_processor
def inject_global_data():
    return dict(global_data=GLOBAL_DATA)

# Force browser to reload all templates/assets without caching during development
@app.after_request
def add_header(response):
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
