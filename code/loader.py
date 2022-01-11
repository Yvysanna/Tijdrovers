import csv

from subject import Subject
from classroom import Classroom


def load_subjects():
    # create objects from csv
    subjects_list = []

    # load csv
    with open('data/subjects.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        # skip header
        next(reader, None)
        # create and add subject one by one
        for row in reader:
            subjects_list.append(Subject(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    return subjects_list


def load_classrooms():
    classrooms_list = []

    with open('data/classrooms.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        for row in reader:
            classrooms_list.append(Classroom(row[0], row[1]))

    return classrooms_list

load_classrooms()
