class Student:
    '''
    Represents a student at the campus

    ATTRIBUTES:
    last_name : str
        The students last name
    first_name : str
        The students first name
    activities : set()
        A set of all activities in which the student participates
    courses : [Course objects]
        List of courses that the student participates in

    METHODS:
    add_course(course):
        Add course to student object
    add_activity(activity):
        Adds activity to set of activities
    remove_activity(activity):
        Removes activity from set of activities
    '''

    def __init__(self, last_name, first_name):
        '''
        ARGUMENTS:
        last_name : str
            The student's surname
        first_name : str
            The student's first name
        '''

        self.last_name = last_name
        self.first_name = first_name
        self.activities = set()
        self.courses = []

    def add_course(self, course):
        '''Add course to student object'''
        self.courses.append(course)

    def add_activity(self, activity):
        '''Adds activity to set of activities'''
        self.activities.add(activity)

    def remove_activity(self, activity):
        '''Removes activity from set of activities'''
        self.activities.remove(activity)

    def __str__(self) -> str:
        return str(f'\n{self.last_name}' )

    def __repr__(self) -> str:
        return str(f'\n{self.last_name}' )
