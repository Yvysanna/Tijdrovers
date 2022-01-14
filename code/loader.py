# ==================================================================================
# main.py
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


# Loads all courses and returns a list of Course objects
def load_courses(course_count):
    course_list = []

    # Open csv
    with open('data/courses.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Create course object from course data
        for row in reader:
            course_list.append(Course(row[0], row[1], row[2], row[3], row[4], row[5], course_count[row[0]], row[7]))
            #course_list.append(Course(row[0], row[1], int(row[2)), int(row[3]) if row[3] != 'nvt' else 0, int(row[4]), int(row[5]) if row[5] != 'nvt' else 0, int(course_count[row[0]]), int(row[7])))
    return course_list


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
        classrooms_list.append(Classroom(classroom, classrooms_dict.pop(classroom)))
    return classrooms_list


# Loads all students and returns a list of Student object and a dictionary with a Course object
# as its key and number of enrolled students as its value
def load_students():
    students_list = []
    course_counter = {}

    # Open csv
    with open('data/students.csv', 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Locate the first empty value which marks the end of student's courses
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

            # Creates new student object and adds it to students_list
            students_list.append(Student(row[0], row[1], row[2], courses))

    return students_list, course_counter


if __name__ == '__main__':
    load_students()
