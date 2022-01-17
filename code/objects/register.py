import conflicts

class Register:

    def __init__(self, course):

        self._course = course

    def register(self, student):

        [activity.add_students(student) for activity in self._activities if activity._type == 'Lecture']
