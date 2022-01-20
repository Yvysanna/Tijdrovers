import math
#from algorithms.conflicts import new_try

class Planner:

    def __init__(self, rooms) -> None:
        self.days = ['ma', 'di', 'wo', 'do', 'vr']
        self.times = ['9-11', '11-13', '13-15', '15-17']
        self.rooms = rooms

        # All available slots
        self.slots = [None] * len(self.days) * len(self.times) * len(rooms) # For alt times create Bool Table

    def get_info(self, activity):
        """
        Get info for activity (more efficient than looping)
        """
        if activity in self.slots:
            index = self.slots.index(activity)

            day = self.days[math.floor(index / (len(self.times) * len(self.rooms)))]
            idx = index % (len(self.times) * len(self.rooms))
            room = self.rooms[math.floor(idx / len(self.times))]
            time = self.times[idx % len(self.times)]
            return room, day, time
        return None, None, None

    def insert_activity(self, activity, room, day, time):
        """
        Plan activity at this timeslot
        """
        rindex = self.rooms.index(room)
        dindex = self.days.index(day)
        tindex = self.times.index(time)
        index = dindex * (len(self.times) * len(self.rooms)) + (rindex * len(self.times)) + tindex

        #print(index, rindex, dindex, tindex)
        if self.slots[index] != None:
            return -1
        self.slots[index] = activity
        return index

    def get_activities(self, day, time):

        dindex = self.days.index(day)
        tindex = self.times.index(time)
        index = dindex * (len(self.times) * len(self.rooms)) + tindex
        return self.slots[index : index + (len(self.rooms) * len(self.times)) - tindex : len(self.times)]

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
        #for activities in new_try(students_set, course_set):
            
        #     for activity in activities:
        #         print (activity)
        #         print([student._last_name for student in activity._students_list])
        
        for room in rooms:
            for day in self.days:
                for time in self.times:
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
        '''
        # Calculation to avoid looping but still finding indexes for what we want
        idx = index % (len(self.times) * len(self.rooms))
        room = self.rooms[math.floor(idx / len(self.times))]
        day = self.days[math.floor(index / (len(self.times) * len(self.rooms)))]
        time = self.times[idx % len(self.times)]
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
    plan = Planner(['A','B','C','D','E','F','G'])

    activity = 'Hallo ich bin eine Activity'
    index = plan.insert_activity(activity, 'F', 'vr', '13-15')
    print(index, plan.get_info(activity))
    print(plan.get_activities('vr', '13-15'))
