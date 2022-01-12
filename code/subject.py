class Subject:

    def __init__(self, name, lectures_number, tutorials_number, tutorial_max, labs_number, lab_max, students_number, min_timeslots):
        self._name = name
        self._lectures_number = int(lectures_number)
        self._tutorials_number = int(tutorials_number)
        self._tutorials_max = int(tutorial_max) if tutorial_max != 'nvt' else 0
        self._labs_number = int(labs_number)
        self._lab_max = int(lab_max) if lab_max != 'nvt' else 0
        self._students_number = int(students_number)
        self._min_timeslots = int(min_timeslots)
        self._possible_classrooms = []

    # Method to find smallest classroom out of all possibilities
    def smallest_classroom(self):
        return min(self._possible_classrooms, key=lambda o: o._capacity)


    # Method for representation (to receive less cryptic info when printing)
    def __str__(self) -> str:
        return str([
            self._name,
            self._lectures_number,
            self._tutorials_number,
            self._tutorials_max,
            self._labs_number,
            self._lab_max,
            self._students_number,
            self._min_timeslots,
            self._possible_classrooms
        ])

    def __repr__(self) -> str:
        return str([
            self._name,
            self._lectures_number,
            self._tutorials_number,
            self._tutorials_max,
            self._labs_number,
            self._lab_max,
            self._students_number,
            self._min_timeslots,
            self._possible_classrooms
        ])
        