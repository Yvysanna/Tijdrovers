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

    def plan(self, day, time, course):
        '''
        Occupies classroom for given course object at given day and time

        PARAMETERS:
        day : str
            The day on which the course should be planned
        time : str
            The timeslot in which the course should be planned
        course : Course object
            The course that should be planned for the classroom

        RETURNS:
            true if success (room occupiable), otherwise false
        '''

        if not day in self._plan.keys():
            self._plan[day] = {}
        if not time in self._plan[day].keys():
            self._plan[day][time] = course
            return True
        return False

    def __str__(self) -> str:
        '''Represents the class as a string'''
        return str([
            self._name,
            #self._capacity,
            #self._possible_courses
            # [(x,[(z,a._name) for z,a in y.items()]) for x,y in self._plan.items()]
        ])

    def __repr__(self) -> str:
        '''Represents the class as a string'''
        return str([
            self.name,
            #self._capacity,
            #self._possible_courses
            # [(x,[(z,a.name) for z,a in y.items()]) for x,y in self._plan.items()]
        ])
