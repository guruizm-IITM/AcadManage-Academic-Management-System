from flask_restful import Resource, fields, marshal_with, reqparse
from ..database import db
from ..models import Course
from ..exceptions import FoundError, NotGivenError


course_fields = {
    "course_id": fields.Integer,
    "course_name": fields.String,
    "course_code": fields.String,
    "course_description": fields.String
}


course_parse = reqparse.RequestParser()
course_parse.add_argument("course_name")
course_parse.add_argument("course_code")
course_parse.add_argument("course_description")


class CourseListAPI(Resource):
    @marshal_with(course_fields)
    def post(self):
        args = course_parse.parse_args()
        course_name = args.get('course_name', None)
        course_code = args.get('course_code', None)
        course_description = args.get('course_description', None)


        if course_name is None:
            raise NotGivenError(status_code=400, error_code="COURSE001", error_message="Course Name is required")
        if course_code is None:
            raise NotGivenError(status_code=400, error_code="COURSE002", error_message="Course Code is required")


        course = Course.query.filter(Course.course_code == course_code).first()
        if course is not None:
            raise FoundError(status_code=409)


        course = Course(course_name=course_name, course_code=course_code, course_description=course_description)
        db.session.add(course)
        db.session.commit()
        return course, 201




class CourseAPI(Resource):
    @marshal_with(course_fields)
    def get(self, course_id):
        course = Course.query.filter(Course.course_id == course_id).first()
        if course:
            return course
        else:
            raise FoundError(status_code=404)


    @marshal_with(course_fields)
    def put(self, course_id):
        course = Course.query.filter(Course.course_id == course_id).first()
        if course is None:
            raise FoundError(status_code=404)


        args = course_parse.parse_args()
        course_name = args.get('course_name', None)
        course_code = args.get('course_code', None)
        course_description = args.get('course_description', None)


        if course_name is None:
            raise NotGivenError(status_code=400, error_code="COURSE001", error_message="Course Name is required")
        if course_code is None:
            raise NotGivenError(status_code=400, error_code="COURSE002", error_message="Course Code is required")


        existing = Course.query.filter(Course.course_code == course_code, Course.course_id != course_id).first()
        if existing:
            raise FoundError(status_code=409)


        course.course_name = course_name
        course.course_code = course_code
        course.course_description = course_description
        db.session.add(course)
        db.session.commit()
        return course


    def delete(self, course_id):
        course = Course.query.filter(Course.course_id == course_id).first()
        if course is None:
            raise FoundError(status_code=404)
        db.session.delete(course)
        db.session.commit()
        return '', 200