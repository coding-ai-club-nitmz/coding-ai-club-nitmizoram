# Copyright (c) 2026 Coding & AI Club, NIT Mizoram. All Rights Reserved.
# This file contains all the content for the website.
# Future teams can simply edit these lists to add/update/delete items.

SYSTEM_CONFIG = {
    "static_cache_max_age": 180,           # Max-age for static assets in seconds (3 minutes)
    "data_reload_threshold_seconds": 180,  # Threshold for reporting recent updates in seconds (3 minutes)
}

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
        "id": "inter-nit-code-wars",
        "featured": True,
        "title": "Inter NIT Code Wars",
        "date": "October 23, 2026",
        "summary": "Organized by AlgoZenith in collaboration with All 31 NITs of India. Coding & AI Club is the official Single Point of Contact (SPOC) for NIT Mizoram. Register by 27th Oct 6:00 PM to represent our campus!",
        "content": "<div class=\"notice-text-intro\"><div class=\"organizer-highlight\"><strong>Organized by:</strong> AlgoZenith | <strong>In Collaboration with:</strong> All 31 NITs of India | <strong>NIT Mizoram SPOC:</strong> Coding & AI Club, NIT Mizoram</div><p><strong>AlgoZenith</strong> is conducting its flagship Pan-India competitive programming contest — the <strong>Inter NIT Code Wars</strong>, where all 31 NITs go head-to-head on a single national leaderboard to settle which NIT has the strongest coding culture!</p><p><strong>Coding & AI Club, NIT Mizoram</strong> is the official <strong>Single Point of Contact (SPOC)</strong> representing NIT Mizoram for this edition. We are calling upon the sharpest coders from NIT Mizoram to step forward, compete, and represent our campus on the national leaderboard.</p><p><strong>Format & Level:</strong> Codeforces Div 2 level contest. Video recording of yourself and your screen (showing you typing) is mandatory during the contest.</p><p><strong>Contest Date:</strong> 27th October 2026 (Tuesday), 8:00 PM onwards.</p><p><strong>Registration Deadline:</strong> 27th October 2026, 6:00 PM.</p><p><strong>Prizes:</strong> To be announced soon by AlgoZenith.</p><p><strong>Single Point of Contact (Queries):</strong> Coding & AI Club, NIT Mizoram — <a href=\"mailto:coding.club@nitmz.ac.in\" style=\"color: var(--accent);\">coding.club@nitmz.ac.in</a></p><p>Register your details on the official Google Form linked below. The contest link, guidelines, and rules will be sent directly via email to registered candidates only.</p></div>",
        "registration_open": True,
        "registration_deadline": "2026-10-27 18:00:00",
        "event_name": "Inter NIT Code Wars",
        "link": "https://forms.gle/V2rUEiLrnKjvCPkJ7",
        "link_text": "Register on Google Form"
    },
    {
        "id": "ai-startup-challenge-2026",
        "featured": True,
        "title": "Innovaite 2026: Successfully Concluded!",
        "date": "August 26, 2026",
        "summary": "The Innovaite AI/ML and Idea Pitching competitions have successfully concluded.",
        "content": "<div class=\"notice-text-intro\"><div class=\"organizer-highlight\"><strong>Organizers:</strong> IIC NIT Mizoram | Coding & AI Club, NIT Mizoram | NMICPS Technology Innovation Hub on Autonomous Navigation (TiHAN) IIT Hyderabad.</div><p>The Innovaite AI & Startup Challenge has officially wrapped up! Thank you to all the participants who pushed the limits of Artificial Intelligence in our Idea Pitching and AI/ML competitions.</p></div>",
        "links": []
    },
