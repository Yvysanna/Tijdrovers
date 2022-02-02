import math
from random import choice

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

    def __init__(self, name, lectures_number, tutorials_number, tutorial_max, \
                       labs_number, lab_max):
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
        self._tutorial_max = int(tutorial_max) if tutorial_max != 'nvt' else 0
        self._labs_number = int(labs_number)
        self._lab_max = int(lab_max) if lab_max != 'nvt' else 0
        self._students_set = set()
        self.students_number = 0

        # Lists with activity objects, gets filled in create activites
        self._lectures = []
        self._tutorials = []
        self._labs = []

        # No more min_timeslots, now calculated, accurate timeslots for courses
        self._timeslots = 0

    def add_student(self, student):
        """
        ARGS: 
            Student, object
        USAGE:
            Add student object into course's set of student objects for students enrolled into this course
        RETURNS:
            None
        """
        self._students_set.add(student)
        self.students_number += 1


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
            lecture = Activity('Hoorcollege', f'{self.name} Hoorcollege {x + 1}', classroom, self.students_number)
            lecture._students_list = list(self._students_set)
            self._lectures.append(lecture)
        self._timeslots += self._lectures_number # Count timeslots accordingly

        self._tutorials = Course.create_activity_list(
            'Werkcollege', self.name, self._tutorials_number, self._tutorial_max, self.students_number, classrooms)

        self._labs = Course.create_activity_list(
            'Practica', self.name, self._labs_number, self._lab_max, self.students_number, classrooms)
      
    def random_register(self):
        """Register students into activities"""
        for student in self._students_set:
            # Add student to every lecture and add every lecture to student activity list
            for lecture in self._lectures:
                student.add_activity(lecture)

            Course.assign_activity(self._tutorials, student)
            Course.assign_activity(self._labs, student)
    
    def assign_activity(activities, student):
        possible_activities = []

        if activities:
            for activity in activities:
                if activity.has_space():
                    possible_activities.append(activity)

            assigned_activity = choice(possible_activities)

            if assigned_activity.register(student):
                student.add_activity(assigned_activity)

    def create_activity_list(type, name, number, max, students_number, classrooms):
    
        activities = []
        activity_number = math.ceil(students_number/max) if number > 0 else 0
        if activity_number > 0:
            student_number = math.ceil(students_number/activity_number)
            # List of all classrooms greater than amount students enrolled
            classroom = min([c for c in classrooms if c.capacity >= student_number], key=lambda c: c.capacity)
            for x in range(activity_number):
                activities.append(Activity(type, f'{name} {type} {x + 1}', classroom, max))
            #self._timeslots += activity_number

        return activities


    def __str__(self) -> str:
        '''Represents class as a string'''
        return str(self.name)

    def __repr__(self) -> str:
        '''Represents class as a string'''
        return str(self.name)
