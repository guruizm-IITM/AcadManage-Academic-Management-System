# 🎓 AcadManage API

AcadManage is a RESTful Academic Management API built with **Flask**, **Flask-RESTful**, **SQLAlchemy**, and **Flasgger** for interactive Swagger documentation.  
It manages students, courses, and enrollments — designed as a modular backend suitable for academic or learning management systems.

---

## 🚀 Features

- 👩‍🎓 **Student Management** – Add, update, fetch, and delete student records.
- 📚 **Course Management** – Manage course data via structured endpoints.
- 🔗 **Enrollment Management** – Link students and courses with proper validation.
- 🧩 **Modular Architecture** – Organized folder structure for scalability.
- 📜 **Interactive API Docs** – Integrated Swagger UI for live endpoint testing.
- 🗄️ **SQLite Database** – Lightweight, file-based database for rapid development.

---

## 🏗️ Project Structure

```
AcadManage/
│
├── app/
│   ├── __init__.py          # Initializes Flask app, routes, and Swagger
│   ├── database.py          # SQLAlchemy database instance
│   ├── models.py            # Student, Course, Enrollment models
│   ├── utils.py             # Custom error classes
│   ├── resources/           # RESTful API resources
│   │   ├── student.py
│   │   ├── course.py
│   │   └── enrollment.py
│   └── ...
│
├── main.py                  # Entry point of the application
└── requirements.txt         # Dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/AcadManage.git
cd AcadManage
```

### 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application
```bash
python main.py
```

By default, the server runs at:
```
http://127.0.0.1:5000/
```

---

## 📚 API Documentation

Visit **Swagger UI** at:

👉 [http://127.0.0.1:5000/docs/](http://127.0.0.1:5000/docs/)

You can test all endpoints directly from this interface!

---

## 🧠 Example Endpoints

### 👩‍🎓 Students
| Method | Endpoint | Description |
|---------|-----------|-------------|
| `POST` | `/api/student` | Create a new student |
| `GET` | `/api/student/<student_id>` | Retrieve student details |
| `PUT` | `/api/student/<student_id>` | Update a student's information |
| `DELETE` | `/api/student/<student_id>` | Delete a student |

### 📚 Courses
| Method | Endpoint | Description |
|---------|-----------|-------------|
| `POST` | `/api/course` | Create a new course |
| `GET` | `/api/course/<course_id>` | Get course details |
| `PUT` | `/api/course/<course_id>` | Update course info |
| `DELETE` | `/api/course/<course_id>` | Delete a course |

### 🔗 Enrollments
| Method | Endpoint | Description |
|---------|-----------|-------------|
| `POST` | `/api/student/<student_id>/course` | Enroll a student in a course |
| `GET` | `/api/student/<student_id>/course/<course_id>` | View enrollment details |
| `DELETE` | `/api/student/<student_id>/course/<course_id>` | Unenroll a student |

---

## 🧰 Technologies Used

- **Python 3.10+**
- **Flask**
- **Flask-RESTful**
- **Flask-SQLAlchemy**
- **Flasgger (Swagger UI)**
- **Flask-CORS**

---

## 🧩 Error Handling

Custom error classes for cleaner responses:

- `FoundError` – Raised when duplicate or conflicting entries are found.
- `NotGivenError` – Raised when required fields are missing.

Example response:
```json
{
  "error_code": "STUDENT001",
  "error_message": "Roll Number is required",
  "status": 400
}
```

---

## 🧑‍💻 Author

**Abhishek Guru**  
📍 IIT Madras | Data Science & AI  
🌐 [LinkedIn](https://linkedin.com/in/) • [GitHub](https://github.com/your-username)

---

## 🏁 License

This project is licensed under the **MIT License**.  
Feel free to modify and reuse it for your own educational or development purposes.

---
