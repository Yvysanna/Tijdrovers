class Classroom:
    '''
    The classroom objects represents one of the campus' classrooms
    where a course may be taught at any time of the week

    ATTRIBUTES:
    name : str
        The name of the classroom
    capacity : int
        The number of students that can be scheduled in the classroom
    possible_courses : list[?]
        A list of courses that may be scheduled in the classroom
    _plan: : dict{str : str : Course object}
        A dictionary with _ as keys and _ as its values

    METHODS:
    plan(day, time, course):
        Occupies classroom for given course object at given day and time
    __str__():
        Represents the class as a string
    '''

    def __init__(self, name, capacity):
        '''
        ARGUMENTS:
        name : str
            The name of the classroom
        capacity : int
            The number of students that can be scheduled in the classroom
        '''

        self.name = name
        self.capacity = int(capacity)
        self.possible_courses = []
        self._plan = {}
        self._slot = 0

    def get_capacity(self):
        return self.capacity

    def __str__(self) -> str:
        '''Represents the class as a string'''
        return str(self.name)

    def __repr__(self) -> str:
        '''Represents the class as a string'''
        return str(self.name)
