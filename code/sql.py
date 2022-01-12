
from re import sub
from cs50 import SQL
import csv

open("subjects.db", "w").close()
db = SQL("sqlite:///subjects.db")

db.execute("CREATE TABLE subjects (id INTEGER, name TEXT, lectures INTEGER, seminars INTEGER, practica INTEGER, \
    maxseminar INTEGER, maxpractica INTEGER, enrolments INTEGER, PRIMARY KEY(id))")

with open("data/subjects.csv", "r", encoding="ISO-8859-1") as file:
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        db.execute("INSERT INTO subjects (name, lectures, seminars, practica,\
            maxseminar, maxpractica, enrolments) VALUES(?,?,?,?,?,?,?)",
            row["Vakken"], row["#Hoorcolleges"],row["#Werkcolleges"],row["#Practica"],
            row["Max. stud."],row["Max. stud.2"], row["E(studenten)"])

db.execute("CREATE TABLE students (id INTEGER, name TEXT, subj1 TEXT, subj2 TEXT, subj3 TEXT, subj4 TEXT, \
    subj5 TEXT, PRIMARY KEY(id))")

with open("data/students.csv", "r", encoding="ISO-8859-1") as file:
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        db.execute("INSERT INTO students (name, subj1, subj2, subj3, subj4, subj5) VALUES(?,?,?,?,?,?)",
            row["Voornaam"] + " " + row["Achternaam"], row["Vak1"],row["Vak2"],row["Vak3"],row["Vak4"],row["Vak5"])
