class Activity:
    '''
    Represents either a lecture, a tutorial group or lab group

    ATTRIBUTES:
    type : str
        The type of activity, either a lecture, tutorial or lab session
    room : Room object
        The classroom in which the activity takes place
    students_list : [Student object]
        A list of every student assigned to the activity
    max_students : int
        The maximum amount of students allowed to participate in the activity
    name : str
        The name of the activity
    day : str
        The day in which the activity takes place, if scheduled
    timeslot : str
        The time at which the activity takes place, if scheduled

    METHODS:
    set_day_time():
        Sets the day and time at which the activity takes place
    get_day_time():
        Returns the day and time at which the activity takes place
    confirm_registration(student):
        Checks whether or not a student is in the list for this activity
    has_space():
        Checks if the activity has reached the maximum amount of allowed enrolments
    register(student):
        Adds a student to its list of students
    maluspoints():
        Calculates the maluspoints it causes using the late timeslot and exceeding of room capacity
    '''

    def __init__(self, act_type, name, room, max_capacity, day = None, timeslot = None):
        '''
        PARAMETERS:
        act_type : str
            The type of activity, either a lecture, tutorial or lab session
        name : str
            The name of the activity
        room : Room object
            The classroom in which the activity takes place
        max_students : int
            The maximum amount of students allowed to participate in the activity
        day : str
            The day in which the activity takes place, if scheduled
        timeslot : str
            The time at which the activity takes place, if scheduled
        '''

        self.type = act_type
        self.room = room
        self.student_list = []
        self.max_students = max_capacity
        self.name = name
        self.day = day
        self.timeslot = timeslot

    def set_day_time(self, day, timeslot):
        '''Sets the day and time at which the activity takes place'''
        self.day = day
        self.timeslot = timeslot

    def get_day_time(self):
        '''Returns the day and time at which the activity takes place'''
        return self.day, self.timeslot

    def confirm_registration(self, student):
        '''Checks whether or not a student is in the list for this activity'''
        if student in self.student_list:
            return True
        return False

    def has_space(self):
        '''Checks if the activity has reached the maximum amount of allowed enrolments'''
        return len(self.student_list) < self.max_students

    def register(self, student):
        '''Adds a student to its list of students, returns bool based on whether registration was succesful or not'''
        if self.has_space():
            self.student_list.append(student)
            return True
        return False

    def maluspoints(self):
        '''Calculates the maluspoints it causes using the late timeslot and exceeding of room capacity'''
        capacity = self.room.get_capacity()

        students_count = len(self.student_list)
        malus = students_count - capacity if students_count > capacity else 0
        malus += 5 if self.timeslot == '17-19' else 0
        malus += sum(student.malus_points() for student in self.student_list)

        return malus

    def __str__(self):
        return f'\n{self.name}'

    def __repr__(self):
        return f'\n{self.name}'
