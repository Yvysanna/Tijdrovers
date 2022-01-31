from collections import Counter
from algorithms.planner import Planner

class TimeClimber(Planner):
    

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