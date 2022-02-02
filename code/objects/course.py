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

    METHODS:
    add_student(student):
        Add Student object to set of students and increase total number of students
    create_activities(classrooms):
        Creates Activity objects for the course and assigns it the smallest possible classroom
    create_groups(type, number, max, classrooms):
        Creates tutorial and lab groups as Activity object and add to list of activities
    random_register():
        Register every student for their activities
    assign_activity(activities, student):
        Randomly assign a tutorial or lab group to a student
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

        self.lectures = []
        self.tutorials = []
        self.labs = []

    def add_student(self, student):
        '''Add Student object to set of students and increase total number of students'''
        self._student_set.add(student)
        self._student_number += 1


    def create_activities(self, classrooms):
        '''Creates Activity objects for the course and assigns it the smallest possible classroom'''
        # Calculate the smallest classroom that still fits all students enrolled to the course
        # Code from https://stackoverflow.com/questions/27966757/find-min-value-in-array-0
        classroom = min([c for c in classrooms if c.capacity >= self._student_number], key=lambda c: c.capacity)

        # Add every lecture which contains every student of the course
        for i in range(self._lecture_number):
            lecture = Activity('Hoorcollege', f'{self.name} Hoorcollege {i + 1}', classroom, self._student_number)
            lecture.student_list = list(self._student_set)
            self.lectures.append(lecture)

        # Create tutorials and labs without assigning students
        self.tutorials = Course.create_groups(self,'Werkcollege', self._tutorial_number, self._tutorial_max, classrooms)
        self.labs = Course.create_groups(self,'Practica', self._lab_number, self._lab_max, classrooms)

    def create_groups(self, type, number, max, classrooms):
        '''
        Creates tutorial and lab groups as Activity object and add to list of activities

        PARAMETERS:
        type : str
            The type of activity that should be made (tutorial or lab)
        number : int
            The number of activities that should be taught per week
        max : int
            The maximum number of students allowed to participate in the activity
        classrooms : [Classroom objects]
            A list of all classrooms that the activity may be scheduled in

        RETURNS:
        activities : [Activity objects]
            A list of every activity for the course
        '''

        # Calculate number of groups for tutorials or labs needed to include every student
        activities = []
        activity_number = math.ceil(self._student_number/max) if number > 0 else 0
        if activity_number > 0:
            # Calculate number of students for each group
            activity_student_number = math.ceil(self._student_number/activity_number)

            # Get smallest available classroom and add activity to list of activities
            classroom = min([c for c in classrooms if c.capacity >= activity_student_number], key=lambda c: c.capacity)
            for x in range(activity_number):
                activities.append(Activity(type, f'{self.name} {type} {x + 1}', classroom, max))

        return activities

    def random_register(self):
        '''Register every student for their activities'''
        # Add student to every lecture and add every lecture to student activity list
        for student in self._student_set:
            for lecture in self.lectures:
                student.add_activity(lecture)

            Course.assign_activity(self.tutorials, student)
            Course.assign_activity(self.labs, student)

    def assign_activity(activities, student):
        '''Randomly assign a tutorial or lab group to a student'''
        possible_activities = []
        if activities:
            for activity in activities:
                if activity.has_space():
                    possible_activities.append(activity)

            assigned_activity = choice(possible_activities)
            if assigned_activity.register(student):
                student.add_activity(assigned_activity)

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)
