# This is a sample Python script.
import datetime
import json
import random

from student_register import StudentRegister
from student_script import StudentScript
import threading

from timetable import is_duplicated

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

count = 0


def send_single_student_api(email, password, student_class):
    st = StudentScript(email, password)
    if len(student_class) > 8:
        st.macro(student_class[:8])
    else:
        st.macro(student_class)


def send_multiple_student_in_a_thread(start, end, data):
    for i in range(int(start), int(end)):
        send_single_student_api(f'2020{i:04d}@sis.hust.edu.vn', '123456', data[f'{i}'])


def stress_test_student(count, data):
    threads = []
    for i in range(10):
        thread = threading.Thread(target=send_multiple_student_in_a_thread,
                                  args=(count / 10 * i, count / 10 * (i + 1), data))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # for i in range(start, end):
    #     send_single_student_api(f'2020{i:04d}@sis.hust.edu.vn', '123456', data[f'{i}'])


# if __name__ == '__main__':
#     threads = []
#     for t in range(300):
#         thread = threading.Thread(target=stress_test_student, args=(t * 2, (t + 1) * 2,))
#         threads.append(thread)
#         thread.start()
#
#     for t in threads:
#         t.join()

def check_timetable(old_timetables, new_timetables):
    for new_timetable in new_timetables:
        for old_timetable in old_timetables:
            if is_duplicated(old_timetable, new_timetable):
                return False

    return True


# noinspection DuplicatedCode
def make_script(number):
    sc = StudentScript('admin', '123456')
    sc.get_current_semester()
    all_classes = sc.get_all_class()
    course_in_semester = {}
    for cls in all_classes:
        course_id = cls['courseId']
        if course_id not in course_in_semester:
            course_in_semester[f'{course_id}'] = {
                'THEORY_EXERCISE': [],
                'THEORY': [],
                'EXERCISE': [],
                'EXPERIMENT': []
            }

        if cls['classType'] == 'THEORY_EXERCISE':
            course_in_semester[f'{course_id}']['THEORY_EXERCISE'].append(cls)
        elif cls['classType'] == 'EXERCISE':
            course_in_semester[f'{course_id}']['EXERCISE'].append(cls)
        elif cls['classType'] == 'EXPERIMENT':
            course_in_semester[f'{course_id}']['EXPERIMENT'].append(cls)
        elif cls['classType'] == 'THEORY':
            course_in_semester[f'{course_id}']['THEORY'].append(cls)
        else:
            raise Exception(f'Class {cls["classType"]} not supported')
    student_register = {}
    for i in range(number):
        student_register[f'{i}'] = StudentRegister(i)
    for i, course in enumerate(course_in_semester):
        for theory_exercise_class in course_in_semester[course]['THEORY_EXERCISE']:
            list_student = [i for i in range(number)]
            random.shuffle(list_student)

            for j in range(int(theory_exercise_class['maxStudent'] * random.choice([0.8, 1.2]))):
                if len(list_student) == 0:
                    continue
                student_index = list_student.pop()
                if not theory_exercise_class['needExperiment']:
                    student_register[f'{student_index}'].add(theory_exercise_class)

        for exercise in course_in_semester[course]['THEORY_EXERCISE']:
            list_student = [i for i in range(number)]
            random.shuffle(list_student)

            for j in range(int(exercise['maxStudent'] * random.choice([0.8, 1.2]))):
                if len(list_student) == 0:
                    continue
                student_index = list_student.pop()
                if not exercise['needExperiment']:
                    student_register[f'{student_index}'].add(exercise)

    register_json = {}
    for i in range(number):
        register_json[f'{i}'] = []
    for key, value in student_register.items():
        for key_course, course in value.courses.items():
            for cls in course:
                register_json[key].append(cls['id'])

    with open('student_script.json', 'w') as file:
        json.dump(register_json, file, indent=4)


def read_script(path):
    with open(path, 'r') as file:
        data = json.load(file)
        return data


if __name__ == '__main__':
    # make_script(500)

    data = read_script('student_script.json')
    start = datetime.datetime.now()
    # stress_test_login(0, 3)
    stress_test_student(500, data)
    end = datetime.datetime.now()
    print(f'Thời gian hoàn thành: {(end - start).total_seconds()}')
