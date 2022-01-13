import csv

from subject import Subject
from classroom import Classroom
from student import Student


def load_subjects(subjects_count):
    # create objects from csv
    subjects_list = []

    # load csv
    with open('data/subjects.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        # skip header
        next(reader, None)
        # create and add subject one by one
        for row in reader:
            subjects_list.append(Subject(row[0], row[1], row[2], row[3], row[4], row[5], subjects_count[row[0]], row[7]))

    return subjects_list


def load_classrooms():
    classrooms_list = []

    with open('data/classrooms.csv', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        for row in reader:
            classrooms_list.append(Classroom(row[0], int(row[1])))

    return classrooms_list


def load_students():
    """
    creates a list of student objects and a dictionary of subjects with number of students
    """
    students_list = []
    subject_counter = {}

    with open('data/students.csv', 'r', encoding="ISO-8859-1") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        # look for the first empty value (end of student's course list)
        for row in reader:
            for i in range(len(row)):
                if row[-i] == '':
                    end = len(row) - i                   

            # counts the students per subject
            for subject in row[3:]:
                if subject == '':
                    continue
                # adds subject if not yet in subject_counter
                elif subject not in subject_counter:
                    subject_counter[subject] = 1
                # adds to student number in subject_counter
                else:
                    subject_counter[subject] += 1
                
            # creates new student object and adds it to students_list
            students_list.append(Student(row[0], row[1], row[2], row[3:end]))

    return students_list, subject_counter


if __name__ == '__main__':
    (students_list, subjects_count) = load_students()
    subjects_list = load_subjects(subjects_count)

    for subject in subjects_list:
        print(subject._name, subject._students_number)
        
    print(subjects_count)

