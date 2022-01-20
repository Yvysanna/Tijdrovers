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


def find_conflict_free_activities(course_set):
    """
    ARGS: course_set, set of course objects
    Checks which activities can be held parallel without students facing overlap
    RETURNS list of lists of all activities that can be held parallel, only having each activity appear once 
    PROBLEM: List is longer than possible timeslots, some lists shorter or longer than 7; 7 would mean activity found for each room at the same timeslot
    """
    result = []
    counter = 0

    # Create list of activities through looping through each course; may be updated with chain method?!
    activities = [activity for course in course_set for activity in course._lectures + course._tutorials + course._labs]
    queue = [activity for activity in activities] # just to avoid duplicates, can't be type(set) bc of indexing

    # Sort list so that Lecture activities are on top
    activities.sort(key=lambda act: act._type == 'Lecture', reverse = True)

    for activity_a in activities:
        if activity_a in queue:
            array = [activity_a]
            result.append(array)
            queue.pop(queue.index(activity_a)) # To only find unique matching pairs and not the same course connected to several courses

            for activity_b in queue:
                students_list = set([student for activity in array for student in activity._students_list])
                
                # Check for overlap in registered students
                if students_list.isdisjoint(activity_b._students_list):
                    queue.pop(queue.index(activity_b))
                    activity_b._counter = counter # just for counting total of groups
                    array.append(activity_b)

        counter += 1 # Just for checking

    # Sort list of lists with activities that can be planned parallel; list of most activities at the same time on top
    result.sort(key=lambda acts: len(acts), reverse=True)

    return result

def book_rooms_for_parallel_activities(result, classroom_list, counter=0):
    taken_activities = []
    for activities in result:
        counter += 1
        activities.sort(key=lambda act: len(act._students_list), reverse=True)

        leftover_activities = []
        activity_dict = {}
        for activity in activities:
            activity._counter = counter # Only for printing and checking necessary

            # Only add activity if room not taken yet
            if not activity._room in activity_dict.keys():
                activity_dict[activity._room] = activity
            else:
                # Check for next possible greater rooms (since classroom list is sortest from smallest to tallest)
                next_rooms = classroom_list[classroom_list.index(activity.room) + 1:]

                for room in next_rooms:
                    if not room in activity_dict.keys():
                        activity._room = room
                        activity_dict[activity._room] = activity
                        break # Sorry... will fix this later
                
                if activity._room in activity_dict.keys():
                    if activity != activity_dict[activity._room]:
                        leftover_activities.append(activity) # Activity cannot be scheduled parallel with others

        taken_activities.append(list(activity_dict.values()))
        if leftover_activities:

            # Recursive loop to call this function again to schedule activities with eachother
            for activities in book_rooms_for_parallel_activities([leftover_activities], classroom_list, counter+1):
                taken_activities.append(activities)

    return taken_activities