# ==================================================================================
# conflicts.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - For every course, finds the number of overlapping students with every
# - other course in order to prevent conflicting courses in the schedule
# ==================================================================================

from itertools import combinations

def find_conflicts(students_list, course_list):
    # Creates the desired data structure {Course : {Course : list[Student]}}
    course_dict = {}
    for course in course_list:
        course_dict[course] = {}
    for element in course_dict.values():
        for course in course_list:
            element[course] = []

    # If a student follows more than one course, get every combination of those courses
    for student in students_list:
        if len(student.courses) > 1:
            combs = list(combinations(student.courses, 2))

            # For every conflicting pair of courses, search for the first course within the dictionary
            for conflict in combs:
                for course_key in course_dict.keys():
                    if conflict[0] == course_key:
                        # Search for the second course in the dictionary values
                        for course_value in course_dict[course_key]:
                            if conflict[1] == course_value:
                                # Add students to the list for the conflicting pair
                                course_dict[course_key][course_value].append(
                                    student)
                                course_dict[course_value][course_key].append(
                                    student)
    return course_dict
