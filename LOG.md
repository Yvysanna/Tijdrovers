# Log

The first day we started with copying all data into csv files and importing this into the repository.

### Rooster alle vakken uit de onderstaande tabel in. Je mag de verwachte studentenaantallen nog even vergeten.

The first step of creating our program, was to develop a base script that allows us to schedule activities. We decided to use dataframes for this base.

The first version of main.py included dataframes based on the csv data. From these dataframes, we created a new set of dataframes. This set represented a timetables for every classroom, which we will use to fit in all course activities. 

Additionally, we also created a simple function that randomly fills the schedule with activities.

The next addition were the course and classroom classes, so objects for these variables could be created. A loader was created to read the data from the csv files and create lists of course and clasrooms objects based on this data. Later, the student class and a loader function for this class was also added.

main.py and randomize.py were edited to account for these objects.

A conflict counter was created, so we could easily visualize the size of student overlap between courses.

We also started making some SQL functions, but an assistant strongly advised against the use of SQL, so we got rid of all parts that included SQL.

### Hou nu wel rekening met de studentenaantallen. Voor iedere student die niet meer in de zaal past krijg je een maluspunt. Hoe minder maluspunten, hoe beter. De grootste zaal heeft ook een avondslot van 17:00-19:00, maar gebruik van het avondslot kost vijf maluspunten.

The next step of the assignment was to fill in the schedule, while taking into account the number of students of each course.

For this, we added a list to the classroom class that stores all possible subjects that could be hosted in that particular classroom. 

We also added a counter to the load_students function, so we could get the accurate number of students per course. The manner in which the student objects were initialized changed, so the exact number of students per course is directly taken from the counter.

In main.py, some lines were added to change the list of course names of every student to a list of course objects and directly create connections between the objects. 

A simple greedy algorithm was created based on the course size and classroom capacity.

The loader for the classrooms was changed to return the classrooms list in order of ascending capacity. As such, the list of possible classrooms of every course will also be sorted when created and we can simply go through this list to look for the next smallest available classroom instead of using a search function. This is yet to be implemented in the scheduling algorithm.

We also needed to be able to know which students were in each class, so a list of student objects was added to the course class. The creation of this list can be found in main.py within an existing loop that changed the list of course names to course objects.