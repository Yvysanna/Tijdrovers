from collections import Counter
from algorithms.planner import Planner

class TimeClimber(Planner):
    
    #def __init__(self):
    #    pass

    # Durch fertigen Plan
    # Wo entstehen meiste Maluspunkte
    # Bewege Activitäten


    # Check welche Activity mehr Maluspunkte gibt
    # Zähle Maluspunkte
    def malus_statistic(self):
        #act_infos = [(activity, *self.get_info(activity)) for activity in self.slots if activity]
        #students_set = set(activity._students_list for activity in self.slots if activity)
        new_schedule = Counter() 
        schedule_dict = {}
        times = [[9,11],[11,13],[13,15],[15,17],[17]]

        for day in self.days:
            for time in self.times:
                activities = self.get_activities(day, time)

                for activity in activities:
                    if activity:
                        results = self.get_all_activities_at(time)

                        for student in activity._students_list:
                            starttime = int(time.split("-")[0])
                            index = self.free_time_around(student, results)
                            #print(index)
                            if index >= 0 and starttime not in times[index]:
                                if activity not in schedule_dict.keys():
                                    schedule_dict[activity] = 0
                                new_schedule.update([activity])
                                schedule_dict[activity] += 1

        #print(new_schedule) 
        return new_schedule, schedule_dict                  


    def get_all_activities_at(self, t):
        """
        ARGS: time
        """
        results = []
        for day in self.days:
            resulties = []
            for time in self.times:
                if time!= t:
                    resulties.append(self.get_activities(day, time))
            results.append(resulties)
        #print([len(r) for r in results])
        return results
        # Index > 35 

    def free_time_around(self, student, activities):
        
        for i in range(len(activities)):
            if activities[i]:
                for j in range(len(activities[i])):
                    if activities[i][j]:
                        for act in activities[i][j]:
                            if act and act.confirm_registration(student):
                                return i # Return index for all activities on same day
        return -1


# [[Project Numerical Recipes Lab 1, Compilerbouw Lab 1, Technology for games Tutorial 2, 
#     Heuristieken 2 Tutorial 1, Software engineering Tutorial 2, Algoritmen en complexiteit Tutorial 1], 
# [Collectieve Intelligentie Lab 1, Compilerbouw Tutorial 1, Programmeren in Java 2 Lab 5, Autonomous Agents 2 Lab 3,
#     Interactie-ontwerp Lecture 2, Project Genetic Algorithms Lab 2], 
# [None, Calculus 2 Lecture 1, Software engineering Lab 2, Data Mining Tutorial 3, Software engineering Lab 1, 
#     Informatie- en organisatieontwerp Tutorial 2], 
# [Collectieve Intelligentie Lab 4], 
# [Reflectie op de digitale cultuur Lecture 2, Databases 2 Tutorial 1, 
#     Bioinformatica Lecture 2, Technology for games Lecture 1, Calculus 2 Tutorial 3, Bioinformatica Tutorial 1], 
# [Heuristieken 1 Lecture 1, None, Lineaire Algebra Lecture 1, Netwerken en systeembeveiliging Lab 3, 
#     Webprogrammeren en databases Tutorial 2, Programmeren in Java 2 Lab 6], 
# [Algoritmen en complexiteit Lecture 1, Moderne Databases Lecture 1, Compilerbouw Tutorial 2, 
#     Bioinformatica Lab 3, Informatie- en organisatieontwerp Lecture 1, Project Numerical Recipes Lab 3], 
# [Technology for games Lecture 2], [Collectieve Intelligentie Lecture 3, Reflectie op de digitale cultuur Tutorial 3,
#     Reflectie op de digitale cultuur Tutorial 2, Algoritmen en complexiteit Lab 1, Zoeken sturen en bewegen Lab 2, 
#     Architectuur en computerorganisatie Lecture 1], 
# [None, None, None, Calculus 2 Tutorial 2, Software engineering Tutorial 1, Technology for games Tutorial 1], 
# [Databases 2 Lecture 1, None, Data Mining Lab 2, Machine Learning Lecture 1, Webprogrammeren en databases Lab 2, 
#     Netwerken en systeembeveiliging Lab 1], 
# [None], 
# [Webprogrammeren en databases Lecture 2, Heuristieken 2 Lecture 1, 
#     Lineaire Algebra Lecture 2, Informatie- en organisatieontwerp Lab 1, Compilerbouw practicum Lab 3, 
#     Informatie- en organisatieontwerp Lab 2], 
# [Databases 2 Tutorial 2, Compilerbouw Lab 2, Calculus 2 Tutorial 1, 
#     Moderne Databases Tutorial 3, Data Mining Lecture 1, Advanced Heuristics Lab 2], 
# [Kansrekenen 2 Lecture 1, None, Algoritmen en complexiteit Lab 2, Webprogrammeren en databases Lab 1, 
#     Moderne Databases Lab 1, Bioinformatica Tutorial 3], 
# [None], 
# [None, None, Collectieve Intelligentie Tutorial 4, Autonomous Agents 2 Lecture 1, 
#     Collectieve Intelligentie Tutorial 1, Project Genetic Algorithms Lab 3], 
# [Heuristieken 1 Tutorial 2, Bioinformatica Lecture 3, Data Mining Tutorial 1, 
#     Webprogrammeren en databases Lecture 1, Bioinformatica Lab 1, Machine Learning Lecture 2], 
# [Collectieve Intelligentie Lecture 1, Reflectie op de digitale cultuur Lecture 1, Autonomous Agents 2 Lecture 2, 
#     Architectuur en computerorganisatie Lecture 2, Bioinformatica Lab 2, Data Mining Lab 3], 
# [None]]