#    {
#        "id": "technox-part-ii",
#        "featured": False,
#        "title": "Technox'2025-26 Part-II",
#        "date": "May 27, 2026",
#        "summary": "Registration is open for Technox Part-II events. Register now!",
#        "content": "The much-awaited Technox'2025-26 Part-II technical festival is starting soon! Get ready for exciting coding events, AI hackathons, hardware exhibitions, and tech #quizzes. Registrations are now open for all students. Choose your target event and submit the registration form to confirm your participation.",
#        "registration_open": False,
#        "event_name": "Technox'2025-26 Part-II",
#        "link": "/register",
#        "link_text": "open soon"
#   },
#    {
#        "id": "oa-helper-collaboration",
#        "featured": True,
#        "title": "OA Helper x Coding & AI Club: Online Assessment Prep",
#        "date": "July 20, 2026",
#        "summary": "Registration is open for the OA Helper initiative. Prepare for company-specific and topic-based MNC Online Assessments!",
#        "content": "The Coding & AI Club, NIT Mizoram is thrilled to announce our collaboration with OA Helper! Gear up for the upcoming placement season with our specialized Online Assessment (OA) preparation series. This comprehensive program is specifically designed to help students master both company-specific test patterns and topic-based coding rounds of top MNCs. Registrations are now officially open. Join us to elevate your problem-solving skills and ace your upcoming technical assessments.",
#        "registration_open": True,
#        "event_name": "OA Helper Preparation Series",
#        "link": "/register",
#        "link_text": "Register Now"
#    },
    {
        "id": "upcoming-projects",
        "featured": True,
        "title": "New Projects Starting Soon!",
        "date": "May 18, 2026",
        "summary": "Innovative projects are kicking off. Share your ideas with us!",
        "content": "Several major club projects are set to start soon across web platforms and machine learning fields. If you have an exciting, innovative idea that you want to lead or collaborate on, we would love to hear it! Bring your technical concepts to our next session or click the button below to submit your project proposal.",
        "link": "/join",
        "prefill": {
            "topic": "Project Proposal - Coding & AI Club",
            "message": "Hello Coding & AI Club,\n\nI have a project idea to propose. Here are the details:\n- Project Title:\n- Brief Description:\n- Technical Stack:\n- Intended Use Case:"
        },
        "link_text": "Propose an Idea"
    },
    {
        "id": "core-team-recruitment",
        "featured": True,
        "title": "Core Team Recruitment 2026",
        "date": "May 16, 2026",
        "summary": "Core team recruitment for the 2026-27 session is now closed.",
        "content": "The Coding & AI Club officially recruited for various Core Team positions for the academic session 2026-27. Thank you to everyone who applied! The application window is now closed.",
        "link": "#",
        "link_text": "Registration Closed"
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
    }
]

