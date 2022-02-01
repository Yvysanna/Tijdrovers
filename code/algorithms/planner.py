from math import floor

import random
#from code.objects.classroom import Classroom
#from copy import copy

class Planner:

    def __init__(self, rooms) -> None:
        self.days = ['ma', 'di', 'wo', 'do', 'vr']
        self.times = ['9-11', '11-13', '13-15', '15-17', '17-19'] # + 17-19
        self.rooms = sorted(rooms, key=lambda c : c.capacity, reverse = True)

        # All available slots
        #   C0.110               C1.112         A1.10          B0.201         A1.04          A1.06          A1.08         
        #   ma , di, wo, do, vr, ma,di,wo,do,vr,ma,di,wo,do,vr,ma,di,wo,do,vr,ma,di,wo,do,vr,ma,di,wo,do,vr,ma,di,wo,do,vr
        # 9  0,  1,  2,  3,  4,  5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34
        #11 35, ...
        #13 70, ...
        #15 105,...
        #17 140,141,142,143,144
        self.create_slots()

    def create_slots(self):
        self.slots = [None] * ((len(self.days) * (len(self.times) - 1) * len(self.rooms)) + len(self.days))# For alt times create Bool Table

    def get_info(self, activity):
        """
        Get info for activity (more efficient than looping)
        """
        if activity in self.slots:
            index = self.slots.index(activity)
            return self.get_slot(index)
        return None, None, None

    def swap_activities(self, i1, i2):
        self.slots[i1], self.slots[i2] = self.slots[i2], self.slots[i1]

    def insert_activity(self, activity, room, day, time):
        """
        Plan activity at this timeslot
        """
        rindex = self.rooms.index(room)
        dindex = self.days.index(day)
        tindex = self.times.index(time)
        index = dindex + (rindex * len(self.days)) + (tindex * len(self.days) * len(self.rooms))
        if index >= len(self.slots) or self.slots[index] != None:
            return -1
        self.slots[index] = activity
        return index

    def get_activities(self, day, time):
        """
        Gets all activities that are planned for the given day and time
        """
        dindex = self.days.index(day)
        tindex = self.times.index(time)
        index = tindex * (len(self.times) * len(self.rooms)) + dindex
        return self.slots[index : index + ((len(self.rooms) - 1) * len(self.days)) : len(self.days)]

    def plan_parallel(self, activities):
        for day in self.days:
            for time in self.time:
                for activity in activities:
                    self.insert_activity(activity, activity._room, day, time)
                       


    def plan_activity(self, rooms, activity):
        '''
        THE IMPORTANT ALGORITHM
        Tries to check for not planned activity, if student follows this activity and if so, which other activities should not be planned for the same timeslot, day based on students enrollment (logic as in conflicts.py used)
        '''        
        for room in rooms:
            for day in self.days:
                for time in self.times[:-1]:
                    activities = self.get_activities(day, time)
                    students_list = Planner.flatten([activity._students_list for activity in activities if activity])

                    # Checks for each student if student already has activity at given time and day
                    students_all = students_list + list(activity._students_list)
                    if not Planner.have_duplicates(students_all):
                        if self.insert_activity(activity, room, day, time) != -1:
                            return True
        return False

    def get_slot(self, index):
        '''
        Tries to find available slots
        RETURNS: room, day, time
        '''
        # Calculation to avoid looping but still finding indexes for what we want
        day = self.days[(index % (len(self.rooms) * len(self.days))) % len(self.days)]
        room = self.rooms[index % (len(self.rooms) * len(self.days)) // len(self.days)]
        time = self.times[index // (len(self.rooms) * len(self.days))]
        return room, day, time

    def get_capacity_info(self):
        '''
        Controll function, checks how many free slots stay with algorithm
        '''
        free_slots = []; busy_slots = []
        for idx, slot in enumerate(self.slots):
            if not slot:
                room, day, time = self.get_slot(idx)
                free_slots.append(f'{room.name}/ ({room.capacity}) / {(day, time)}')
            else:
                busy_slots.append(self.get_slot(idx))
        return {f"free slots: ({len(free_slots)})" :free_slots, "busy slots": len(busy_slots)}


    def unplan(self):

        malus_activities = [activity for activity in self.slots if activity and activity.malus_points()]
        for activity in self.slots:
            if activity:
                pass
                #berechnen wieviel maluspoints
        pass

    def create_student_dict(self, students_set):
        """
        Gets student dict from data in planner
        RETURNS:
            student_dict[name] = [{day: [time]}]
        """
        student_dict = {}  
        for student in students_set:
            slots = {}
            name = f'{student._last_name} {student._first_name}'
            student_dict[name] = []
            for activity in student.activities:
                room, day, time = self.get_info(activity)
                activity._room = room
                activity._day = day
                activity._timeslot = time

                # Write information into dictionary
                if day not in slots:
                    slots[day] = []
                slots[day].append(time)
            #student_dict[name].append((slots, student.activities))
            student_dict[name].append(slots)
        return student_dict   

    def flatten(lst):
        '''
        Creates one list out of a list of lists / unpacks list of lists to have only one list containing all values
        '''
        return [item for sublist in lst for item in sublist]

    def have_duplicates(lst):
        seen = set()
        dups = [x for x in lst if x in seen or seen.add(x)]
        return len(dups) > 0


if __name__ == '__main__':
    pass
    # plan = Planner([
    #     Classroom('A',20),
    #     Classroom('B',20),
    #     Classroom('C',20),
    #     Classroom('D',20),
    #     Classroom('E',20),
    #     Classroom('F',20),
    #     Classroom('G',20)
    # ])

    # activity = 'Hallo ich bin eine Activity'
    # index = plan.insert_activity(activity, 'F', 'vr', '13-15')
    # print(index, plan.get_info(activity))
    # print(plan.get_activities('vr', '13-15'))
