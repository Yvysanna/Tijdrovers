# Find conflicts between two subjects so that they should not be scheduled in the same time slot

import csv
from itertools import combinations


# make list of subjects
subjects = []
with open("data/subjects.csv", "r") as file:
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        subjects.append(row["Vakken"])

# make dictionary of every possible pair of subjects and number of conflicts
# taken from https://stackoverflow.com/questions/42591283/all-possible-combinations-of-a-set-as-a-list-of-strings
pairs = {"/".join(map(str, comb)):0 for comb in combinations(subjects, 2)}

# make list of list of subjects for every student
with open("data/students.csv", "r", encoding="ISO-8859-1") as file:
    reader = csv.DictReader(file, delimiter=";")
    subject_per_student = []
    for row in reader:
        temp = [row["Vak1"], row["Vak2"], row["Vak3"], row["Vak4"], row["Vak5"]]
        while "" in temp:
            temp.remove("")
        subject_per_student.append(temp)

# create list of conflicting subject pairs
conflicting_pairs = []
for subjects_one_student in subject_per_student:
    if len(subjects_one_student) > 1:
        conflicting_pairs.extend(["/".join(map(str, comb)) for comb in combinations(subjects_one_student, 2)])

# count the number of conflicts
for pair in conflicting_pairs:
    if pair in pairs:
        pairs[pair] += 1

# sort dictionary (taken from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value)
sorted_dict = {k: v for k, v in sorted(pairs.items(), key=lambda item: item[1])}
print(sorted_dict)