TEAM_DATA = {
    "mentors": [
        {"name": "Dr. Sukanta Roy", "role": "Faculty Mentor", "badge": "Faculty", "image": "https://ui-avatars.com/api/?name=S&background=random&color=fff&size=200"},
        {"name": "Mr. Bishal Sinha", "role": "PhD Mentor", "badge": "Research", "image": "https://ui-avatars.com/api/?name=B&background=random&color=fff&size=200"}
    ],
    "founding": [
        {"name": "Pragya", "role": "Founding Member (4th Year, IIT Madras)", "badge": "Founder", "image": "images/pragya.jpg"},
        {"name": "Rishabh Shukla", "role": "Founding Member (4th Year, IIT Madras)", "badge": "Founder", "image": "images/rishabh.jpg"}
    ],
    "core": [
        {"name": "Routhu Deva Varshini", "role": "President", "badge": "President", "image": "images/varshini.jpg"},
        {"name": "Dilip Sahu", "role": "Vice-President", "badge": "VP", "image": "images/dilip.jpg"},
        {"name": "Mahak Singh", "role": "General Secretary", "badge": "Gen. Sec.", "image": "images/mahak.jpg"},
        {"name": "V. Vyshnavi", "role": "Development & Media Lead", "badge": "Lead", "image": "images/vyshnavi.jpg"},
        {"name": "Aditya Kumar", "role": "Finance & Operations Lead", "badge": "Lead", "image": "images/aditya.jpg"},
        {"name": "Bijjala Thanmai", "role": "Events & Logistics Lead", "badge": "Lead", "image": "https://ui-avatars.com/api/?name=B&background=random&color=fff&size=200"},
        {"name": "Manoranjan Kumar", "role": "PR & Partnerships Lead", "badge": "Lead", "image": "https://ui-avatars.com/api/?name=M&background=random&color=fff&size=200"}
    ],
    "coordinators": [
        {"name": "Anand", "role": "CP Coordinator", "badge": "Coord.", "image": "https://ui-avatars.com/api/?name=A&background=random&color=fff&size=200"},
        {"name": "Mashood", "role": "Open Source Coordinator", "badge": "Coord.", "image": "https://ui-avatars.com/api/?name=M&background=random&color=fff&size=200"},
        {"name": "Saurabh Kumar Gupta", "role": "Web Development Coordinator", "badge": "Coord.", "image": "https://ui-avatars.com/api/?name=S&background=random&color=fff&size=200"},
        {"name": "Chandan Kumar", "role": "Web Development Coordinator", "badge": "Coord.", "image": "images/chandankumar.jpg"},
        {"name": "Raunak Kumar", "role": "Membership Coordinator", "badge": "Coord.", "image": "https://ui-avatars.com/api/?name=R&background=random&color=fff&size=200"},
        {"name": "S. Veerswar", "role": "Social Media Coordinator", "badge": "Coord.", "image": "https://ui-avatars.com/api/?name=S&background=random&color=fff&size=200"},
        {"name": "Dibyanshu Jha", "role": "Photography Coordinator", "badge": "Coord.", "image": "https://ui-avatars.com/api/?name=D&background=random&color=fff&size=200"}
    ]
}

PROJECT_DATA = {
    "intro": "Exploring real-world solutions through technology.",
    "featured": [
        {
            "title": "Official Club Website",
            "desc": "The very website you are browsing! Designed and built from scratch by the Web Team to showcase our club's members, events, and projects.",
            "github": "https://github.com/coding-ai-club-nitmz",
            "live": None
        }
    ],
    "contribution": {
        "title": "Want to Contribute?",
        "desc": "Club members actively collaborate on these projects. Join a team, propose an idea, or contribute code.",
        "options": [
            {
                "title": "Propose an Idea",
                "desc": "Have a project concept? Bring it to our next session.",
                "prefill": {
                    "topic": "Project Proposal Idea",
                    "message": "Respected Team,\n\nI want to propose a project idea. Here are the details:\n- Project Concept:\n- Description:"
                }
            },
            {
                "title": "Join a Team",
                "desc": "Ongoing projects always welcome new contributors.",
                "prefill": {
                    "topic": "Join Project Team Request",
                    "message": "Respected Team,\n\nI am interested in contributing to the ongoing projects. Here are my skills:\n- Tech stack skills:\n- Projects worked on:"
                }
            }
        ]
    }
}

EVENT_DATA = [
#    {"title": "Technox'2025-26 Part-II", "desc": "The premier technical festival featuring advanced coding hacks, AI quizzes, and hardware exhibitions.", "image": "images/events/notpresent.jpg", "registration_open": True, "upcoming": True},
    {"title": "Inter NIT Code Wars", "desc": "Flagship Pan-India coding contest by AlgoZenith across All 31 NITs (Codeforces Div 2 level). Contest: 27th Oct (Tue) 8:00 PM onwards. Register by 27th Oct 6:00 PM to represent NIT Mizoram!", "image": "images/club-logo.png", "registration_open": True, "registration_link": "https://forms.gle/V2rUEiLrnKjvCPkJ7", "registration_deadline": "2026-10-27 18:00:00", "upcoming": True},
    {"title": "Samyuga - Prarambh", "desc": "The coding contest initiation designed to test your algorithmic thinking and speed.", "image": "images/events/prarambh.jpg", "registration_open": False, "upcoming": False},
    {"title": "Samyuga - Trishul", "desc": "Advanced competitive programming challenges for the sharpest coders.", "image": "images/events/trishul.jpg", "registration_open": False, "upcoming": False},
    {"title": "Chakravyuh AI Quiz", "desc": "Test your knowledge of Machine Learning, Deep Learning, and AI history.", "image": "images/events/chakravyuh.jpg", "registration_open": False, "upcoming": False},
    {"title": "24 Hours Hackathon", "desc": "Build real-world solutions and innovative prototypes overnight.", "image": "images/events/hackathon.jpg", "registration_open": False, "upcoming": False},
    {"title": "Innovaite 2026", "desc": "Massive AI/ML and Idea Pitching competitions pushing the limits of Artificial Intelligence.", "image": "images/club-logo.png", "registration_open": False, "upcoming": False}
]

