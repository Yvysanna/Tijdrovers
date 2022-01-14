# deze code is nog niet af, dus nog niet gebruiken in andere programmas

import csv
from itertools import combinations
import loader

(students_list, course_count) = loader.load_students()
course_list = loader.load_courses(course_count)

course_dict = {}
for course in course_list:
    course_dict[course] = {}
for element in course_dict.values():
    for course in course_list:
        element[course] = []


for student in students_list:
    if len(student.courses) > 1:
        combs = list(combinations(student.courses, 2))
        for conflict in combs:

            for course_key in course_dict.keys():
                if conflict[0] == course_key.name:
                    for course_value in course_dict[course_key]:
                        if conflict[1] == course_value.name:
                            #TODO:
                            #student objects ipv string
                            course_dict[course_key][course_value].append(student._first_name + ' ' + student._last_name)
                if conflict[1] == course_key.name:
                    for course_value in course_dict[course_key]:
                        if conflict[0] == course_value.name:
                            course_dict[course_key][course_value].append(student._first_name + ' ' + student._last_name)
    # if len(student.courses) == 5:
    #     print(student.courses)
    # if student._last_name == 'Brunsveld':
    #     print(student.courses)
for key, value in course_dict.items():
    print(key, '->', value)

# for x in course_dict:
#     if x.name == 'Calculus 2':
#         print(course_dict[x])
