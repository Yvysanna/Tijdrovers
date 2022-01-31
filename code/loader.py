# ==================================================================================
# loader.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Loads in data from csv files
# - Initializes objects
# 
# Functions: load_classrooms, 
# ==================================================================================

import csv
import itertools

from objects.course import Course
from objects.classroom import Classroom
from objects.student import Student
from algorithms.register import Register


def load_classrooms():
    """
    ARGS:
        None
    USAGE:
        Loads all classrooms from csv file
    RETURNS:
        List of all classroom objects sorted by classroom capacity ascending
    """

    # Open and read through classrooms csv
    with open('data/classrooms.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Create list of Classroom objects with name and capacity for each row in the file
        classrooms_list = [Classroom(row[0], row[1]) for row in reader]

    # Return list of objects sorted by capacity ascending
    return sorted(classrooms_list, key=lambda c: c.capacity, reverse=False)

 
def load_courses():
    """
    ARGS:
        None
    USAGE:
        Loads all courses from csv file
    RETURNS:
        course_set: Set of all course objects
    """
    course_set = set()

    with open('data/courses.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Create course object from course data and add it to the set of all objects
        for row in reader:
            course = Course(row[0], row[1], row[2], row[3], row[4], row[5])              
            course_set.add(course)

    return course_set


def load_students(course_set):
    """
    ARGS:
        course_set: set of all course objects
    USAGE:
        Loads all students from csv file
        Creates student objects and connects them with the according course objects
    RETURNS:
        students_set: set of student objects
    """
    students_set = set()

    # Open csv
    with open('data/students.csv', 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Creates new student object and adds it to students_set
        for row in reader:
            student = Student(row[0], row[1], row[2])
            students_set.add(student)

            # Iterate over all courses student is registered to
            for course in row[3:]:
                if course:
                    
                    # Find course object through equivalent string, connect student object with course object
                    course_object = [c for c in course_set if c.name == course][0]
                    student.add_course(course_object)
                    course_object.add_student(student)

    return students_set  


def load_activities(students_set, course_set, classrooms_list):
    """
    ARGS:
        students_set, course_set, classrooms_list
    USAGE:
        Loads all students from csv file
        Creates student objects and connects them with the according course objects
    RETURNS:
        students_set: set of student objects
    """
    for course in course_set:
        course.create_activities(classrooms_list)
        register_course = Register(course)
        

        for student in students_set:
            if course in student.courses:
                # Add students to courses
                register_course.random_register(student)


def connect_courses(students_set, course_set):
    # Connect student objects with according course objects
    for student in students_set:
        classmates_list = []

        for i, course in enumerate(student.courses):
            course_object = list(filter(lambda subj: subj.name == course, course_set))[0]
            student.courses[i] = course_object

            # Add all students in the same courses to a list and repeat as many times as there are lectures
            for _ in itertools.repeat(None, course_object._lectures_number):
                classmates_list.extend(course_object._students_set)

        # Counts how often this student is in the same lecture per classmate
        #print(classmates_list)
        student.classmates.update(classmates_list)

def load_results(classrooms_list = None):
    """
    Loads results from results.csv for maluspoint calculation
    RETURNS: List of activities & Dictionary in format according to maluspoint calculation
    """
    file = 'data/semirandom.csv'

    if not classrooms_list:
        classrooms_list = load_classrooms()

    # Open schedule
    # with open('data/results/results.csv', 'r', encoding="ISO-8859-1") as f:
    with open(file, 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Desired datatype: {Student : [{Day : [Timeslot]}]}
        student_dict = {}
        activity_dict = {}
        for row in reader:

            # Add entry if student not in dictionary
            name = row[0] #student name
            day = row[4]
            time = row[5]

            act_name = row[1]
            act_type = row[2]
            act_room = row[3]
            if act_name not in activity_dict.keys():
                room = [r for r in classrooms_list if r.name == act_room][0]
                from objects.activity import Activity
                activity_dict[act_name] = Activity(act_type, act_name, room, room.capacity, day, time)
            
            activity = activity_dict[act_name]
            if name not in activity._students_list:
                activity._students_list.append(name) 
                

            if name not in student_dict:
                student_dict[name] = [{day: [time]}]
            else:
                # Add entry if day not in dictionary for this student
                if not any(day in d for d in student_dict[name]):
                    #print (student_dict)
                    student_dict[name].append({day: [time]})
                # Add entry if student and day are both in dictionary
                else:
                    for x in student_dict[name]:
                        if day in x:
                            x[day].append(time)
                

        return list(activity_dict.values()), student_dict

def loadall():
    """
    ARGS: 
        None 
    USAGE:
        Loads all necessary objects and creates all necessary class objects
    RETURNS: 
        classrooms_list : List of all classroom objects sorted after capacity ascending
        students_set : Set of all student objects
        course_set : Set of all course objects
    """
    classrooms_list = load_classrooms()
    course_set = load_courses()
    students_set = load_students(course_set)
    
    load_activities(students_set, course_set, classrooms_list)
    return classrooms_list, students_set, course_set

if __name__ == '__main__':
    #import time
    # classrooms_list, students_set, course_set= loadall()
    # for course in course_set:
    #     print(course._labs)
    from checker import checker
    print(checker(*load_results()))

    # t0 = time.time()
    # for i in range(1000000):
    #     load_classrooms()
    # t1 = time.time()
    # total = t1-t0
    # print(t0, t1, total)