# Lectures & Lesroosters

This project aims to optimally create a class schedule for the Science Park Campus at UvA. This project has been made in the scope of the course 'Programmeertheorie / Heuristiek' from the Minor Programming at the University of Amsterdam.

## Problem summary

All the data used in this project is found in the `data` directory. This problem in this project involves a list of
609 students that each follows up to 5 courses found in `students.csv`, and a list of classrooms, each with a maximum capacity found in `classrooms.csv`.<br>
There are 29 courses, each of which has a certain amount of lectures, tutorials and lab lessons per week. Each tutorial
and lab session has a maximum number of students that can participate in it, meaning there will be multiple groups
for each of these activities. All students are assigned to every lecture, so no groups are made for lectures.
Each classroom is suitable for any of the three types of activities. The number of activities and maximum amount of students is found in `courses.csv`.<br>

Each classroom has either 4 or 5 timeslots, at 9-11, 11-13, 13-15, 15-17, and only the largest classroom having a timeslot
at 17-19. Given this data it is our goal to create the most optimal class schedule by giving each activity their own
timeslot in a classroom, where we are free to assign students to any activity group.
How optimal the schedule is, is measured my maluspoints. Maluspoints are given for each of the following:<br>

- 1 point for each student that exceeds the capacity limit for a classroom
- 1 point for each time a student has two activities planned in the same timeslot
- 1 point for every time a student has a gap in their schedule
- 3 points for every time a student has two consecutive gaps in their schedule
- 5 points for every use of the timeslot at 17-19

With these soft constraints also come a few hard constraints:<br>

- Each student must have every activity that they signed up for in the schedule
- No activities can be given in the same classroom in the same timeslot
- No student may have three consecutive gaps in their schedule

## Solution summary

Explanation of summary here

## Run Locally

Clone the project

```bash
  git clone https://github.com/Yvysanna/Tijdrovers
```

Install dependencies<br>
*This code is written in Python 3.8.10 and 3.10.1. To run this code, the required packages are noted down in requirements.txt and can be installed easily via pip with this command:*

```bash
  pip install -r requirements.txt
```

Run the program

```bash
  python3 main.py
```

#### Instructions for experiments
Run the program multiple times for testing:
* Determine the time you want to run the program in line 28 of distribution.py by changing `start < {time}`
* Change the file name in line 51 to save distribution histogram
* The main algorithm used can be changed in main.py in line 56. Usable algorithm functions can be found in algorithms/hill_climber.py.
* Algorithm for determining starting position for the main algorithm can be changed to random_method or semirandom in line 50 of main.py
* In line 62 of checker.py, `idx > 2` can be used for a hard constraint for the third break period, or `idx > 3` can be used to calculate 1000 points for the third break period.
* Parameters 'streak' for climbers and 'range', formulas for 'T' and 'chance' for annealing can be changed in algorithms/hill_climber.py
* After making adjustments, run the program multiple times for a determined amount of time with `python3 code/distribution.py`

## Acknowledgements

* StackOverflow
* Minor Programmeren, Programming Lab, Faculty of Science, University of Amsterdam

## Authors

* [Karel Nijhuis](https://github.com/5inu)
* [Yvette Schröder](https://github.com/Yvysanna)
* [Julia Liem](https://github.com/julialfk)
