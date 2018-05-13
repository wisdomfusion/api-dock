import json


def user_login(self, name, password):
    return self.client.post(
        '/api/v1/login',
        data=json.dumps({'name': name, 'password': password})
    )
