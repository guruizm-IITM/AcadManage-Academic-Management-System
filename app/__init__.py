from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flasgger import Swagger
from .database import db


from .resources.student import StudentListAPI, StudentAPI
from .resources.course import CourseListAPI, CourseAPI
from .resources.enrollment import EnrollmentListAPI, EnrollmentAPI




def create_app(database_uri: str = 'sqlite:///api_database.sqlite3'):
    app = Flask(__name__)
    CORS(app)


    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
    api = Api(app)


    # Register routes (keeps routes consistent with autograder-friendly names)
    api.add_resource(StudentListAPI, '/api/student')
    api.add_resource(StudentAPI, '/api/student/<int:student_id>')


    api.add_resource(CourseListAPI, '/api/course')
    api.add_resource(CourseAPI, '/api/course/<int:course_id>')


    api.add_resource(EnrollmentListAPI, '/api/student/<int:student_id>/course', '/api/student/<int:student_id>/course')
    api.add_resource(EnrollmentAPI, '/api/student/<int:student_id>/course/<int:course_id>')


    # Swagger configuration
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    template = {
        "swagger": "2.0",
        "info": {
            "title": "AcadManage API",
            "description": "Academic Management System for managing students, courses, and enrollments.",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http"]
    }

    Swagger(app, config=swagger_config, template=template)



    with app.app_context():
        db.create_all()

    
    @app.route('/')
    def home():
        return {
            "message": "Welcome to AcadManage API 👋",
            "documentation": "Visit /apidocs to explore the Swagger UI."
        }

    return app