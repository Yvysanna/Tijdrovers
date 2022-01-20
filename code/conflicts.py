# ==================================================================================
# conflicts.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - For every course, finds the number of overlapping students with every
# - other course in order to prevent conflicting courses in the schedule
# ==================================================================================

from itertools import combinations, chain

def find_course_conflicts(students_set, course_set):
    # Creates the desired data structure {Course : {Course : list[Student]}}
    course_dict = {}
    conflicting_pairs = {}
    for course in course_set:
        course_dict[course] = {}
    for element in course_dict.values():
        for course in course_set:
            element[course] = []

    # If a student follows more than one course, get every combination of those courses
    for student in students_set:
        if len(student.courses) > 1:
            combs = list(combinations(student.courses, 2))

            # Add students to the list for the conflicting pair
            for conflict in combs:
                course_dict[conflict[0]][conflict[1]].append(student)
                course_dict[conflict[1]][conflict[0]].append(student)

                # for course_key in course_dict.keys():
                #     print(course_key, type(course_key), conflict[0], type(conflict[0]))
                #     if conflict[0] == course_key:
                #         # Search for the second course in the dictionary values
                #         for course_value in course_dict[course_key]:
                #             if conflict[1] == course_value:
                #                 print("test2")
                #                 # Add students to the list for the conflicting pair
                #                 course_dict[course_key][course_value].append(
                #                     student)
                #                 course_dict[course_value][course_key].append(
                #                     student)

                conflicting_pairs[conflict] = len(course_dict[conflict[0]][conflict[1]])

    # Sort dictionary (taken from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value)
    conflicting_pairs = {k: v for k, v in sorted(conflicting_pairs.items(), reverse=True, key=lambda item: item[1])}


    return course_dict, conflicting_pairs


def find_activity_conflicts(course_set, students_set):
    # Creates the desired data structure {Activity : {Activity : list[Student]}}
    activity_dict = {}
    for course in course_set:
        for activity in chain(course._tutorials, course._labs):
            activity_dict[activity] = {}
    for element in activity_dict.values():
        for course in course_set:
            for activity in chain(course._tutorials, course._labs):
                element[activity] = []

    # If a student follows more than one course, get every combination of activities
    for student in students_set:
        if len(student.courses) > 1:
            activity_list = []
            for course in student.courses:
                for activity in chain(course._labs, course._tutorials):
                    if student in activity._students_list:
                        activity_list.append(activity)
            combs = list(combinations(activity_list, 2))

            # For every conflicting pair of courses, add to dictionary
            for conflict in combs:
                if conflict[0] in activity_dict:
                    activity_dict[conflict[0]][conflict[1]].append(student)
                    activity_dict[conflict[1]][conflict[0]].append(student)

    return activity_dict
