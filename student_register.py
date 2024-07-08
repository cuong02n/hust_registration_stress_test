from timetable import is_duplicated


class StudentRegister:
    def __init__(self, student_id):
        self.student_id = student_id
        self.credit = 0
        self.timetables = []
        self.courses = {}
        pass

    def add(self, other):

        if self.credit >= 22 and other['courseId'] not in self.courses:
            return False

        if other['courseId'] in self.courses:
            for cls in self.courses[other['courseId']]:
                if cls['classType'] == other['classType']:
                    return False
        else:
            self.courses[other['courseId']] = []
        self.credit += other['credit']
        for old_ttb in self.timetables:
            for new_ttb in other['timetables']:
                if is_duplicated(old_ttb, new_ttb):
                    return False
        for ttb in other['timetables']:
            self.timetables.append(ttb)
        self.courses[other['courseId']].append(other)

        return True
