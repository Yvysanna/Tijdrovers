# ==================================================================================
# distribution.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Creates a histogram of total number of maluspoints across N runs
# ==================================================================================

from statistics import mean
import matplotlib.pyplot as plt
import time

from main import main
from store import store


start = time.time()
n_runs = 0

points = []
iterations = []
old_points = 1000000000000
min_students_set = None
min_planner = None
# N = 5
# for x in range(N):

while time.time() - start < 3600:
    students_set, planner, new_points, i = main()
    points.append(new_points)
    iterations.append(i)
    # if n_runs % 100 == 0:
    print(n_runs, i, points[n_runs])
    n_runs += 1

    if old_points > new_points:
        old_points = new_points
        min_students_set = students_set
        min_planner = planner

store(students_set, planner, new_points)

print("\n Average: " + str(mean(points)))
print("\n Average iterations: " + str(mean(iterations)))
plt.hist(points, range=(50, 150), color='midnightblue', edgecolor='mediumblue', density=True, bins=10)
plt.xlim(50, 150)
plt.title(f"Probability distribution of maluspoints across {n_runs} runs")
plt.xlabel("Maluspoints")
plt.ylabel("Probability")
plt.tight_layout()
plt.savefig('data/distribution_random_annealing_climber.png', dpi=1000)
