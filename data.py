# This file contains all the content for the website.
# Future teams can simply edit these lists to add/update/delete items.

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

# Announcements / Notice Board
# To show a notice on the home page, set 'featured': True
ANNOUNCEMENTS = [
    {
        "id": "core-team-recruitment",
        "featured": True,
        "title": "Core Team Recruitment 2026",
        "date": "May 16, 2026",
        "summary": "We are currently recruiting for core team positions. Mail us to apply!",
        "content": "The Coding & AI Club is officially recruiting for various Core Team positions for the academic session 2026-27. If you are passionate about software engineering, artificial intelligence, event management, design, or content creation, this is your chance to lead and shape the club's future! To apply, click the button below to mail us directly with your details. If selected, we will contact you for a brief interaction.",
        "link": "mailto:coding.club@nitmz.ac.in",
        "link_text": "Join Us"
    },
    {
        "id": "hackathon-closed",
        "featured": True,
        "title": "24 Hours Hackathon Closed!",
        "date": "May 15, 2026",
        "summary": "The hackathon has officially concluded. Final results have been sent to student emails.",
        "content": "The annual 24 Hours Hackathon has successfully concluded! We witnessed outstanding project prototypes built in just a single day. The evaluation phase is now complete, and the official results and feedback have been dispatched directly to the registered email addresses of all student participants. Thank you to all the mentors, judges, and teams for making this event a spectacular success!",
        "link": None,
        "link_text": ""
    },
    {
        "id": "upcoming-projects",
        "featured": True,
        "title": "New Projects Starting Soon!",
        "date": "May 18, 2026",
        "summary": "Innovative projects are kicking off. Share your ideas with us!",
        "content": "Several major club projects are set to start soon across web platforms and machine learning fields. If you have an exciting, innovative idea that you want to lead or collaborate on, we would love to hear it! Bring your technical concepts to our next session or click the button below to mail us your proposal directly.",
        "link": "mailto:coding.club@nitmz.ac.in",
        "link_text": "Propose an Idea"
    }
]

TEAM_DATA = {
    "mentors": [
        {"name": "Dr. Suakanta Roy", "role": "Faculty Mentor", "badge": "Faculty", "image": "https://ui-avatars.com/api/?name=S&background=random&color=fff&size=200"},
        {"name": "Mr. Bishal Sinha", "role": "PhD Mentor", "badge": "Research", "image": "https://ui-avatars.com/api/?name=B&background=random&color=fff&size=200"}
    ],
    "guiders": [
        {"name": "Tanmay Kumar", "role": "Guider", "badge": "Guider", "image": "https://ui-avatars.com/api/?name=T&background=random&color=fff&size=200"},
        {"name": "Suman Singh", "role": "Guider", "badge": "Guider", "image": "images/suman.jpg"},
        {"name": "Pragya Tripathi", "role": "Guider", "badge": "Guider", "image": "images/pragya.jpg"},
        {"name": "Khush Katariya", "role": "Guider", "badge": "Guider", "image": "https://ui-avatars.com/api/?name=K&background=random&color=fff&size=200"}
    ],
    "core": [
        {"name": "Rishabh Shukla", "role": "Club President", "badge": "President", "image": "https://ui-avatars.com/api/?name=R&background=random&color=fff&size=200"},
        {"name": "Routhu Deva Varshini", "role": "Vice President", "badge": "VP", "image": "images/varshini.jpg"},
        {"name": "Mahak Singh", "role": "Event Manager", "badge": "Events", "image": "images/mahak.jpg"},
        {"name": "Ritika Kumari", "role": "Membership Chair", "badge": "Membership", "image": "images/ritika.jpg"},
        {"name": "Vivek Kumar", "role": "Coordinator", "badge": "Coord.", "image": "images/vivek.jpg"}
    ],
    "web_team": [
        {"name": "Dilip Sahu", "role": "Team Head", "badge": "Web Team", "image": "images/dilip.jpg"},
        {"name": "Chandan Kumar", "role": "Developer", "badge": "Web Team", "image": "images/chandan.jpg"},
        {"name": "Aditya Kumar", "role": "Designer", "badge": "Web Team", "image": "images/aditya.jpg"},
        {"name": "V. Vyshnavi", "role": "Content Creator", "badge": "Web Team", "image": "images/vyshnavi.jpg"}
    ],
    "volunteers": [
        {"name": "Aditya Kumar Ranjan", "role": "Design Support", "badge": "Contributor", "image": "https://ui-avatars.com/api/?name=A&background=random&color=fff&size=200"},
        {"name": "Vivek Kumar", "role": "Design Support", "badge": "Contributor", "image": "images/vivek.jpg"},
        {"name": "Bijjla Thanmai", "role": "Design Support", "badge": "Contributor", "image": "https://ui-avatars.com/api/?name=B&background=random&color=fff&size=200"}
    ]
}

