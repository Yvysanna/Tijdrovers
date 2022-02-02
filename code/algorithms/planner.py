class Planner:
    '''
    The schedule for all days, times and classrooms
    Holds all activity objects after an order according to at which day,
    time and location they take place

    ATTRIBUTES:
    days : [str]
        List of days in the week
    times : [str]
        List of timeslots in a day
    rooms : [Classroom objects]
        A list of all classrooms sorted by capacity
    slots : [Activity objects]
        A list containing all timeslots across all classrooms

    METHODS:
    create_slots(self):
        Creates an empty array holding all timeslots across all classrooms
    get_info(self, activity):
        Gets room, day and time for a given activity if scheduled
    swap_activities(self, i1, i2):
        Swaps two activities
    insert_activity(self, activity, room, day, time):
        Plans given activity at given room, day, time
    get_activities(self, day, time):
        Gets all activities that are scheduled at a given day and time
    plan_activity(self, rooms, activity):
        Plans activity without causing conflicts
    get_slot(self, index):
        Gets activity planned at certain slot
    create_student_dict(self, students_set):
        Creates dictionary in format to be read by checker

    HELPERS:
    flatten(lst):
        Function to flatten a list of lists
    have_duplicates(students_list):
        Checks how many duplicates are in a list
    '''

    def __init__(self, rooms):
        '''
        ARGUMENTS:
        rooms : list()
            containing all room objects
        '''

        self.days = ['ma', 'di', 'wo', 'do', 'vr']
        self.times = ['9-11', '11-13', '13-15', '15-17', '17-19']
        self.rooms = sorted(rooms, key=lambda c: c.capacity, reverse=True)
        self.create_slots()

    def create_slots(self):
        """
        Creates slots that are used as a 2 dimensional grid
        Every fifth element marks a timeslot in a different classroom, and each consecutive element stands for
        the same time, but on a different day

        For example, the first 6 elements of this list would stand for the following:
        [Activity at monday 9-11 in C0.110, Activity at tuesdayy 9-11 in C0.110,Activity at wednesday 9-11 in C0.110,
        Activity at thursday 9-11 in C0.110, Activity at friday 9-11 in C0.110, Activity at monday 9-11 in C1.112]

        All available slots look like this if drawn schematically:
        *   C0.110               C1.112         A1.10          B0.201         A1.04          A1.06          A1.08
        *   ma , di, wo, do, vr, ma,di,wo,do,vr,ma,di,wo,do,vr,ma,di,wo,do,vr,ma,di,wo,do,vr,ma,di,wo,do,vr,ma,di,wo,do,vr
        *  9  0,  1,  2,  3,  4,  5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34
        * 11 35, ...
        * 13 70, ...
        * 15 105,...
        * 17 140,141,142,143,144
        """
        self.slots = [None] * ((len(self.days) * (len(self.times) - 1) * len(self.rooms)) + len(self.days))

    def get_info(self, activity):
        """Returns room, day and time for a certain activity or None, None, None"""
        if activity in self.slots:
            index = self.slots.index(activity)
            return self.get_slot(index)
        return None, None, None

    def swap_activities(self, i1, i2):
        """Swap activities in timeslots"""
        self.slots[i1], self.slots[i2] = self.slots[i2], self.slots[i1]

    def insert_activity(self, activity, room, day, time):
        """
        Plan activity at given room day and time
        Returns index if succeeded, else -1
        """
        rindex = self.rooms.index(room)
        dindex = self.days.index(day)
        tindex = self.times.index(time)
        index = dindex + (rindex * len(self.days)) + (tindex * len(self.days) * len(self.rooms))
        if index >= len(self.slots) or self.slots[index] is not None:
            return -1
        self.slots[index] = activity
        return index

    def get_activities(self, day, time):
        """RETURNS: all activities that are planned for the given day and time"""
        dindex = self.days.index(day)
        tindex = self.times.index(time)
        index = tindex * (len(self.times) * len(self.rooms)) + dindex
        return self.slots[index:index + ((len(self.rooms) - 1) * len(self.days)):len(self.days)]

    def plan_activity(self, rooms, activity):
        '''
        Plan activity in a room with enough capacity if no conflicts arise from students
        Returns True if success, else False
        '''
        for room in rooms:
            for day in self.days:
                for time in self.times[:-1]:
                    activities = self.get_activities(day, time)
                    students_list = Planner.flatten([activity.student_list for activity in activities if activity])

                    # Checks for each student if student already has activity at given time and day
                    students_all = students_list + list(activity.student_list)
                    if not Planner.have_duplicates(students_all):
                        if self.insert_activity(activity, room, day, time) != -1:
                            return True
        return False

    def get_slot(self, index):
        '''Returns room, day, time for an activity at a certain index'''
        day = self.days[(index % (len(self.rooms) * len(self.days))) % len(self.days)]
        room = self.rooms[index % (len(self.rooms) * len(self.days)) // len(self.days)]
        time = self.times[index // (len(self.rooms) * len(self.days))]
        return room, day, time

    def create_student_dict(self, students_set):
        """
        Creates dictionary that contains student names as keys and all timeslots and its value
        RETURNS:
        student_dict : {str : [{day: [time]}]}
        """
        student_dict = {}

        # Get student name as key for dictionary
        for student in students_set:
            slots = {}
            name = f'{student.last_name} {student.first_name}'
            student_dict[name] = []
            for activity in student.activities:
                room, day, time = self.get_info(activity)
                activity.set_day_time(day, time, room)

                # Write information into dictionary
                if day not in slots:
                    slots[day] = []
                slots[day].append(time)
            student_dict[name].append(slots)
        return student_dict

    def flatten(lst):
        '''
        Creates one list out of a list of lists / unpacks list of lists to have only one list containing all values
        https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
        '''
        return [item for sublist in lst for item in sublist]

    def have_duplicates(students_list):
        '''
        Check for duplicates in list
        https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order
        '''
        students = set()
        duplicates = [x for x in students_list if x in students or students.add(x)]
        return len(duplicates) > 0
