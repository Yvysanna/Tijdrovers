# ==================================================================================
# conflicts.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Find conflicts between two courses so that they should not be scheduled
# - in the same time slot
# ==================================================================================

import csv
from itertools import combinations


# Make list of courses
courses = []
with open("data/courses.csv", "r") as file:
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        courses.append(row["Vakken"])

# Make dictionary of every possible pair of courses and number of conflicts
# Taken from https://stackoverflow.com/questions/42591283/all-possible-combinations-of-a-set-as-a-list-of-strings
pairs = {"/".join(map(str, comb)):0 for comb in combinations(courses, 2)}

# Make list of list of courses for every student
with open("data/students.csv", "r", encoding="ISO-8859-1") as file:
    reader = csv.DictReader(file, delimiter=";")
    course_per_student = []
    for row in reader:
        temp = [row["Vak1"], row["Vak2"], row["Vak3"], row["Vak4"], row["Vak5"]]
        while "" in temp:
            temp.remove("")
        course_per_student.append(temp)

# Create list of conflicting course pairs
conflicting_pairs = []
for courses_one_student in course_per_student:
    if len(courses_one_student) > 1:
        conflicting_pairs.extend(["/".join(map(str, comb)) for comb in combinations(courses_one_student, 2)])

# Count the number of conflicts
for pair in conflicting_pairs:
    if pair in pairs:
        pairs[pair] += 1

# Sort dictionary (taken from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value)
sorted_dict = {k: v for k, v in sorted(pairs.items(), key=lambda item: item[1])}
print(sorted_dict)
