from conflicts import find_course_conflicts
import loader
from random import randrange, choice
from itertools import combinations
from copy import deepcopy, copy


# Load classrooms and courses
classrooms_list = loader.load_classrooms()
(students_set, course_students) = loader.load_students()
course_set = loader.load_courses(classrooms_list, course_students)
loader.connect_courses(students_set, course_set)
course_dict, conflicting_pairs = find_course_conflicts(
    students_set, course_set)
loader.load_activities(classrooms_list, students_set, course_set)


timeslots_random = []
for _ in range(20):
    timeslots_random.append([])
for course in course_set:
    for _ in course._lectures:
        index = randrange(0, 20)
        timeslots_random[index].append(course.name)


def malus_count3(timeslots):
    malus = 0
    for slot in timeslots:
        if len(slot) > 1:
            combs = list(combinations(slot, 2))
            for conflict in combs:
                for x in course_dict.items():
                    if x[0].name == conflict[0]:
                        for y in course_dict.items():
                            if y[0].name == conflict[1]:
                                malus += len(course_dict[x[0]][y[0]])
                                print(conflict, len(course_dict[x[0]][y[0]]), malus)
                                if conflict[0] == conflict[1]:
                                    malus += x[0].students_number
    return malus


def malus_count2(timeslots):
    malus = 0
    for slot in timeslots:
        if len(slot) > 1:
            combs = list(combinations(slot, 2))
            for conflict in combs:
                for x in course_dict.items():
                    if x[0].name == conflict[0]:
                        for y in course_dict.items():
                            if y[0].name == conflict[1]:
                                malus += len(course_dict[x[0]][y[0]])
                                if conflict[0] == conflict[1]:
                                    malus += x[0].students_number
    return malus


def hill_climber():
    streak = 0
    old_slots = timeslots_random
    old_points = malus_count2(old_slots)
    # print("BEFORE: " + str(old_points))
    print()
    for x in old_slots:
        print(x)
    while streak < 35000:
        if streak % 5000 == 0:
            print(streak)
        new_slots = deepcopy(old_slots)
        new_slots = change(new_slots)
        new_points = malus_count2(new_slots)

        if new_points > old_points:
            new_slots = [i for i in old_slots]
            new_points = old_points
            streak += 1
        else:
            if new_points < old_points:
                streak = 0
            old_slots = [i for i in new_slots]
            old_points = new_points

    print()
    malus_count3(new_slots)
    print()
    print("AFTER: " + str(new_points))
    print()
    for x in new_slots:
        print(x)
    return new_points


def change(timeslots):
    # Pick a random lecture
    random_slot = []
    while len(random_slot) == 0:
        index1 = choice(range(len(timeslots)))
        random_slot = timeslots[index1]
    index2 = choice(range(len(random_slot)))
    random_pick = timeslots[index1][index2]

    # Randomly move lecture elsewhere
    timeslots[index1].remove(random_pick)
    new_index = randrange(0, 20)
    timeslots[new_index].append(random_pick)

    return timeslots


print(hill_climber())
