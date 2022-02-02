This directory contains the following programs:

- `checker.py` which counts the number of maluspoints
- `loader.py` which loads in all the csv files and creates every object necessary
- `visualisations.py` which handles all the output like the schedule csv, line graph and histogram


All class definitions are found in `code/objects`. It contains the Activity, Classroom, Course and Student objects.
`activtiy` is the class to all information and methods for every activity (lecture, tutorial, lab) for each course. It also holds information over all students assigned to it and the time and location to which it is scheduled.<br>
`classroom` is the class all classroom objects belong to<br>
`course` is the main structure for each course from where its activities (activity objects) are split up and its registered students (student objects) are hold<br>
`student` holds the structure for every student object which stands for every student that is registered to its individual course choices. It also holds information about the courses(course objects) a student is assigned to and the activities(activity objects) the student belongs to<br>

The `results` directory contains every csv file from every run of the main program. It contains the schedule of every student
including every activity with its classroom and timeslot.

The algorithms for this project are found in `algorithms`, which includes a random algorithm, semirandom algorithm, and hill climber algorithms.
All these algorithms make use of the Planner object, which is found in the same directory. `planner.py` handles every timeslot for every classroom
and is integrated with every algorithm. the `plots` directory within `algorithms` contains the visualisations from these algorithms. It contains
line graphs for single runs which plot the number of maluspoints against the iterations. It also contains distribution histograms across a number
of runs. Finally, a number of graphs from old algorithms are in this folder, such as `baseline.png`.
