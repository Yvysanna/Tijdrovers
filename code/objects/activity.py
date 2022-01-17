class Activity:

    def __init__(self, act_type, room, student_count, name):
        self._type = act_type
        self._room = room # OPTIMISATION: GET ALL ROOMS IN A LIST
        self._student_count = student_count
        self._students_list = []
        self._name = name
        self._timeslot = None

    def confirm_registration(self, student):
        # Correction
        if student in self._students_list:
            return True
        return False

    def add_students(self, student):
        '''
        Connect student objects to according activity
        RETURNS: True if added, False if student could not be added
        '''
        if len(self._students_list) < self._student_count:
            self._students_list.append(student)
            return True
        return False

    def set_timeslot(self, day, time):
        '''
        Add timeslot to activity
        '''
        self._timeslot = (day, time)
        #print(self._timeslot, self._room)

    def __str__(self):
        return f'\n{self._name} ({self._type}) - {self._room.name} / {self._timeslot}'

    def __repr__(self):
        return f'\n{self._name} ({self._type}) - {self._room.name}/ {self._timeslot}'