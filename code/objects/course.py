import math
from objects.activity import Activity


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
    _timeslots : int
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

    def __init__(self, name, lectures_number, tutorials_number, tutorial_max, labs_number, lab_max, students_number):
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
        _timeslots : int
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

        # List with activity objects, gets filled in create activites
        self._activities = []

        # No more min_timeslots, now calculated, accurate timeslots for courses
        self._timeslots = 0
        
    def create_activities(self, classrooms):
        '''
        Creates activity objects for each course, fills self._activities
        MUCH ROOM FOR OPTIMIZATION: 
        - LOOKING FOR MIN CLASSROOM COULD BE MOVED TO OTHER FUNCTION
        - LECTURE, TUTORIAL, LAB WITH F-STRING ALTERNATED TO NOT REPEAT CODE
        - CALL SCHEDULE FUNCTION HERE OR IN ACTIVITY
        RETURNS: None
        '''

        #https://stackoverflow.com/questions/27966757/find-min-value-in-array-0
        # Calculate the smallest classroom that still fits all students enrolled to the course
        classroom = min([c for c in classrooms if c.capacity >= self.students_number], key=lambda c: c.capacity)
        
        # Create as many lecture activity objects as to be planned
        for x in range(self._lectures_number):
            self._activities.append(Activity('Lecture', classroom, self.students_number, f'{self.name} Lecture {x + 1}'))
        self._timeslots += self._lectures_number # Count timeslots accordingly
        
        # Tutorials, calculate number tutorials through amount student/ max amount accepted per tutorial
        tutorials_num = math.ceil(self.students_number/self._tutorials_max) if self._tutorials_number > 0 else 0
        if tutorials_num > 0:
            student_number = math.ceil(self.students_number/tutorials_num) # Total amount students after course is divided
            # Same procedure as Lecture; look for ideal classroom
            classroom = min([c for c in classrooms if c.capacity >= student_number], key=lambda c: c.capacity)
            for x in range(tutorials_num):
                self._activities.append(Activity('Tutorial', classroom, student_number, f'{self.name} Tutorial {x + 1}'))
            self._timeslots += tutorials_num

        # Same procedure for Labs
        lab_number = math.ceil(self.students_number/self._lab_max) if self._labs_number > 0 else 0
        if lab_number > 0:
            student_number = math.ceil(self.students_number/lab_number)
            # List of all classrooms greater than amount students enrolled
            classroom = min([c for c in classrooms if c.capacity >= student_number], key=lambda c: c.capacity)
            for x in range(lab_number):
                self._activities.append(Activity('Lab', classroom, student_number, f'{self.name} Lab {x + 1}'))
            self._timeslots += lab_number

    def register(self, student):
        """
        Register student for all necessary activities
        Break out of loops if student registered to avoid duplicate addings
        DISCLAIMER: Only works if tutorial and lab no more than 1 per course!!!!
        RETURNS NONE
        """
        [activity.add_students(student) for activity in self._activities if activity._type == 'Lecture']

        # Add student to first possible tutorial and lab
        for activity in self._activities:    
            if activity._type == 'Tutorial' and activity.add_students(student):
                break
        
        for activity in self._activities:
            if activity._type == 'Lab' and activity.add_students(student):
                break

    def schedule(self, rooms):
        """
        Schedules the course at a timeslot on random day and time
        RETURNS: None
        """
        for activity in self._activities:
            activity.plan(rooms)

    def __str__(self) -> str:
        '''Represents class as a string'''
        return str([
            self.name,
            #self._lectures_number,
            #self._tutorials_number,
            #self._tutorials_max,
            #self._labs_number,
            #self._lab_max,
            self.students_number,
            self._activities
            #self._timeslots,
            # self.possible_classrooms
            # self.students_list
            # len(self.students_number)

        ])

    def __repr__(self) -> str:
        '''Represents class as a string'''
        return str([
            self.name,
            #self._lectures_number,
            #self._tutorials_number,
            #self._tutorials_max,
            #self._labs_number,
            #self._lab_max,
            self.students_number,
            self._activities
            #self._timeslots,
            # self.possible_classrooms
            # self.students_list
            # len(self.students_number)
        ])
