# ==================================================================================
# loader.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Loads in data from csv files
# - Initializes objects
# ==================================================================================

import csv
import itertools

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
    course_students = {}

    # Open csv
    with open('data/students.csv', 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        for row in reader:
            # Creates new student object and adds it to students_set
            student = Student(row[0], row[1], row[2])
            students_set.add(student)

            # Creates list of courses per student and counts the students per course
            for course in row[3:]:
                # Stops loop if end of student's course list is reached, otherwise adds course to student's courses
                if course == '':
                    break
                else:
                    student.courses.append(course)

                    # Add course with student counter and set if not yet in course_students
                    if course not in course_students:
                        course_students[course] = {'count': 1, 'students': set()}
                    else:
                        course_students[course]['count'] += 1

                    # Add student object to set
                    course_students[course]['students'].add(student)

    return students_set, course_students


# Loads all courses and returns a list of Course objects
def load_courses(classroom_list, course_students):
    course_set = set()

    # Open csv
    with open('data/courses.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Create course object from course data
        for row in reader:
            course = Course(row[0], row[1], row[2], row[3],
                            row[4], row[5], course_students[row[0]]['count'], course_students[row[0]]['students'])
            for classroom in classroom_list:
                if classroom.capacity >= course.students_number:
                    classroom.possible_courses.append(course)
                    #course.possible_classrooms.append(classroom)
            course_set.add(course)

    return course_set

def load_activities(classrooms_list, students_set, ordered_courses):

    for course in ordered_courses:
        course.create_activities(classrooms_list)

        register_course = Register(course)

        for student in students_set:
            if course in student.courses:
                # Add students to courses
                register_course.register(student)


def connect_courses(students_set, course_set):
    # Connect student objects with according course objects
    for student in students_set:
        classmates_list = []

        for i, course in enumerate(student.courses):
            course_object = list(
                filter(lambda subj: subj.name == course, course_set))[0]
            student.courses[i] = course_object

            # Add all students in the same courses to a list and repeat as many times as there are lectures
            for _ in itertools.repeat(None, course_object._lectures_number):
                classmates_list.extend(course_object._students_set)

        # Counts how often this student is in the same lecture per classmate
        student.classmates.update(classmates_list)

def load_results():
    """
    Loads results from results.csv for maluspoint calculation
    RETURNS: Dictionary in format according to maluspoint calculation
    """
    # Open schedule
    with open('data/results/results.csv', 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)

        # Desired datatype: {Student : [{Day : [Timeslot]}]}
        student_dict = {}
        for row in reader:

            # Add entry if student not in dictionary
            name = row[0]
            day = row[4]
            time = row[5]
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

        return student_dict

if __name__ == '__main__':
    print(load_activities())