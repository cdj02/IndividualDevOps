import os
from pymongo import MongoClient

mongo_uri = os.environ.get('MONGO_URI', 'mongodb://mongo:27017')
client = MongoClient(mongo_uri)
db = client['student_db']
student_db = db['students']

def add(student=None):
    res = student_db.find_one({"first_name": student.first_name, "last_name": student.last_name})
    if res:
        return 'already exists', 409

    student_dict = student.to_dict()

    count = student_db.count_documents({})
    student_dict['student_id'] = count + 1
    
    student_db.insert_one(student_dict)
    return student_dict['student_id']

def get_by_id(student_id=None, subject=None):
    student = student_db.find_one({"student_id": int(student_id)})
    if not student:
        return 'not found', 404
    student.pop('_id', None)
    return student

def delete(student_id=None):
    res = student_db.delete_one({"student_id": int(student_id)})
    if res.deleted_count == 0:
        return 'not found', 404
    return student_id

def get_average_grade(student_id):
    student = student_db.find_one({"student_id": int(student_id)})
    
    if not student or not student.get('grade_records'):
        return 'not found', 404
    
    grades = [float(g['grade']) for g in student['grade_records']]
    return sum(grades) / len(grades)