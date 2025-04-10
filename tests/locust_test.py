import datetime

from locust import HttpUser, task


class MyUser(HttpUser):
    host = "http://127.0.0.1:8000"

    @task
    def test_stat_on_username_all_device(self):
        data = {
            'username': 'string',
            'device_name': 'string',
        }
        self.client.post(url='http://localhost:8000/analytics/on_name_one_device', json=data)

    @task
    def test_stat_on_username_all_device(self):
        data = {
            'username': 'string',
        }
        self.client.post(url='http://localhost:8000/analytics/on_username_all_device', json=data)

    @task
    def test_add_element(self):
        data = {
            'device_name': 'string',
            'x': 1,
            'y': 1,
            'z': 1,
        }
        self.client.post(url='http://localhost:8000/analytics/add_elements', json=data)

    @task
    def test_calculate_stat_all_time(self):
        data = {
            'device_name': 'string',
        }
        self.client.post(url='http://localhost:8000/analytics/all_time', json=data)

    @task
    def test_calculate_stat_interval(self):
        data = {
            'device_name': 'string',
            'start': '2020-10-10 10:10:20',
            'end': '2020-10-10 10:10:10',
        }
        self.client.post(url='http://localhost:8000/analytics/interval', json=data)

    @task
    def test_register_user(self):
        data = {
            'username': 'string1234',
        }
        self.client.post(url='http://localhost:8000/user/register', json=data)


