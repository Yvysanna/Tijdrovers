class Activity:

    def __init__(self, act_type, name, room, max_capacity):

        self.room_list = []

        self._type = act_type
        self._room = room # OPTIMISATION: GET ALL ROOMS IN A LIST
        self._students_list = []
        self._max_capacity = max_capacity
        self._name = name
        self._timeslot = None

    def confirm_registration(self, student):
        # Correction
        if student in self._students_list:
            return True
        return False

    def malus_points(self):
        #student_points = sum(student.malus_points() for student in self._students_list)
        return len(self._students_list) - self._room.capacity if len(self._students_list) > self._room.capacity else 0 #+ student_points
    
    
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
