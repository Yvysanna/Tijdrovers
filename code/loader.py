# ==================================================================================
# loader.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Loads in data from csv files
# - Initializes and connects objects
#
# Functions: load_classrooms, load_courses, load_students, load_activities,
#            load_results, load_all
# ==================================================================================

import csv

from objects.course import Course
from objects.classroom import Classroom
from objects.student import Student
from objects.activity import Activity


def load_classrooms():
    """
    Loads all classrooms from csv file

    RETURNS:
        Sorted list of all classroom objects sorted by classroom capacity ascending
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
    Loads all students from csv file
    Creates student objects and connects them with the according course objects

    ARGS:
        course_set: set of all course objects
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
            student = Student(row[0], row[1])
            students_set.add(student)

            # Iterate over all courses student is registered to
            for course in row[3:]:
                if course:

                    # Find course object through equivalent string, connect student object with course object
                    course_object = [c for c in course_set if c.name == course][0]
                    course_object.add_student(student)

    return students_set 


def load_activities(course_set, classrooms_list):
    """
    Creates activity objects through courses and randomly registers students into it

    ARGS:
        course_set, classrooms_list
    """

    for course in course_set:
        course.create_activities(classrooms_list)
        course.random_register()


def load_results(classrooms_list = None):
    """
    Loads results from results.csv for maluspoint calculation

    ARGS:
        optional: classrooms_list
    RETURNS:
        List of activities, students dictionary with format {Student : [{Day : [Timeslot]}]}
    """

    file = 'data/climber64.csv'

    # Create list with classroom objects if not given as argument
    if not classrooms_list:
        classrooms_list = load_classrooms()

    # Open schedule
    with open(file, 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        student_dict = {}
        activity_dict = {}

        # Read through csv to collect information for student and activity
        for row in reader:
            name = row[0]
            day = row[4]
            time = row[5]

            act_name = row[1]
            act_type = row[2]
            act_room = row[3]

            # Create activity object and add to activity dict {'activity name': Activity object}
            if act_name not in activity_dict.keys():
                room = [r for r in classrooms_list if r.name == act_room][0]
                activity_dict[act_name] = Activity(act_type, act_name, room, room.capacity, day, time)
            
            activity = activity_dict[act_name]
            if name not in activity.student_list:
                activity.student_list.append(name) 
                
            if name not in student_dict:
                student_dict[name] = [{day: [time]}]
            else:
                # Add entry if day not in dictionary for this student
                if not any(day in d for d in student_dict[name]):
                    student_dict[name].append({day: [time]})

                # Add entry if student and day are both in dictionary
                else:
                    for x in student_dict[name]:
                        if day in x:
                            x[day].append(time)
                

        return list(activity_dict.values()), student_dict


def load_all():
    """
    Loads all data and creates every object for the program

    RETURNS:
        classrooms_list : List of all classroom objects sorted after capacity ascending
        students_set : Set of all student objects
        course_set : Set of all course objects
    """

    classrooms_list = load_classrooms()
    course_set = load_courses()
    students_set = load_students(course_set)
    load_activities(course_set, classrooms_list)

    return classrooms_list, students_set, course_set
