import random

class Course:
    '''
    Represents a single course at the campus to be scheduled

    ATTRIBUTES:
    name : str
        The name of the course
    _lectures_number : int
        The amount of lectures per week of a course
    _tutorials_number : int
        The number of tutorials per week of a course
    _tutorial_max : int
        The maximum number of students allowed to partake in a tutorial
    _labs_number : int
        The number of lab classes per week of a course
    _lab_max : int
        The maximum number of students allowed to partake in a lab class
    students_number : int
        The number of expected enrolments for the course
    _min_timeslots : int
        The minimum number of timeslots that the course will need
    possible_classrooms : list[Classroom object]
        A list of classrooms in which the course can be taught

    METHODS:
    schedule()
        Schedules the course at a timeslot on random day and time
    smallest_classroom()
        Returns the classroom with the smallest capacity suitable for the course
    __str__()
        Represents the class as a string
    '''

    def __init__(self, name, lectures_number, tutorials_number, tutorial_max, labs_number, lab_max, students_number, min_timeslots):
        '''
        PARAMETERS:
        name : str
            The name of the course
        _lectures_number : int
            The amount of lectures per week of a course
        _tutorials_number : int
            The number of tutorials per week of a course
        _tutorial_max : int
            The maximum number of students allowed to partake in a tutorial
        _labs_number : int
            The number of lab classes per week of a course
        _lab_max : int
            The maximum number of students allowed to partake in a lab class
        students_number : int
            The number of expected enrolments for the course
        _min_timeslots : int
            The minimum number of timeslots that the course will need
        possible_classrooms : list[Classroom object]
            A list of classrooms in which the course can be taught
        '''

        self.name = name
        self._lectures_number = int(lectures_number)
        self._tutorials_number = int(tutorials_number)
        self._tutorials_max = int(tutorial_max) if tutorial_max != 'nvt' else 0
        self._labs_number = int(labs_number)
        self._lab_max = int(lab_max) if lab_max != 'nvt' else 0
        self.students_number = int(students_number)
        self._min_timeslots = int(min_timeslots)
        self.possible_classrooms = []

    def schedule(self):
        """
        Schedules the course at a timeslot on random day and time, returns None
        """
        days = ['ma', 'di', 'wo', 'do', 'vr']
        timeslots = ['9-11', '11-13', '13-15', '15-17']
        for i in range(self._min_timeslots):
            while True:
                day = random.choice(days)
                time = random.choice(timeslots)
                if self.smallest_classroom().plan(day, time, self) == True:
                    #print (i, day, time, self._name)
                    break

    def smallest_classroom(self):
        """
        Returns Classroom object with smallest capacity out of all possibilities
        """
        return min(self._possible_classrooms, key=lambda o: o._capacity)

    def __str__(self) -> str:
        '''Represents class as a string'''
        return str([
            self._name,
            #self._lectures_number,
            #self._tutorials_number,
            #self._tutorials_max,
            #self._labs_number,
            #self._lab_max,
            #self._students_number,
            #self._min_timeslots,
            self._possible_classrooms
        ])

    def __repr__(self) -> str:
        '''Represents class as a string'''
        return str([
            self._name,
            #self._lectures_number,
            #self._tutorials_number,
            #self._tutorials_max,
            #self._labs_number,
            #self._lab_max,
            #self._students_number,
            #self._min_timeslots,
            self._possible_classrooms
        ])
