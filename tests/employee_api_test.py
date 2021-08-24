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

class Employee_Api_Test(unittest.TestCase):
    def test_6_employee_vacation_request(self):
        response = requests.get(BASE_URL + API_URL + 'employee', TEST_DATA[0])
        self.assertEqual(response.status_code, 200)

    def test_7_employee_filter_vacation_request(self):
        response = requests.get(BASE_URL + API_URL + 'employee/filter', TEST_DATA[1])
        self.assertEqual(response.status_code, 200)

    def test_8_vacation_days_remaining(self):
        response = requests.get(BASE_URL + API_URL + 'employee/remaining', TEST_DATA[0])
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()