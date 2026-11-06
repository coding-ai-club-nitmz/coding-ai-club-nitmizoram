# Copyright (c) 2026 Coding & AI Club, NIT Mizoram. All Rights Reserved.
import unittest
from unittest.mock import patch
from app import app

class TestWebRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_all_routes(self):
        routes = [
            '/',
            '/about',
            '/notices',
            '/events',
            '/teams',
            '/projects',
            '/resources',
            '/verify',
            '/collaborate',
            '/contact',
            '/join',
            '/register',
            '/attendance',
            '/robots.txt',
            '/sitemap.xml'
        ]
        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                print(f"Route '{route}' -> HTTP {response.status_code}")
                self.assertEqual(response.status_code, 200, f"Route {route} failed with {response.status_code}")

    @patch('app.background_sync_worker')
    def test_register_post_route(self, mock_sync):
        mock_sync.return_value = {"status": "success"}
        payload = {
            'name': 'TEST STUDENT',
            'roll': 'BT23CS099',
            'email': 'test@nitmz.ac.in',
            'phone': '9876543210',
            'branch': 'Computer Science & Engineering',
            'degree': 'B.Tech',
            'year': '3rd Year',
            'eventName': '24 Hours Hackathon',
            'skills': 'Python and Flask development'
        }
        response = self.client.post('/register', data=payload)
        print(f"POST /register -> HTTP {response.status_code}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registration Successful", response.data)

    def test_notice_detail_route(self):
        from data import ANNOUNCEMENTS
        if ANNOUNCEMENTS:
            first_id = ANNOUNCEMENTS[0]['id']
            route = f'/notices/{first_id}'
            response = self.client.get(route)
            print(f"Notice detail '{route}' -> HTTP {response.status_code}")
            self.assertEqual(response.status_code, 200)

            # Test non-existent notice -> should return 404
            bad_route = '/notices/nonexistent-id-12345'
            response = self.client.get(bad_route)
            print(f"Bad notice '{bad_route}' -> HTTP {response.status_code}")
            self.assertEqual(response.status_code, 404)

    @patch('google_sheets.background_sync_team_worker')
    def test_team_register_route(self, mock_team_sync):
        mock_team_sync.return_value = {"status": "success"}
        get_res = self.client.get('/register/innovaite-idea-pitching')
        self.assertEqual(get_res.status_code, 200)

        payload = {
            'team_name': 'CYBERBOTS',
            'members_count': '1',
            'track': 'Healthcare',
            'l_name': 'LEADER NAME',
            'l_roll': 'BT24CS001',
            'l_email': 'leader@nitmz.ac.in',
            'l_phone': '9876543210'
        }
        post_res = self.client.post('/register/innovaite-idea-pitching', data=payload)
        self.assertEqual(post_res.status_code, 200)
        self.assertIn(b"Registration Successful", post_res.data)

    @patch('google_sheets.background_dynamic_sync_worker')
    def test_apply_form_route(self, mock_dynamic_sync):
        mock_dynamic_sync.return_value = {"status": "success"}
        get_res = self.client.get('/apply/club-join')
        self.assertEqual(get_res.status_code, 200)

        payload = {
            'full_name': 'TEST APPLICANT',
            'roll_number': 'BT24CS010',
            'email_address': 'applicant@nitmz.ac.in',
            'phone_number': '9876543210',
            'branch': 'Computer Science & Engineering',
            'degree_programme': 'B.Tech',
            'academic_year': '1st Year',
            'why_do_you_want_to_join': 'I want to build real software.'
        }
        post_res = self.client.post('/apply/club-join', data=payload)
        self.assertEqual(post_res.status_code, 200)
        self.assertIn(b"Registration Successful", post_res.data)

    @patch('google_sheets.background_attendance_worker')
    def test_attendance_post_route(self, mock_attendance):
        mock_attendance.return_value = {"status": "success", "name": "TEST STUDENT"}

        from data import ATTENDANCE_CONFIG
        orig_start, orig_end = ATTENDANCE_CONFIG.get('start_time'), ATTENDANCE_CONFIG.get('end_time')
        ATTENDANCE_CONFIG['start_time'] = '2020-01-01 00:00:00'
        ATTENDANCE_CONFIG['end_time'] = '2030-01-01 00:00:00'

        try:
            payload = {'roll': 'BT24CS028'}
            response = self.client.post('/attendance', data=payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Attendance Marked", response.data)
        finally:
            ATTENDANCE_CONFIG['start_time'] = orig_start
            ATTENDANCE_CONFIG['end_time'] = orig_end

    def test_verify_certificate_routes(self):
        get_res = self.client.get('/verify')
        self.assertEqual(get_res.status_code, 200)

        post_valid = self.client.post('/verify', data={'cert_id': 'CERT-2026-INV-028'})
        self.assertEqual(post_valid.status_code, 200)
        self.assertIn(b"OFFICIAL VERIFIED CREDENTIAL", post_valid.data)

        post_invalid = self.client.post('/verify', data={'cert_id': 'INVALID-CERT-999'})
        self.assertEqual(post_invalid.status_code, 200)
        self.assertIn(b"VERIFICATION FAILED", post_invalid.data)

        get_cert = self.client.get('/verify/CERT-2026-INV-028')
        self.assertEqual(get_cert.status_code, 200)
        self.assertIn(b"Dilip Sahu", get_cert.data)

    def test_calendar_ics_route(self):
        res = self.client.get('/event/debate-competition-2026/calendar.ics')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'text/calendar')
        self.assertIn(b"BEGIN:VCALENDAR", res.data)
        self.assertIn(b"Inter-Departmental / Clubs Debate Competition", res.data)

        bad_res = self.client.get('/event/non-existent-event/calendar.ics')
        self.assertEqual(bad_res.status_code, 404)

if __name__ == '__main__':
    unittest.main()
