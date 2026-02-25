from abc import ABC, abstractmethod

courses = [
    ("CSE101", "Python Programming", "CSE", 2, 4, 5000),
    ("ECE201", "Digital Circuits", "ECE", 1, 3, 4500)
]

discounts = {"final_year": 0.10, "merit": 0.05}

registrations = []
registered_rolls = {}
waiting_list = {}
reg_counter = 1

for c in courses:
    registered_rolls[c[0]] = set()
    waiting_list[c[0]] = []

class UniversitySystem(ABC):
    @abstractmethod
    def register_student(self): pass

    @abstractmethod
    def drop_course(self): pass

    @abstractmethod
    def report(self): pass

    @abstractmethod
    def search(self): pass

    @abstractmethod
    def revenue(self): pass

class Course:
    def __init__(self, code, name, dept, seats, credits, fee):
        self.code = code
        self.name = name
        self.dept = dept
        self.seats = seats
        self.credits = credits
        self.fee = fee

class Student:
    def __init__(self, name, roll, year, merit):
        self.name = name
        self.roll = roll
        self.year = year
        self.merit = merit

class Registration(Course, Student, UniversitySystem):
    def __init__(self):
        pass

    def get_course(self, code):
        for c in courses:
            if c[0] == code:
                return Course(*c)

    def calculate_fee(self, course, student):
        fee = course.fee
        if student.year == 4:
            fee -= fee * discounts["final_year"]
        if student.merit:
            fee -= fee * discounts["merit"]
        return fee

    def register_student(self):
        global reg_counter
        code = input("Course Code: ")
        name = input("Student Name: ")
        roll = int(input("Roll No: "))
        year = int(input("Year (1-4): "))
        merit = input("Merit Student (yes/no): ").lower() == "yes"

        course = self.get_course(code)
        student = Student(name, roll, year, merit)

        if len(registered_rolls[code]) < course.seats:
            fee_paid = self.calculate_fee(course, student)
            registrations.append({
                "reg_id": reg_counter,
                "course_code": code,
                "student_name": name,
                "roll_no": roll,
                "year": year,
                "fee_paid": fee_paid
            })
            registered_rolls[code].add(roll)
            print("Registered with ID:", reg_counter, "Fee:", fee_paid)
            reg_counter += 1
        else:
            waiting_list[code].append((name, roll, year, merit))
            print("Added to Waiting List. Position:", len(waiting_list[code]))

    def drop_course(self):
        reg_id = int(input("Enter Registration ID: "))
        for r in registrations:
            if r["reg_id"] == reg_id:
                code = r["course_code"]
                roll = r["roll_no"]
                registrations.remove(r)
                registered_rolls[code].remove(roll)
                print("Dropped Successfully")

                if waiting_list[code]:
                    w = waiting_list[code].pop(0)
                    self.register_waiting(code, w)
                return
        print("Registration ID Not Found")

    def register_waiting(self, code, w):
        global reg_counter
        name, roll, year, merit = w
        course = self.get_course(code)
        student = Student(name, roll, year, merit)
        fee_paid = self.calculate_fee(course, student)
        registrations.append({
            "reg_id": reg_counter,
            "course_code": code,
            "student_name": name,
            "roll_no": roll,
            "year": year,
            "fee_paid": fee_paid
        })
        registered_rolls[code].add(roll)
        print("Auto Registered from Waiting List:", name)
        reg_counter += 1

    def report(self):
        for c in courses:
            code = c[0]
            total = c[3]
            filled = len(registered_rolls[code])
            wait = len(waiting_list[code])
            fee = sum(r["fee_paid"] for r in registrations if r["course_code"] == code)
            print(code, "Total:", total, "Filled:", filled, "Waiting:", wait, "Fee:", fee)

    def search(self):
        ch = int(input("1.Search by Reg ID  2.Search by Course Code: "))
        if ch == 1:
            reg_id = int(input("Enter Reg ID: "))
            for r in registrations:
                if r["reg_id"] == reg_id:
                    print(r)
        else:
            code = input("Course Code: ")
            for r in registrations:
                if r["course_code"] == code:
                    print(r)

    def revenue(self):
        total_fee = sum(r["fee_paid"] for r in registrations)
        occ = 0
        for c in courses:
            occ += len(registered_rolls[c[0]]) / c[3]
        avg_occ = (occ / len(courses)) * 100
        print("Total Revenue:", total_fee)
        print("Average Occupancy:", avg_occ)

system = Registration()

while True:
    print("\n1.Register Student")
    print("2.Drop Course")
    print("3.Course Report")
    print("4.Search")
    print("5.Total Revenue & Occupancy")
    print("6.Exit")

    ch = int(input("Enter Choice: "))

    if ch == 1:
        system.register_student()
    elif ch == 2:
        system.drop_course()
    elif ch == 3:
        system.report()
    elif ch == 4:
        system.search()
    elif ch == 5:
        system.revenue()
    elif ch == 6:
        break