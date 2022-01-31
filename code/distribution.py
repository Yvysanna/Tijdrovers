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

start = time.time()
n_runs = 0

points = []
N = 5
for x in range(N):

# while time.time() - start < 3600:
    new_points = main()
    points.append(new_points)
    print(n_runs, points[n_runs])
    n_runs += 1

print("\n Average: " + str(mean(points)))
plt.hist(points, range=(50, 150), color='midnightblue', edgecolor='mediumblue', density=True, bins=12)
plt.xlim(50, 150)
plt.title(f"Probability distribution of maluspoints across {n_runs} runs")
plt.xlabel("Maluspoints")
plt.ylabel("Probability")
plt.tight_layout()
plt.savefig('data/distribution.png', dpi=1000)
