from flask_restful import Resource, reqparse
from ..database import db
from ..models import Student, Course, Enrollment
from ..utils import FoundError, NotGivenError

class EnrollmentListAPI(Resource):
    def get(self, student_id):
        """List all courses the student is enrolled in."""
        student = Student.query.get(student_id)
        if not student:
            raise FoundError(f"Student with ID {student_id} not found")

        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        return [{"course_id": e.course_id, "enrollment_date": e.enrollment_date.isoformat()} for e in enrollments], 200

    def post(self, student_id):
        """Enroll the student in a new course."""
        parser = reqparse.RequestParser()
        parser.add_argument("course_id", type=int, required=True, help="Course ID is required")
        args = parser.parse_args()

        course = Course.query.get(args["course_id"])
        if not course:
            raise FoundError(f"Course with ID {args['course_id']} not found")

        existing = Enrollment.query.filter_by(student_id=student_id, course_id=args["course_id"]).first()
        if existing:
            raise FoundError("Student already enrolled in this course")

        new_enrollment = Enrollment(student_id=student_id, course_id=args["course_id"])
        db.session.add(new_enrollment)
        db.session.commit()
        return {"message": "Enrollment created successfully"}, 201


class EnrollmentAPI(Resource):
    def get(self, student_id, course_id):
        """Get details of a specific enrollment."""
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if not enrollment:
            raise FoundError("Enrollment not found")

        return {"student_id": student_id, "course_id": course_id, "enrollment_date": enrollment.enrollment_date.isoformat()}, 200

    def delete(self, student_id, course_id):
        """Unenroll a student from a course."""
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if not enrollment:
            raise FoundError("Enrollment not found")

        db.session.delete(enrollment)
        db.session.commit()
        return {"message": "Enrollment deleted successfully"}, 200
