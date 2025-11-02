from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request
from flasgger import swag_from
from ..database import db
from ..models import Student
from ..exceptions import FoundError, NotGivenError


# ---------- Field mapping for marshalling ----------
student_fields = {
    "student_id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "roll_number": fields.String
}

# ---------- Request parser ----------
student_parse = reqparse.RequestParser()
student_parse.add_argument("first_name")
student_parse.add_argument("last_name")
student_parse.add_argument("roll_number")


# ---------- Student List API ----------
class StudentListAPI(Resource):
    @swag_from({
        'tags': ['Students'],
        'summary': 'Create a new student',
        'description': 'Add a new student record with first name, last name, and roll number.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'first_name': {'type': 'string', 'example': 'John'},
                        'last_name': {'type': 'string', 'example': 'Doe'},
                        'roll_number': {'type': 'string', 'example': 'CE001'}
                    },
                    'required': ['first_name', 'roll_number']
                }
            }
        ],
        'responses': {
            201: {'description': 'Student created successfully'},
            400: {'description': 'Missing required parameters'},
            409: {'description': 'Duplicate roll number'}
        }
    })
    @marshal_with(student_fields)
    def post(self):
        args = student_parse.parse_args()
        first_name = args.get('first_name', None)
        last_name = args.get('last_name', None)
        roll_number = args.get('roll_number', None)

        if roll_number is None:
            raise NotGivenError(status_code=400, error_code="STUDENT001", error_message="Roll Number is required")
        if first_name is None:
            raise NotGivenError(status_code=400, error_code="STUDENT002", error_message="First Name is required")

        student = Student.query.filter(Student.roll_number == roll_number).first()
        if student is not None:
            raise FoundError(status_code=409)

        student = Student(first_name=first_name, last_name=last_name, roll_number=roll_number)
        db.session.add(student)
        db.session.commit()
        return student, 201


# ---------- Student API (GET, PUT, DELETE) ----------
class StudentAPI(Resource):
    @swag_from({
        'tags': ['Students'],
        'summary': 'Get student by ID',
        'description': 'Retrieve a specific student record by ID.',
        'parameters': [
            {'name': 'student_id', 'in': 'path', 'type': 'integer', 'required': True, 'example': 1}
        ],
        'responses': {
            200: {'description': 'Student found and returned'},
            404: {'description': 'Student not found'}
        }
    })
    @marshal_with(student_fields)
    def get(self, student_id):
        student = Student.query.filter(Student.student_id == student_id).first()
        if student:
            return student
        else:
            raise FoundError(status_code=404)


    @swag_from({
        'tags': ['Students'],
        'summary': 'Update student by ID',
        'description': 'Modify the details of an existing student record.',
        'parameters': [
            {'name': 'student_id', 'in': 'path', 'type': 'integer', 'required': True, 'example': 1},
            {
                'name': 'body',
                'in': 'body',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'first_name': {'type': 'string', 'example': 'Jane'},
                        'last_name': {'type': 'string', 'example': 'Doe'},
                        'roll_number': {'type': 'string', 'example': 'CE002'}
                    }
                }
            }
        ],
        'responses': {
            200: {'description': 'Student updated successfully'},
            400: {'description': 'Missing required parameters'},
            404: {'description': 'Student not found'},
            409: {'description': 'Duplicate roll number'}
        }
    })
    @marshal_with(student_fields)
    def put(self, student_id):
        student = Student.query.filter(Student.student_id == student_id).first()
        if student is None:
            raise FoundError(status_code=404)

        args = student_parse.parse_args()
        first_name = args.get('first_name', None)
        last_name = args.get('last_name', None)
        roll_number = args.get('roll_number', None)

        if roll_number is None:
            raise NotGivenError(status_code=400, error_code="STUDENT001", error_message="Roll Number is required")
        if first_name is None:
            raise NotGivenError(status_code=400, error_code="STUDENT002", error_message="First Name is required")

        existing = Student.query.filter(Student.roll_number == roll_number, Student.student_id != student_id).first()
        if existing:
            raise FoundError(status_code=409)

        student.first_name = first_name
        student.last_name = last_name
        student.roll_number = roll_number
        db.session.add(student)
        db.session.commit()
        return student


    @swag_from({
        'tags': ['Students'],
        'summary': 'Delete student by ID',
        'description': 'Delete a specific student record using their ID.',
        'parameters': [
            {'name': 'student_id', 'in': 'path', 'type': 'integer', 'required': True, 'example': 1}
        ],
        'responses': {
            200: {'description': 'Student deleted successfully'},
            404: {'description': 'Student not found'}
        }
    })
    def delete(self, student_id):
        student = Student.query.filter(Student.student_id == student_id).first()
        if student is None:
            raise FoundError(status_code=404)
        db.session.delete(student)
        db.session.commit()
        return '', 200