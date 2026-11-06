# Copyright (c) 2026 Coding & AI Club, NIT Mizoram. All Rights Reserved.
import unittest
from unittest.mock import patch
from app import app

class TestWebRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_all_get_routes(self):
        routes = [
            '/',
            '/about',
            '/notices',
            '/events',
            '/teams',
            '/projects',
            '/portal',
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
                self.assertEqual(response.status_code, 200, f"Route {route} failed with {response.status_code}")

    @patch('app.background_sync_worker')
    def test_single_registration_scenarios(self, mock_sync):
        # Scenario A: Successful registration
        mock_sync.return_value = {"status": "success"}
        valid_payload = {
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
        response = self.client.post('/register', data=valid_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registration Successful", response.data)

        # Scenario B: Duplicate registration
        mock_sync.return_value = {"status": "duplicate"}
        dup_response = self.client.post('/register', data=valid_payload)
        self.assertEqual(dup_response.status_code, 200)
        self.assertIn(b"Already Registered", dup_response.data)

        # Scenario C: Missing required fields (missing name)
        invalid_payload = valid_payload.copy()
        invalid_payload['name'] = ''
        err_response = self.client.post('/register', data=invalid_payload)
        self.assertEqual(err_response.status_code, 200)
        self.assertIn(b"Registration Failed", err_response.data)

    @patch('google_sheets.background_sync_team_worker')
    def test_team_registration_scenarios(self, mock_team_sync):
        mock_team_sync.return_value = {"status": "success"}

        # GET team registration form
        get_res = self.client.get('/register/innovaite-idea-pitching')
        self.assertEqual(get_res.status_code, 200)

        # Scenario A: Solo team registration
        solo_payload = {
            'team_name': 'SOLO BOT',
            'members_count': '1',
            'track': 'Healthcare',
            'l_name': 'LEADER NAME',
            'l_roll': 'BT24CS001',
            'l_email': 'leader@nitmz.ac.in',
            'l_phone': '9876543210'
        }
        post_solo = self.client.post('/register/innovaite-idea-pitching', data=solo_payload)
        self.assertEqual(post_solo.status_code, 200)
        self.assertIn(b"Registration Successful", post_solo.data)

        # Scenario B: Duplicate roll numbers inside submitted team
        dup_team_payload = {
            'team_name': 'DUP BOTS',
            'members_count': '2',
            'track': 'AI',
            'l_name': 'LEADER NAME',
            'l_roll': 'BT24CS001',
            'l_email': 'leader@nitmz.ac.in',
            'l_phone': '9876543210',
            'm2_name': 'MEMBER TWO',
            'm2_roll': 'BT24CS001', # Same roll number as leader!
            'm2_email': 'm2@nitmz.ac.in'
        }
        post_dup_team = self.client.post('/register/innovaite-idea-pitching', data=dup_team_payload)
        self.assertEqual(post_dup_team.status_code, 200)
        self.assertIn(b"Duplicate roll numbers found", post_dup_team.data)

        # Scenario C: Invalid team event ID -> 404
        bad_event = self.client.get('/register/nonexistent-team-event-id')
        self.assertEqual(bad_event.status_code, 404)

    @patch('google_sheets.background_dynamic_sync_worker')
    def test_dynamic_form_scenarios(self, mock_dynamic_sync):
        mock_dynamic_sync.return_value = {"status": "success"}

        # Scenario A: Active form submission (club-join)
        get_res = self.client.get('/apply/club-join')
        self.assertEqual(get_res.status_code, 200)

        valid_payload = {
            'full_name': 'TEST APPLICANT',
            'roll_number': 'BT24CS010',
            'email_address': 'applicant@nitmz.ac.in',
            'phone_number': '9876543210',
            'branch': 'Computer Science & Engineering',
            'degree_programme': 'B.Tech',
            'academic_year': '1st Year',
            'why_do_you_want_to_join': 'I want to build real software.'
        }
        post_res = self.client.post('/apply/club-join', data=valid_payload)
        self.assertEqual(post_res.status_code, 200)
        self.assertIn(b"Registration Successful", post_res.data)

        # Scenario B: Expired deadline form (inter-nit-algo)
        expired_res = self.client.get('/apply/inter-nit-algo')
        self.assertEqual(expired_res.status_code, 200)
        self.assertIn(b"Registration for this event has closed", expired_res.data)

        # Scenario C: Non-existent form ID -> 404
        bad_form = self.client.get('/apply/non-existent-form-xyz')
        self.assertEqual(bad_form.status_code, 404)

    @patch('google_sheets.background_attendance_worker')
    def test_attendance_scenarios(self, mock_attendance):
        from data import ATTENDANCE_CONFIG
        orig_start, orig_end = ATTENDANCE_CONFIG.get('start_time'), ATTENDANCE_CONFIG.get('end_time')

        # Scenario A: Time window closed
        ATTENDANCE_CONFIG['start_time'] = '2020-01-01 00:00:00'
        ATTENDANCE_CONFIG['end_time'] = '2020-01-01 00:15:00'
        closed_get = self.client.get('/attendance')
        self.assertEqual(closed_get.status_code, 200)
        self.assertIn(b"Attendance Window Closed", closed_get.data)

        # Scenario B: Time window open -> Successful attendance
        ATTENDANCE_CONFIG['start_time'] = '2020-01-01 00:00:00'
        ATTENDANCE_CONFIG['end_time'] = '2030-01-01 00:00:00'
        mock_attendance.return_value = {"status": "success", "name": "TEST STUDENT"}

        try:
            payload = {'roll': 'BT24CS028'}
            response = self.client.post('/attendance', data=payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Attendance Marked", response.data)

            # Scenario C: Already marked
            mock_attendance.return_value = {"status": "already_marked", "name": "TEST STUDENT"}
            already_res = self.client.post('/attendance', data=payload)
            self.assertEqual(already_res.status_code, 200)
            self.assertIn(b"Already Marked", already_res.data)

            # Scenario D: Not registered member
            mock_attendance.return_value = {"status": "not_registered"}
            unregistered_res = self.client.post('/attendance', data={'roll': 'BT24CS099'})
            self.assertEqual(unregistered_res.status_code, 200)
            self.assertIn(b"Not Registered", unregistered_res.data)
        finally:
            ATTENDANCE_CONFIG['start_time'] = orig_start
            ATTENDANCE_CONFIG['end_time'] = orig_end

    def test_verify_certificate_scenarios(self):
        # GET search page
        get_res = self.client.get('/verify')
        self.assertEqual(get_res.status_code, 200)

        # POST with valid cert_id
        post_valid_id = self.client.post('/verify', data={'cert_id': 'CERT-2026-INV-028'})
        self.assertEqual(post_valid_id.status_code, 200)
        self.assertIn(b"OFFICIAL VERIFIED CREDENTIAL", post_valid_id.data)

        # POST with valid roll number
        post_valid_roll = self.client.post('/verify', data={'cert_id': 'BT24CS028'})
        self.assertEqual(post_valid_roll.status_code, 200)
        self.assertIn(b"Dilip Sahu", post_valid_roll.data)

        # POST with invalid query
        post_invalid = self.client.post('/verify', data={'cert_id': 'INVALID-CERT-999'})
        self.assertEqual(post_invalid.status_code, 200)
        self.assertIn(b"VERIFICATION FAILED", post_invalid.data)

        # GET direct ID URL
        get_direct = self.client.get('/verify/CERT-2026-INV-028')
        self.assertEqual(get_direct.status_code, 200)
        self.assertIn(b"Dilip Sahu", get_direct.data)

    def test_calendar_ics_generation(self):
        res = self.client.get('/event/debate-competition-2026/calendar.ics')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'text/calendar')
        self.assertIn(b"BEGIN:VCALENDAR", res.data)
        self.assertIn(b"Inter-Departmental / Clubs Debate Competition", res.data)

        bad_res = self.client.get('/event/non-existent-event/calendar.ics')
        self.assertEqual(bad_res.status_code, 404)

    def test_notice_detail_scenarios(self):
        from data import ANNOUNCEMENTS
        if ANNOUNCEMENTS:
            first_id = ANNOUNCEMENTS[0]['id']
            res = self.client.get(f'/notices/{first_id}')
            self.assertEqual(res.status_code, 200)

        bad_notice = self.client.get('/notices/nonexistent-notice-id-999')
        self.assertEqual(bad_notice.status_code, 404)

    def test_custom_404_handler(self):
        response = self.client.get('/non-existent-path-12345')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.data)

if __name__ == '__main__':
    unittest.main()
