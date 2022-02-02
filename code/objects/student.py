from collections import Counter

class Student:
    '''
    Represents a student at the campus

    ATTRIBUTES:
    _last_name : str
        The student's surname
    _first_name : str
        The student's first name
    _student_number : str
        The student number
    courses : list[str]
        A list of all the courses in which the student has enrolled

    METHODS:
    __str__()
        Represents the class as a string
    '''

    def __init__(self, last_name, first_name, student_number):
        '''
        ARGUMENTS:
        _last_name : str
            The student's surname
        _first_name : str
            The student's first name
        _student_number : str
            The student number
        courses : list[str]
            A list of all the courses in which the student has enrolled
        '''

        self._last_name = last_name
        self._first_name = first_name
        self._student_number = student_number
        self.courses = []
        self.activities = set()

    def add_course(self, course):
        """Add course to student object"""
        self.courses.append(course)

    def add_activity(self, activity):
        """Add activity to student object"""
        self.activities.add(activity)

    def remove_activity(self, activity):
        """Remove activity from student object"""
        self.activities.remove(activity)

    def malus_points(self):
        """Calculate maluspoints caused by each student object"""
        #ct = Counter([f'{activity.get_day_time()}' for activity in self.activities]
        return sum(c - 1 for c in Counter([f'{activity.get_day_time()}' for activity in self.activities]).values())

    def __str__(self) -> str:
        '''Represents the class as a string'''
        return str(
            f'\n{self._last_name} ({len(self.courses)})' 
        )

    def __repr__(self) -> str:
        '''Represents the class as a string'''
        return str(
            f'\n{self._last_name} ({len(self.courses)})' 
        )
