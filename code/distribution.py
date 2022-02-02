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
print("random_climber_3000_hardconstraint_14h")
n_runs = 0

points = []
iterations = []
# N = 5
# for x in range(N):

while time.time() - start < 50400:
    new_points, i = main()
    points.append(new_points)
    iterations.append(i)
    print(n_runs, i, points[n_runs])
    n_runs += 1

print("\n Average: " + str(mean(points)))
print("\n Average iterations: " + str(mean(iterations)))
plt.hist(points, range=(60, 150), color='midnightblue', edgecolor='mediumblue', density=True, bins=1)
plt.xlim(60, 150)
plt.title(f"Probability distribution of maluspoints across {n_runs} runs")
plt.xlabel("Maluspoints")
plt.ylabel("Probability")
plt.tight_layout()
plt.savefig('data/distribution_random_climber_3000_hardconstraint_14h.png', dpi=1000)
