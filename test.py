import requests

BASE = "http://127.0.0.1:5000/"

test_data = [
    {'id': 0, 'author': 0, 'status': 'pending', 'resolved_by': 100, 'request_created_at': "2020-08-09T12:57:13.506Z", 'vacation_start_date': "2020-08-24T00:00:00.000Z", "vacation_end_date": "2020-09-04T00:00:00.000Z"},
    {'id': 1, 'author': 0, 'status': 'pending', 'resolved_by': 100, 'request_created_at': "2020-08-09T12:57:13.506Z", 'vacation_start_date': "2020-08-24T00:00:00.000Z", "vacation_end_date": "2020-09-04T00:00:00.000Z"},
    {'id': 2, 'author': 0, 'status': 'pending', 'resolved_by': 100, 'request_created_at': "2020-08-09T12:57:13.506Z", 'vacation_start_date': "2020-08-24T00:00:00.000Z", "vacation_end_date": "2020-09-04T00:00:00.000Z"},
    {'id': 3, 'author': 0, 'status': 'pending', 'resolved_by': 100, 'request_created_at': "2020-08-09T12:57:13.506Z", 'vacation_start_date': "2020-08-24T00:00:00.000Z", "vacation_end_date": "2020-09-04T00:00:00.000Z"},
]

# FIXME: ids should be counted globally

# for i in range(len(test_data)):
#     response = requests.put(BASE + str(i), test_data[i])
#     print(response.json())
# response = requests.put(BASE + str(2), test_data[2])
# print(response.json())

# response = requests.get(BASE  + '5')
# print(response.json())
# input()
# response = requests.delete(BASE + '5')
# print(response.json())

# Testing CRUD
print('GET')
response = requests.get(BASE  + '2')
print(response.json())
print('\n')

print('PUT')
response = requests.put(BASE + '2', test_data[2])
print(response.json())
print('\n')

print('PATCH')
response = requests.patch(BASE  + '2', {'status': 'approved'})
print(response)
print('\n')

print('GET')
response = requests.get(BASE  + '2')
print(response.json())
print('\n')

print('DELETE')
response = requests.delete(BASE  + '2')
print(response)