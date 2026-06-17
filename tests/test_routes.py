# Copyright (c) 2026 Coding & AI Club, NIT Mizoram. All Rights Reserved.
import unittest
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
            '/credits',
            '/projects',
            '/resources',
            '/contact',
            '/join',
            '/register',
            '/robots.txt',
            '/sitemap.xml'
        ]
        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                print(f"Route '{route}' -> HTTP {response.status_code}")
                self.assertEqual(response.status_code, 200, f"Route {route} failed with {response.status_code}")

    def test_register_post_route(self):
        payload = {
            'name': 'Test Student',
            'roll': 'CSE/23/99',
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
        # Notice detail requires a valid ID. Let's inspect ANNOUNCEMENTS from data
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

if __name__ == '__main__':
    unittest.main()

