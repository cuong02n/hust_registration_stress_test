import requests

base_url = 'http://localhost:8080'
url_auth = base_url + '/api/v1/auth/login'
url_get_info = base_url + '/api/user/get-info'

url_get_current_semester = base_url + '/api/metadata/current-semester'

url_get_metadata_semester = base_url + '/api/metadata/get-by-semester'

url_get_register_course = base_url + '/api/students/courses/register-courses'

url_register_class = base_url + '/api/students/classes/register-class'

url_get_all_class = base_url + '/api/classes/get-by-semester'

success = 0
failed = 0


class StudentScript:
    def __init__(self, email, password):
        self.role = None
        self.token = None
        self.semester = None
        self.email = email
        self.password = password
        self.authorize()

    def authorize(self):
        response = requests.post(url_auth, json={'email': self.email, 'password': self.password}).json()
        # print(response)
        self.token = response['data']['token']
        self.role = response['data']['role']
        # print(response)

    def get_info(self):
        response = requests.get(url_get_info, self.token).json()
        # do nothing

    def get_current_semester(self):
        self.semester = \
            requests.get(url_get_current_semester, headers={'Authorization': f'Bearer {self.token}'}).json()['data']

    def get_metadata_semester(self):
        response = requests.get(url_get_metadata_semester, params={'semester': self.semester},
                                headers={'Authorization': f'Bearer {self.token}'}).json()
        # print(response['data'])
        # do nothing

    def get_register_course(self):
        response = requests.get(url_get_register_course, params={'semester': self.semester},
                                headers={'Authorization': f'Bearer {self.token}'}).json()
        print(response['data'])

    def get_register_class(self):
        response = requests.get(url_register_class, params={'semester': self.semester},
                                headers={'Authorization': f'Bearer {self.token}'}).json()
        print(response)

    def get_all_class(self):
        response = requests.get(url_get_all_class, params={'semester': self.semester},
                                headers={'Authorization': f'Bearer {self.token}'}).json()
        return response['data']

    def register_class(self, classes):
        response = requests.post(url_register_class, headers={'Authorization': f'Bearer {self.token}'},
                                 json={'semester': self.semester, 'classIds': classes})
        if str(response.status_code)[0] == '2':
            global success
            success += 1
            print(f'Thành công {success}')
        else:
            global failed
            failed += 1
            print(f'Thất bại {failed}')

    def macro(self, classes):
        # self.get_info()
        self.get_current_semester()
        # self.get_metadata_semester()
        # self.get_register_course()

        # self.get_register_class()
        self.register_class(classes)
