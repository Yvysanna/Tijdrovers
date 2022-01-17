import math

class Planner:

    days = ['ma', 'di', 'wo', 'do', 'vr']
    times = ['9-11', '11-13', '13-15', '15-17']

    def __init__(self, rooms) -> None:
        self.rooms = rooms

        # All available slots
        self.slots = [None] * len(Planner.days) * len(Planner.times) * len(rooms) # For alt times create Bool Table

    def get_info(self, activity):
        """
        Get info for activity (more efficient than looping)
        """
        if activity in self.slots:
            index = self.slots.index(activity)

            day = Planner.days[math.floor(index / (len(Planner.times) * len(self.rooms)))]
            idx = index % (len(Planner.times) * len(self.rooms))
            room = self.rooms[math.floor(idx / len(Planner.times))]
            time = Planner.times[idx % len(Planner.times)]
            return room, day, time
        return None, None, None
        
        # try:
        #     index = self.slots.index(activity)

        #     day = Planner.days[math.floor(index / (len(Planner.times) * len(self.rooms)))]
        #     idx = index % (len(Planner.times) * len(self.rooms))
        #     room = self.rooms[math.floor(idx / len(Planner.times))]
        #     time = Planner.times[idx % len(Planner.times)]

        #     return room, day, time
        # except: return None, None, None


    def plan(self, activity, room, day, time):
        """
        Plan activity at this timeslot
        """
        rindex = self.rooms.index(room)
        dindex = Planner.days.index(day)
        tindex = Planner.times.index(time)
        index = dindex * (len(Planner.times) * len(self.rooms)) + (rindex * len(Planner.times)) + tindex

        #print(index, rindex, dindex, tindex)
        if self.slots[index] != None:
            return -1
        self.slots[index] = activity
        return index
        
    def get_activities(self, day, time):

        dindex = Planner.days.index(day)
        tindex = Planner.times.index(time)
        index = dindex * (len(Planner.times) * len(self.rooms)) + tindex
        return self.slots[index : index + (len(self.rooms) * len(Planner.times)) - tindex : len(Planner.times)]

    def plan_activity(self, rooms, activity):
        '''
        THE IMPORTANT ALGORITHM
        Tries to check for not planned activity, if student follows this activity and if so, which other activities should not be planned for the same timeslot, day based on students enrollment (logic as in conflicts.py used)
        '''
        for room in rooms:
            for day in Planner.days:
                for time in Planner.times:
                    activities = self.get_activities(day, time)
                    students_list = flatten([activity._students_list for activity in activities if activity])
                    
                    # Checks for each student if student already has activity at given time and day
                    students_all = students_list + activity._students_list
                    if not have_duplicates(students_all): 
                        if self.plan(activity, room, day, time) != -1:
                            return True
        return False

    def _get_slot(self, index):
        '''
        Tries to find available slots
        '''
        # Calculation to avoid looping but still finding indexes for what we want
        idx = index % (len(Planner.times) * len(self.rooms))
        room = self.rooms[math.floor(idx / len(Planner.times))]
        day = Planner.days[math.floor(index / (len(Planner.times) * len(self.rooms)))]
        time = Planner.times[idx % len(Planner.times)]
        return room, day, time
    
    def get_capacity_info(self):
        '''
        Controll function, checks how many free slots stay with algorithm
        '''
        free_slots = []; busy_slots = []
        for idx, slot in enumerate(self.slots):
            if not slot:
                room, day, time = self._get_slot(idx)
                free_slots.append(f'{room.name}/ ({room.capacity}) / {(day, time)}')
            else:
                busy_slots.append(self._get_slot(idx))
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
    index = plan.plan(activity, 'F', 'vr', '13-15')
    print(index, plan.get_info(activity))
    print(plan.get_activities('vr', '13-15'))


