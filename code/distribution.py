# ==================================================================================
# distribution.py
#
# Julia Liem, Karel Nijhuis, Yvette Schröder
#
# - Creates a histogram of total number of maluspoints across N runs
# ==================================================================================

from statistics import mean
import matplotlib.pyplot as plt
from main import main
from store import store
import time


start = time.time()
print("random_climber_hardconstraint100000")
n_runs = 0

points = []
iterations = []
# N = 5
# for x in range(N):

while time.time() - start < 36000:
    new_points, i = main()
    points.append(new_points)
    iterations.append(i)
    print(n_runs, i, points[n_runs])
    n_runs += 1

print("\n Average: " + str(mean(points)))
print("\n Average iterations: " + str(mean(iterations)))
plt.hist(points, range=(30, 150), color='midnightblue', edgecolor='mediumblue', density=True, bins=5)
plt.xlim(30, 150)
plt.title(f"Probability distribution of maluspoints across {n_runs} runs")
plt.xlabel("Maluspoints")
plt.ylabel("Probability")
plt.tight_layout()
plt.savefig('code/algorithms/plots/distribution_random_climber_hardconstraint100000.png', dpi=1000)
