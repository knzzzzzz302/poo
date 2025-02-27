class Student:
    def __init__(self, name, student_id, age):
        self.name = name
        self.student_id = student_id
        self.age = age
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def get_average_grade(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0

    def to_dict(self):
        return {"name": self.name, "id": self.student_id, "age": self.age, "avg_grade": self.get_average_grade()}

class Course:
    def __init__(self, name, code, credits):
        self.name = name
        self.code = code
        self.credits = credits
        self.students = []

    def enroll(self, student):
        self.students.append(student)

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "credits": self.credits,
            "students": [s.to_dict() for s in self.students]
        }
