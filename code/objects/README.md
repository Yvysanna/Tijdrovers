This directory contains all class objects that form the structure of the different agents that create the complexity of this problem.

`activtiy` is the class to all information and methods for every activity (lecture, tutorial, lab) for each course. It also holds information over all students assigned to it and the time and location to which it is scheduled.<br>
`classroom` is the class all classroom objects belong to<br>
`course` is the main structure for each course from where its activities (activity objects) are split up and its registered students (student objects) are hold<br>
`student` holds the structure for every student object which stands for every student that is registered to its individual course choices. It also holds information about the courses(course objects) a student is assigned to and the activities(activity objects) the student belongs to<br>