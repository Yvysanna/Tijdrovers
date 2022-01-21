# ==================================================================================
# main.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Usage: python3 main.py
#
# - Creates schedule
# ==================================================================================

import pandas as pd
from algorithms.planner import Planner
from statistics import mean

from algorithms.planner import Planner
from conflicts import find_course_conflicts, find_activity_conflicts, find_conflict_free_activities, book_rooms_for_parallel_activities
import loader
import checker
import matplotlib.pyplot as plt
import random
from main import main


days = ['ma', 'di', 'wo', 'do', 'vr']
timeslots = ['9-11', '11-13', '13-15', '15-17']

pd.set_option("display.max_rows", None, "display.max_columns", None)

points = []
for x in range(500):
    classrooms_list, course_set = main()

    print(checker.count_points(classrooms_list, course_set))
    points.append(checker.count_points(classrooms_list, course_set))
print(mean(points))
plt.hist(points, range=(1300, 2000), color='midnightblue', edgecolor='mediumblue', density=True, bins=28)
plt.xlim(1300, 2000)
plt.title("Probability distrubtion of maluspoints across 500 runs")
plt.xlabel("Maluspoints")
plt.ylabel("Probability")
plt.tight_layout()
plt.savefig('test.png', dpi=1000)
