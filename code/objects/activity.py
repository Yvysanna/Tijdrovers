class Activity:
    '''
    Activity object for each activity (lecture, tutorial or lab) for a certain course

    ATTRIBUTES:
        str: type
        object: room
        list: room_list
        list: students_list
        int: max_capacity
        str: name
        str or None: day
        str or None: timeslot

    METHODS:
    confirm_registration(student):
        Returns whether a student is in the list for this activity
    has_space():
        Checks if the activity has not reached the max of allowed enrollments yet
    register(student):
        Adds a student to its student list
    malus_points():
        Calculates the malus points it causes with a late timeslot and more students enrolled than room capacity
    __str__():
        Represents the class as a string
    __repr__():
        Defines the class representation
    '''

    def __init__(self, act_type, name, room, max_capacity, day = None, timeslot = None):
        self._type = act_type
        self._room = room
        self.room_list = []
        self._students_list = []
        self._max_capacity = max_capacity
        self._name = name
        self._day = day
        self._timeslot = timeslot

    def change_day_time(self, day, timeslot):
        self._day = day
        self._timeslot = timeslot

    def confirm_registration(self, student):
        """Returns whether or not a student is registered to this activity"""
        if student in self._students_list:
            return True
        return False

    def has_space(self):
        """Return True if max enrollment has not been exceeded yet, else False"""
        return len(self._students_list) < self._max_capacity

    def register(self, student):
        """Returns True if student registration successfull, else False"""
        if self.has_space():
            self._students_list.append(student)
            return True
        return False

    def malus_points(self):
        """Calculate and return maluspoints for late timeslot and room capacity issues"""
        malus = 0
        if self._timeslot == '17-19':
            malus += 5
        if len(self._students_list) > self._room.capacity:
            malus += (len(self._students_list) - self._room.capacity)
        return malus
    
    
    def __str__(self):
        # return self._name
        return f'\n{self._name}'
        # return f'\n{self._name} ({self._type}) - {self._room.name} / {self._timeslot} --- {self.room_list}'

    def __repr__(self):
        # return self._name
        return f'\n{self._name}'
        # return f'\n{self._name} ({self._type}) - {self._room.name}/ {self._timeslot} --- {self.room_list}'
