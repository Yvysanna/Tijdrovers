class Activity:

    def __init__(self, act_type, name, room, max_capacity, day = None, timeslot = None):
        
        self.room_list = []

        self._type = act_type
        self._room = room
        self._students_list = []
        self._max_capacity = max_capacity
        self._name = name
        self._day = day
        self._timeslot = timeslot

    def confirm_registration(self, student):
        # Correction
        if student in self._students_list:
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
    
    
    # def add_students(self, student):
    #     '''
    #     Connect student objects to according activity
    #     RETURNS: True if added, False if student could not be added
    #     '''
    #     if len(self._students_list) < self._student_count:
    #         self._students_list.append(student)
    #         return True
    #     return False

    def __str__(self):
        # return self._name
        return f'\n{self._name}'
        # return f'\n{self._name} ({self._type}) - {self._room.name} / {self._timeslot} --- {self.room_list}'

    def __repr__(self):
        # return self._name
        return f'\n{self._name}'
        # return f'\n{self._name} ({self._type}) - {self._room.name}/ {self._timeslot} --- {self.room_list}'