RESOURCE_DATA = [
    {"title": "Machine Learning Guide", "desc": "Our comprehensive introductory PDF guide for beginners starting with Python and ML models.", "tag": "Documentation", "link": "https://github.com/coding-ai-club-nitmz#ml-guide"},
    {"title": "Web Dev Roadmap", "desc": "A step-by-step checklist and resource collection for mastering frontend and backend development.", "tag": "Roadmap", "link": "https://github.com/coding-ai-club-nitmz#web-roadmap"},
    {"title": "Tech Fest Rulebooks", "desc": "Official guidelines, problem statements, and judging criteria for upcoming hackathons.", "tag": "Competition", "link": "https://github.com/coding-ai-club-nitmz#rulebooks"}
]

STATS_DATA = [
    {"num": "30+", "label": "Active Members"},
    {"num": "1+", "label": "Projects Launched"},
    {"num": "7+", "label": "Events Hosted"},
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
            "link_text": "Write a Message",
            "link_type": "join",
            "prefill": {
                "topic": "General Collaboration Inquiry",
                "message": "Hello Coding & AI Club,\n\nI would like to connect with you regarding:\n\n"
            }
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
        "name": GLOBAL_DATA["club_name"],
        "institute": "National Institute of Technology Mizoram",
        "location": "Chaltlang, Aizawl — 796012, Mizoram, India"
    }
}

