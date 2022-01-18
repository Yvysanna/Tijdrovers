# ==================================================================================
# loader.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Loads in data from csv files
# - Initializes objects
# ==================================================================================

import csv

from objects.course import Course
from objects.classroom import Classroom
from objects.student import Student
from algorithms.register import Register


# Loads all classrooms and returns a list of Classroom objects sorted by capacity
def load_classrooms():
    classrooms_dict = {}
    classrooms_list = []

    # Open csv
    with open('data/classrooms.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Populate dictionary with name as its key and capacity as its value
        for row in reader:
            classrooms_dict[row[0]] = int(row[1])

    # Creates Classrooms objects and inserts them sorted into classrooms_list
    # min() function format from https://stackoverflow.com/questions/3282823/get-the-key-corresponding-to-the-minimum-value-within-a-dictionary
    while len(classrooms_dict) > 0:
        classroom = min(classrooms_dict, key=classrooms_dict.get)
        classrooms_list.append(
            Classroom(classroom, classrooms_dict.pop(classroom)))
    return classrooms_list


# Loads all students and returns a list of Student object and a dictionary with a Course object
# as its key and number of enrolled students as its value
def load_students():
    students_set = set()
    course_counter = {}

    # Open csv
    with open('data/students.csv', 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        for row in reader:
            courses = []
            # Creates list of courses per student and counts the students per course
            for course in row[3:]:
                # Stops loop if end of student's course list is reached
                if course == '':
                    break
                else:
                    courses.append(course)
                    # Add course if not yet in course_counter
                    if course not in course_counter:
                        course_counter[course] = 1
                    # Adds to student number in course_counter
                    else:
                        course_counter[course] += 1

            # Creates new student object and adds it to students_set
            students_set.add(Student(row[0], row[1], row[2], courses))

    return students_set, course_counter

# Loads all courses and returns a list of Course objects


def load_courses(classroom_list, course_count):
    course_set = set()

    # Open csv
    with open('data/courses.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Create course object from course data
        for row in reader:
            course = Course(row[0], row[1], row[2], row[3],
                            row[4], row[5], course_count[row[0]])
            for classroom in classroom_list:
                if classroom.capacity >= course.students_number:
                    classroom.possible_courses.append(course)
                    #course.possible_classrooms.append(classroom)
            course_set.add(course)

    return course_set

def load_activities(classrooms_list, students_set, course_list):

    for course in course_list:
        course.create_activities(classrooms_list)
    # Connect student objects with according course objects
    for student in students_set:
        for i, course in enumerate(student.courses):
            course_object = list(
                filter(lambda subj: subj.name == course, course_list))[0]
            student.courses[i] = course_object

            # Add students to courses
            register_course = Register(student.courses[i])
            register_course.register(student)

            # student.courses[i].register(student)
            #course_object.students_set.append(student)


if __name__ == '__main__':
    print(load_activities())