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

    # def plan(self, day, time, activity):
    #     '''
    #     Occupies classroom for given course object at given day and time

    #     PARAMETERS:
    #     day : str
    #         The day on which the course should be planned
    #     time : str
    #         The timeslot in which the course should be planned
    #     activity : Activity object
    #         The activity of a course that should be planned for the classroom

    #     RETURNS:
    #         day and time when the room will be occupied for certain activity
    #     '''

    #     if self._slot == 20: # HARDCODED: COULD BE CHANGED THROUGH TIMESLOT ARG IN INIT AND LIST LEN OR SO
    #         return None

    #     if not day in self._plan.keys():
    #         self._plan[day] = {}
    #         if not time in self._plan[day].keys():
    #             self._plan[day][time] = activity
    #             self._slot += 1
    #             return (day, time)

    #         time = self._get_time(day)
    #         if time != None:# or time != None:
    #             self._plan[day][time] = activity
    #             self._slot += 1
    #             return (day, time)

    #     day, time = self._get_timeslot()
    #     if day != None:# or time != None:
    #         self._plan[day][time] = activity
    #         self._slot += 1
    #         return (day, time)

    # def _get_timeslot(self):
    #     '''
    #     Looks for alternative timeslot
    #     OPTIMIZATION: 
    #     - CORRECT VARIABLE NAMES
    #     - NO HARDCODED TIMESLOTS
    #     RETURNS day, time for timeslot or None, None tuple
    #     '''
    #     days = ['ma', 'di', 'wo', 'do', 'vr']
    #     timeslots = ['9-11', '11-13', '13-15', '15-17']
    #     for d in days:
    #         if not d in self._plan.keys():
    #             self._plan[d] = {}
    #             return d, timeslots[0]
    #         t = self._get_time(d)
    #         if t != None:
    #             return d, t
    #     return None, None        

    # def _get_time(self, day):
    #     '''
    #     Looks for alternative time on day
    #     RETURNS available time
    #     '''
    #     times = ['9-11', '11-13', '13-15', '15-17']
    #     for time in times:
    #         if not time in self._plan[day].keys():
    #             return time
    #     return None

    def __str__(self) -> str:
        '''Represents the class as a string'''
        return str([
            self.name,
            #self.capacity,
            #self._possible_courses
            # [(x,[(z,a._name) for z,a in y.items()]) for x,y in self._plan.items()]
        ])

    def __repr__(self) -> str:
        '''Represents the class as a string'''
        return str([
            self.name,
            #self.capacity,
            #self._possible_courses
            # [(x,[(z,a._name) for z,a in y.items()]) for x,y in self._plan.items()]
        ])
