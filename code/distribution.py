# ==================================================================================
# distribution.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Creates a histogram of total number of maluspoints across N runs
# ==================================================================================

from statistics import mean
import checker
import matplotlib.pyplot as plt
from main import main

points = []
N = 200
for x in range(N):
    classrooms_list, course_set = main()
    print(checker.count_points(course_set))
    points.append(checker.count_points(course_set))

print("\n Average: " + str(mean(points)))
plt.hist(points, range=(1300, 2000), color='midnightblue', edgecolor='mediumblue', density=True, bins=28)
plt.xlim(1300, 2000)
plt.title(f"Probability distribution of maluspoints across {N} runs")
plt.xlabel("Maluspoints")
plt.ylabel("Probability")
plt.tight_layout()
plt.savefig('data/results/distribution.png', dpi=1000)
