import unittest
import requests

BASE_URL = 'http://127.0.0.1:5000/'
API_URL = 'vacation/'
TEST_DATA = [
    {'id': 0, 'author': 0, 'status': 'pending', 'resolved_by': 100, 'request_created_at': "2021-11-01T00:00:00.000Z", 'vacation_start_date': "2021-11-09T00:00:00.000Z", "vacation_end_date": "2021-11-13T00:00:00.000Z"},
    {'id': 1, 'author': 0, 'status': 'pending', 'resolved_by': 100, 'request_created_at': "2021-12-20T00:00:00.000Z", 'vacation_start_date': "2021-12-24T00:00:00.000Z", "vacation_end_date": "2022-01-02T00:00:00.000Z"},
    {'id': 2, 'author': 0, 'status': 'pending', 'resolved_by': 100, 'request_created_at': "2022-01-10T00:00:00.000Z", 'vacation_start_date': "2022-01-20T00:00:00.000Z", "vacation_end_date": "2022-01-25T00:00:00.000Z"},
    {'id': 3, 'author': 1, 'status': 'pending', 'resolved_by': 100, 'request_created_at': "2021-10-20T00:00:00.000Z", 'vacation_start_date': "2021-11-09T00:00:00.000Z", "vacation_end_date": "2021-11-13T00:00:00.000Z"},
    {'id': 4, 'author': 1, 'status': 'approved', 'resolved_by': 100, 'request_created_at': "2021-12-20T00:00:00.000Z", 'vacation_start_date': "2021-12-24T00:00:00.000Z", "vacation_end_date": "2022-01-02T00:00:00.000Z"},
    {'id': 5, 'author': 1, 'status': 'approved', 'resolved_by': 100, 'request_created_at': "2022-01-10T00:00:00.000Z", 'vacation_start_date': "2022-01-20T00:00:00.000Z", "vacation_end_date": "2022-01-25T00:00:00.000Z"},
    {'id': 6, 'author': 2, 'status': 'pending', 'resolved_by': 100, 'request_created_at': "2021-10-20T00:00:00.000Z", 'vacation_start_date': "2021-11-09T00:00:00.000Z", "vacation_end_date": "2021-11-13T00:00:00.000Z"},
    {'id': 7, 'author': 2, 'status': 'approved', 'resolved_by': 100, 'request_created_at': "2021-11-20T00:00:00.000Z", 'vacation_start_date': "2021-12-24T00:00:00.000Z", "vacation_end_date": "2022-01-02T00:00:00.000Z"},
    {'id': 8, 'author': 2, 'status': 'approved', 'resolved_by': 100, 'request_created_at': "2022-01-10T00:00:00.000Z", 'vacation_start_date': "2022-01-20T00:00:00.000Z", "vacation_end_date": "2022-01-25T00:00:00.000Z"},
    {'id': 9, 'author': 3, 'status': 'pending', 'resolved_by': 101, 'request_created_at': "2021-10-20T00:00:00.000Z", 'vacation_start_date': "2021-11-09T00:00:00.000Z", "vacation_end_date": "2021-11-13T00:00:00.000Z"},
    {'id': 10, 'author': 3, 'status': 'approved', 'resolved_by': 101, 'request_created_at': "2021-11-20T00:00:00.000Z", 'vacation_start_date': "2021-12-24T00:00:00.000Z", "vacation_end_date": "2022-01-02T00:00:00.000Z"},
]

class Api_Test(unittest.TestCase):

    def test_1_get_base_url(self):
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_2_put_vacation_request(self):
        for i in range(len(TEST_DATA)):
            response = requests.put(BASE_URL + API_URL, TEST_DATA[i])
            self.assertEqual(response.status_code, 200)

    def test_3_get_vacation_request(self):
        response = requests.get(BASE_URL + API_URL, TEST_DATA[0])
        self.assertEqual(response.status_code, 200)


    def test_4_patch_vacation_request(self):
        TEST_DATA[0]['status'] = 'approved'
        response = requests.patch(BASE_URL + API_URL, TEST_DATA[0])
        self.assertEqual(response.status_code,200)

        response = requests.get(BASE_URL + API_URL, TEST_DATA[0])
        self.assertEqual(response.json()['status'], 'approved')
        
    def test_5_delete_vacation_request(self):
        response = requests.delete(BASE_URL + API_URL, data=TEST_DATA[0])
        self.assertEqual(response.status_code, 200)

        response = requests.get(BASE_URL + API_URL, TEST_DATA[0])
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()