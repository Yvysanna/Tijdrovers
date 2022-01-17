<<<<<<< HEAD
class Activity:

    def __init__(self, act_type, room, student_count, name):
        self._type = act_type
        self._room = room # OPTIMISATION: GET ROOM IN ACTIVITY BASED ON LEN(STUDENT_LIST)
        self._student_count = student_count
        self._students_list = []
        self._name = name
        self._timeslot = None

    def confirm_registration(self, student):
        try: 
            self._students_list.index(student)
            return True
        except:
            return False

    def plan(self, rooms):
        '''
        Plans timeslot for activity in given room
        RETURNS: True if found, False if could not be planned (doesn't happen ATM :D )
        '''
        # Could later be replaced / sent as arguments
        days = ['ma', 'di', 'wo', 'do', 'vr']
        timeslots = ['9-11', '11-13', '13-15', '15-17']
        
        self._timeslot = self._room.plan(days[0],timeslots[0], self)
        if self._timeslot != None:
            return True

        # Find alternative rooms (next greatest)
        i = rooms.index(self._room)
        for r in rooms[i+1::]:
            self._timeslot = r.plan(days[0],timeslots[0], self)
            #print(self._timeslot, r._classroom)
            if self._timeslot != None:
                self._room = r
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
=======
class Activity:

    def __init__(self, act_type, room, student_count, name):
        self._type = act_type
        self._room = room # OPTIMISATION: GET ROOM IN ACTIVITY BASED ON LEN(STUDENT_LIST)
        self._student_count = student_count
        self._students_list = []
        self._name = name
        self._timeslot = None

    def confirm_registration(self, student):
        try: 
            self._students_list.index(student)
            return True
        except:
            return False

    def plan(self, rooms):
        '''
        Plans timeslot for activity in given room
        RETURNS: True if found, False if could not be planned (doesn't happen ATM :D )
        '''
        # Could later be replaced / sent as arguments
        days = ['ma', 'di', 'wo', 'do', 'vr']
        timeslots = ['9-11', '11-13', '13-15', '15-17']
        
        self._timeslot = self._room.plan(days[0],timeslots[0], self)
        if self._timeslot != None:
            return True

        # Find alternative rooms (next greatest)
        i = rooms.index(self._room)
        for r in rooms[i+1::]:
            self._timeslot = r.plan(days[0],timeslots[0], self)
            #print(self._timeslot, r._classroom)
            if self._timeslot != None:
                self._room = r
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
>>>>>>> 193e060e79315aea8e6b7781f567b9c2a3a1f155
        return f'\n{self._name} ({self._type}) - {self._room.name}/ {self._timeslot}'