PROJECT_DATA = {
    "intro": "Exploring real-world solutions through technology.",
    "featured": [
        {
            "title": "Official Club Website",
            "desc": "The very website you are browsing! Designed and built from scratch by the Web Team to showcase our club's members, events, and projects.",
            "github": "https://github.com/coding-ai-club-nitmz",
            "live": "/"
        }
    ],
    "contribution": {
        "title": "Want to Contribute?",
        "desc": "Club members actively collaborate on these projects. Join a team, propose an idea, or contribute code.",
        "options": [
            {
                "title": "Propose an Idea",
                "desc": "Have a project concept? Bring it to our next session."
            },
            {
                "title": "Join a Team",
                "desc": "Ongoing projects always welcome new contributors."
            }
        ]
    }
}

EVENT_DATA = [
    {"title": "Samyuga - Prarambh", "desc": "The coding contest initiation designed to test your algorithmic thinking and speed.", "image": "images/events/prarambh.jpg"},
    {"title": "Samyuga - Trishul", "desc": "Advanced competitive programming challenges for the sharpest coders.", "image": "images/events/trishul.jpg"},
    {"title": "Chakravyuh AI Quiz", "desc": "Test your knowledge of Machine Learning, Deep Learning, and AI history.", "image": "images/events/chakravyuh.jpg"},
    {"title": "24 Hours Hackathon", "desc": "Build real-world solutions and innovative prototypes overnight.", "image": "images/events/hackathon.jpg"}
]

RESOURCE_DATA = [
    {"title": "Machine Learning Guide", "desc": "Our comprehensive introductory PDF guide for beginners starting with Python and ML models.", "tag": "Documentation", "link": "https://github.com/coding-ai-club-nitmz"},
    {"title": "Web Dev Roadmap", "desc": "A step-by-step checklist and resource collection for mastering frontend and backend development.", "tag": "Roadmap", "link": "https://github.com/coding-ai-club-nitmz"},
    {"title": "Tech Fest Rulebooks", "desc": "Official guidelines, problem statements, and judging criteria for upcoming hackathons.", "tag": "Competition", "link": "https://github.com/coding-ai-club-nitmz"}
]

STATS_DATA = [
    {"num": "30+", "label": "Active Members"},
    {"num": "1+", "label": "Projects Launched"},
    {"num": "5+", "label": "Events Hosted"},
    {"num": "2025", "label": "Est."}
]

ABOUT_DATA = {
    "intro": "We are a student-driven community focused on engineering real-world software, exploring the depths of artificial intelligence, and maintaining professional development standards.",
    "mission_cards": [
        {"title": "Our Mission", "content": "To cultivate a culture of innovation, practical learning, and collaborative engineering among students."},
        {"title": "Our Scope", "content": "From AI research to IoT hardware — we work across the full spectrum of modern technology."},
        {"title": "Our Community", "content": "Open to all students who want to build, learn, and grow together."}
    ],
    "core_values": [
        {"title": "Build", "content": "Ship real projects that solve real problems — not just theory.", "tag": "Engineering Mindset"},
        {"title": "Learn", "content": "Workshops, bootcamps, and peer-led sessions that grow your skills fast.", "tag": "Continuous Growth"},
        {"title": "Launch", "content": "Represent at hackathons, competitions, and technical fests.", "tag": "Compete & Win"}
    ]
}
CONTACT_PAGE_DATA = {
    "intro": "Follow our journey and reach out for collaborations, queries, or just to say hello.",
    "cards": [
        {
            "title": "Email Us",
            "desc": "Drop us a message for collaborations or queries.",
            "link_text": "coding.club@nitmz.ac.in",
            "link_type": "email"
        },
        {
            "title": "Instagram",
            "desc": "Stay updated with events, achievements, and behind-the-scenes.",
            "link_text": "@codingclub_nitmz",
            "link_type": "instagram"
        },
        {
            "title": "LinkedIn",
            "desc": "Connect professionally and follow our project updates.",
            "link_text": "Coding & AI Club",
            "link_type": "linkedin"
        }
    ],
    "address": {
        "title": "Find Us",
        "name": "Coding & AI Club",
        "institute": "National Institute of Technology Mizoram",
        "location": "Chaltlang, Aizawl — 796012, Mizoram, India"
    }
}

HOME_DATA = {
    "welcome_title": "Welcome to the Club",
    "welcome_desc": "The official home of the Coding & AI Club — a student-driven community building real-world technology at NIT Mizoram.",
    "banner_text": "Grow Together and Learn Together",
    "hero_desc": "We focus on practical engineering, collaborative projects, and peer-to-peer learning. Join us to turn your ideas into functional software."
}