COLLABORATE_DATA = {
    "hero": {
        "title": "Let's Build Something Together",
        "subtitle": "We partner with university clubs, industry sponsors, AI platforms, and competition organizers to run better hackathons, build stronger open-source projects, and create hands-on learning experiences for our members.",
    },

    "why_partner": [
        {
            "title": "An Active Builder Community",
            "desc": "30+ members engaged in AI/ML, full-stack development, and competitive programming — building real projects, not just attending talks."
        },
        {
            "title": "End-to-End Event Execution",
            "desc": "We don't just share posters. Our team plans, runs, and follows through on events end-to-end — from 24-hour hackathons like Samyuga to recurring technical bootcamps."
        },
        {
            "title": "Institute-Recognized & Reliable",
            "desc": "As an officially recognized club at NIT Mizoram, we have the backing to coordinate logistics, venues, and cross-department support for large-scale technical events."
        },
        {
            "title": "Built by Engineers, for Engineers",
            "desc": "Our core and web teams are technical by default — API integrations, platform-specific requirements, and custom tooling are things we can actually build, not just talk about."
        },
    ],


    "categories": [
        {
            "title": "University Clubs",
            "desc": "Co-host inter-college hackathons, joint workshops, and peer learning exchanges.",
            "we_offer": "Shared event planning, combined participant pools, and collaborative technical content.",
            "looking_for": "Clubs interested in running cross-campus coding contests, AI workshops, or knowledge-sharing sessions."
        },
        {
            "title": "Industry & Startups",
            "desc": "Sponsor hackathon problem statements, deliver guest lectures, or provide APIs and dev tools for our members to build with.",
            "we_offer": "A focused technical audience for your product demos, sponsored challenges at Samyuga/Technox, and real-world project integrations using your APIs.",
            "looking_for": "Companies willing to sponsor hackathon tracks, mentor student teams, or provide sandbox access to their developer tools."
        },
        {
            "title": "AI Platforms & Tools",
            "desc": "Provide compute credits, model access, or early-stage tools that our members can use in their AI/ML projects.",
            "we_offer": "Genuine usage, feedback, and project showcases from students actively building with ML frameworks and LLM pipelines.",
            "looking_for": "Platforms offering compute credits, beta access, or educational licenses worth putting in front of a builder community."
        },
        {
            "title": "Competition & Hackathon Platforms",
            "desc": "Host our coding contests and hackathons on your platform, or run structured prep programs for our members.",
            "we_offer": "A ready cohort of competitive programmers for pilot contests, mock rounds, or co-branded coding challenges.",
            "looking_for": "Platforms looking to onboard active student users or co-host competitive programming events."
        },
    ],

    "process": [
        {
            "step": "Reach Out",
            "desc": "Send us a proposal using the form below or email us directly."
        },
        {
            "step": "Discovery Call",
            "desc": "A quick call to understand your goals and explore how our community fits."
        },
        {
            "step": "Scope & Plan",
            "desc": "We define the collaboration together — format, timeline, and deliverables from each side."
        },
        {
            "step": "Execute",
            "desc": "We run the event, workshop, or integration with our core and web teams."
        },
        {
            "step": "Review",
            "desc": "We share outcomes and feedback, and discuss whether to continue or expand."
        },
    ],

    "past_collaborations": {
        "status": "onboarding",
        "message": "Our first partnerships are currently being formalized. This section will be updated as collaborations go live.",
        "items": []
    },

    "faq": [
        {
            "q": "Is there any cost involved?",
            "a": "Most partnerships are mutual — value exchanged through visibility, access, or resources rather than direct payment. If there is a financial component (e.g., hackathon sponsorship), it is discussed and agreed upon explicitly before proceeding."
        },
        {
            "q": "Can we do a one-time event instead of a long-term partnership?",
            "a": "Absolutely. We're open to both — a single guest lecture, a one-off hackathon track sponsorship, or an ongoing tool partnership."
        },
        {
            "q": "Who handles coordination on your end?",
            "a": "All inquiries go through our official club email and are handled by our core team. Leadership transitions are documented, so continuity is maintained year to year."
        },
        {
            "q": "What kind of collaborations work best?",
            "a": "The most impactful ones give our members something to build with — a real problem statement, an API to integrate, compute credits to train models, or a platform to compete on. We handle the event logistics; you bring the technical substance."
        },
    ],

    "cta": {
        "text": "Propose a Collaboration",
        "email": GLOBAL_DATA["social"]["email"],
        "link": "/join",
        "prefill": {
            "topic": "Collaboration Proposal - Coding & AI Club",
            "message": (
                "Hello Coding & AI Club,\n\n"
                "We are interested in collaborating with your club. Here are the details:\n\n"
                "- Organization / Club Name:\n"
                "- Type of Collaboration (e.g., Hackathon Sponsorship, Guest Lecture, API/Tool Access, Joint Event):\n"
                "- What We're Proposing:\n"
                "- Expected Timeline:\n"
                "- Any Resource / Cost Involvement:\n"
                "- Additional Details:\n\n"
                "Looking forward to your response."
            )
        }
    }
}

HOME_DATA = {
    "welcome_title": "Welcome to the Club",
    "welcome_desc": f"The official home of the {GLOBAL_DATA['club_name']} — a student-driven community building real-world technology at NIT Mizoram.",
    "banner_text": "Grow Together and Learn Together",
    "hero_desc": "We focus on practical engineering, collaborative projects, and peer-to-peer learning. Join us to turn your ideas into functional software."
}

