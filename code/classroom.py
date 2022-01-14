class Classroom:

    def __init__(self, classroom, capacity):
        self._classroom = classroom
        self._capacity = int(capacity)
        self._possible_subjects = []
        self._plan = {}
    
    def plan(self, day, time, course):
        """
        occupies room for given course object at given day and time
        RETURNS true if success (room occupiable), otherwise false
        """
        if not day in self._plan.keys():
            self._plan[day] = {}
        if not time in self._plan[day].keys():
            self._plan[day][time] = course
            return True
        return False

    def __str__(self) -> str:
        return str([
            self._classroom, 
            #self._capacity, 
            # self._possible_subjects,
            [(x,[(z,a._name) for z,a in y.items()]) for x,y in self._plan.items()]
        ])

    def __repr__(self) -> str:
        return str([
            self._classroom, 
            #self._capacity, 
            # self._possible_subjects,
            [(x,[(z,a._name) for z,a in y.items()]) for x,y in self._plan.items()]
        ])