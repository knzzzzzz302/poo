from flask import request, jsonify
from management import app
from management.models import Student, Course

students = []
courses = []

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    student = Student(data['name'], data['id'], data['age'])
    students.append(student)
    return jsonify({"msg": "Student added"}), 201

@app.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    course = Course(data['name'], data['code'], data['credits'])
    courses.append(course)
    return jsonify({"msg": "Course added"}), 201

@app.route('/enrollments', methods=['POST'])
def enroll():
    data = request.get_json()
    student = next((s for s in students if s.student_id == data['id']), None)
    course = next((c for c in courses if c.code == data['code']), None)
    if student and course:
        course.enroll(student)
        return jsonify({"msg": "Enrollment successful"}), 201
    return jsonify({"error": "Student or course not found"}), 404

@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    student = next((s for s in students if s.student_id == id), None)
    return jsonify(student.to_dict()) if student else jsonify({"error": "Student not found"}), 404

@app.route('/courses/<code>', methods=['GET'])
def get_course(code):
    course = next((c for c in courses if c.code == code), None)
    return jsonify(course.to_dict()) if course else jsonify({"error": "Course not found"}), 404
