class Subject:

    def __init__(self, name, lectures_number, tutorials_number, tutorial_max, labs_number, lab_max, students_number, min_timeslots):
        self._name = name
        self._lectures_number = lectures_number
        self._tutorials_number = tutorials_number
        self._tutorials_max = tutorial_max
        self._labs_number = labs_number
        self._lab_max = lab_max
        self._students_number = students_number
        self._min_timeslots = min_timeslots
        self._possible_classrooms = []
