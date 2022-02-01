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

points = []
N = 20
for x in range(N):
    new_points = main()
    print(new_points)
    points.append(new_points)

print("\n Average: " + str(mean(points)))
plt.hist(points, range=(50, 150), color='midnightblue', edgecolor='mediumblue', density=True, bins=12)
plt.xlim(50, 150)
plt.title(f"Probability distribution of maluspoints across {N} runs")
plt.xlabel("Maluspoints")
plt.ylabel("Probability")
plt.tight_layout()
plt.savefig('data/distribution.png', dpi=1000)
