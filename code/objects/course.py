import math
from random import choice
from objects.activity import Activity

class Course:
    '''
    Represents a single course at the campus to be scheduled

    ATTRIBUTES:
    name : str
        The name of the course
    _lecture_number : int
        The amount of lectures per week of a course
    _tutorial_number : int
        The number of tutorials per week of a course
    _tutorial_max : int
        The maximum number of students allowed to partake in a tutorial
    _lab_number : int
        The number of lab classes per week of a course
    _lab_max : int
        The maximum number of students allowed to partake in a lab class
    _student_set : set()
        Set of students assigned to the activity
    _student_number : int
        The number of enrolments for the course
    lectures :
        List of lectures for the course
    tutorials :
        List of tutorial groups for the course
    labs :
        List of lab sessions for the course
    _timeslots : int
        The minimum number of timeslots that the course will need

    METHODS:
    schedule()
        Schedules the course at a timeslot on random day and time
    smallest_classroom()
        Returns the classroom with the smallest capacity suitable for the course
    __str__()
        Represents the class as a string
    '''

    def __init__(self, name, lecture_number, tutorial_number, tutorial_max, lab_number, lab_max):
        '''
        PARAMETERS:
        name : str
            The name of the course
        lecture_number : int
            The amount of lectures per week of a course
        tutorial_number : int
            The number of tutorials per week of a course
        tutorial_max : int
            The maximum number of students allowed to partake in a tutorial
        lab_number : int
            The number of lab classes per week of a course
        lab_max : int
            The maximum number of students allowed to partake in a lab class
        '''

        self.name = name
        self._lecture_number = int(lecture_number)
        self._tutorial_number = int(tutorial_number)
        self._tutorial_max = int(tutorial_max) if tutorial_max != 'nvt' else 0
        self._lab_number = int(lab_number)
        self._lab_max = int(lab_max) if lab_max != 'nvt' else 0
        self._student_set = set()
        self._student_number = 0
        self._timeslots = 0

        self.lectures = []
        self.tutorials = []
        self.labs = []

    def add_student(self, student):
        """
        ARGS: 
            Student, object
        USAGE:
            Add student object into course's set of student objects for students enrolled into this course
        RETURNS:
            None
        """
        self._student_set.add(student)
        self._student_number += 1


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
        classroom = min([c for c in classrooms if c.capacity >= self._student_number], key=lambda c: c.capacity)

        # Create as many lecture activity objects as to be planned
        for x in range(self._lecture_number):
            lecture = Activity('Hoorcollege', f'{self.name} Hoorcollege {x + 1}', classroom, self._student_number)
            lecture.student_list = list(self._student_set)
            self.lectures.append(lecture)
        self._timeslots += self._lecture_number # Count timeslots accordingly

        self.tutorials = Course.create_activity_list(
            'Werkcollege', self.name, self._tutorial_number, self._tutorial_max, self._student_number, classrooms)

        self.labs = Course.create_activity_list(
            'Practica', self.name, self._lab_number, self._lab_max, self._student_number, classrooms)
      
    def random_register(self):
        """Register students into activities"""
        for student in self._student_set:
            # Add student to every lecture and add every lecture to student activity list
            for lecture in self.lectures:
                student.add_activity(lecture)

            Course.assign_activity(self.tutorials, student)
            Course.assign_activity(self.labs, student)
    
    def assign_activity(activities, student):
        possible_activities = []

        if activities:
            for activity in activities:
                if activity.has_space():
                    possible_activities.append(activity)

            assigned_activity = choice(possible_activities)

            if assigned_activity.register(student):
                student.add_activity(assigned_activity)

    def create_activity_list(type, name, number, max, student_number, classrooms):
    
        activities = []
        activity_number = math.ceil(student_number/max) if number > 0 else 0
        if activity_number > 0:
            student_number = math.ceil(student_number/activity_number)
            # List of all classrooms greater than amount students enrolled
            classroom = min([c for c in classrooms if c.capacity >= student_number], key=lambda c: c.capacity)
            for x in range(activity_number):
                activities.append(Activity(type, f'{name} {type} {x + 1}', classroom, max))
            #self._timeslots += activity_number

        return activities

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)