JOIN_PAGE_DATA = {
    "title": "Application & Proposal Portal",
    "desc": "Please complete the application form below. Upon submission, a formalized email draft will be prepared for transmission to the club administration.",
    "intro_block": {
        "title": "Want to join the club?",
        "desc": f"If you are a student at NIT Mizoram and want to become a member of the {GLOBAL_DATA['club_name']}, please use our dedicated membership registration form.",
        "button_text": "Apply for Membership",
        "button_link": "/apply/club-join"
    },
    "options": [
        "Core Team Application - Coding & AI Club",
        "Project Proposal - Coding & AI Club",
        "Join Project Team Request",
        "Collaboration Proposal - Coding & AI Club",
        "General Collaboration Inquiry",
        "General Inquiry"
    ]
}

COMMON_DROPDOWNS = {
    "degree": [
        "B.Tech",
        "M.Tech",
        "Ph.D",
        "Other"
    ],
    "year": [
        "1st Year",
        "2nd Year",
        "3rd Year",
        "4th Year",
        "Other / Master-PhD Year"
    ],
    "branch": [
        "Computer Science & Engineering",
        "Mathematics & Computing",
        "Chemical Science & Technology",
        "Electronics & Communication Engineering",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Other / Open Elective"
    ]
}

DYNAMIC_FORMS = {
    "inter-nit-algo": {
        "title": "Inter NIT Code Wars",
        "description": "Organized by AlgoZenith in collaboration with All 31 NITs of India. Coding & AI Club, NIT Mizoram is the official Single Point of Contact (SPOC) representing NIT Mizoram in this Pan-India competitive programming contest (Codeforces Div 2 level). Contest Date: 27th Oct (Tuesday) 8:00 PM onwards. Registration closes: 27th Oct 6:00 PM. For queries: coding.club@nitmz.ac.in",
        "sheet_name": "InterNIT_Algo_Championship_2026",
        "duplicate_check_field": "Roll Number",
        "registration_deadline": "2026-10-27 18:00:00",
        "redirect_url": "https://forms.gle/V2rUEiLrnKjvCPkJ7",
        "fields": [
            "Full Name-comp",
            "Roll Number-comp",
            "Branch-comp",
            "Academic Year-comp",
            "Email Address-comp"
        ]
    },
    "club-join": {
        "title": "Join the Club",
        "description": "Formally inviting student applications for the upcoming academic term. Join our community to learn how to build real-world technology, receive mentorship, and grow your technical skills!",
        "sheet_name": "Club_Registrations_2026",
        "whatsapp_group_link": "https://chat.whatsapp.com/FprsWaXEO3L7GY97eMkAh2",
        "whatsapp_group_text": "Join Whatsapp Group",
        "duplicate_check_field": "Roll Number",
        "fields": [
            "Full Name-comp",
            "Roll Number-comp",
            "Email Address-comp",
            "Phone Number-comp",
            "Branch-comp",
            "Degree Programme-comp",
            "Academic Year-comp",
            "Why do you want to join?-comp"
        ]
    }
}

TEAM_EVENTS = {
    "innovaite-idea-pitching": {
        "title": "Innovaite 2026: Idea Pitching Competition",
        "form_type": "idea"
    },
    "innovaite-ai-ml": {
        "title": "Innovaite 2026: AI/ML Competition",
        "form_type": "aiml"
    }
}

ATTENDANCE_CONFIG = {
    "title": "Mark Your Attendance",
    "description": "Enter your Roll Number to mark today's attendance. You must be a registered club member.",
    "sheet_name": "Club_Registrations_2026",
    "roll_column": "Roll Number",
    "start_time": "2026-10-31 10:00:00",
    "end_time": "2026-10-31 23:59:00",
    "not_registered_message": "You are currently not registered as a club member. Please go to the Join Us page and apply for membership first.",
    "not_registered_link": "/apply/club-join",
    "not_registered_link_text": "Apply for Membership"
}

