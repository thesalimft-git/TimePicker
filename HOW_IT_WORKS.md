# How TimePicker Works

## 📋 Overview

TimePicker is a Django REST Framework API for managing students, courses, and their calendar schedules. It allows you to:
- Manage student information
- Manage course information  
- Schedule time slots for courses with students

## 🏗️ Architecture

### Components

```
┌─────────────────┐
│   Models        │  ← Database structure (Student, Course, CalendarSlot)
└────────┬────────┘
         │
┌────────▼────────┐
│  Serializers    │  ← Convert models to/from JSON
└────────┬────────┘
         │
┌────────▼────────┐
│   ViewSets      │  ← Handle HTTP requests (GET, POST, PUT, DELETE)
└────────┬────────┘
         │
┌────────▼────────┐
│     URLs        │  ← Route requests to correct views
└─────────────────┘
```

## 📊 Data Models & Relationships

### 1. **Student Model**
Stores student information:
- `student_id` - Unique identifier
- `first_name`, `last_name` - Name
- `email` - Email address (unique)
- `phone` - Phone number (optional)

### 2. **Course Model**
Stores course information:
- `course_code` - Unique code (e.g., "CS101")
- `name` - Course name
- `description` - Course description
- `instructor` - Instructor name
- `credits` - Number of credits

### 3. **CalendarSlot Model**
Links students to courses with time information:
- `course` → **Foreign Key** to Course (required)
- `student` → **Foreign Key** to Student (optional)
- `day_of_week` - MON, TUE, WED, THU, FRI, SAT, SUN
- `start_time`, `end_time` - Time range
- `date` - Specific date (for one-time slots)
- `is_recurring` - Weekly recurring or one-time
- `room` - Room location
- `notes` - Additional notes

**Relationships:**
- One Course can have many CalendarSlots
- One Student can have many CalendarSlots
- CalendarSlot connects a Course to a Student at a specific time

## 🚀 How to Use

### 1. Start the Server

```bash
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000/`

### 2. API Endpoints

#### **Root Endpoint**
```
GET http://127.0.0.1:8000/
```
Returns API information and available endpoints.

#### **Students API**
```
GET    /api/students/          # List all students
POST   /api/students/          # Create a student
GET    /api/students/{id}/     # Get specific student
PUT    /api/students/{id}/     # Update student
DELETE /api/students/{id}/     # Delete student
```

#### **Courses API**
```
GET    /api/courses/           # List all courses
POST   /api/courses/           # Create a course
GET    /api/courses/{id}/      # Get specific course
PUT    /api/courses/{id}/      # Update course
DELETE /api/courses/{id}/      # Delete course
```

#### **Calendar Slots API**
```
GET    /api/calendar-slots/                    # List all slots
POST   /api/calendar-slots/                    # Create a slot
GET    /api/calendar-slots/{id}/               # Get specific slot
PUT    /api/calendar-slots/{id}/               # Update slot
DELETE /api/calendar-slots/{id}/               # Delete slot

# Custom Actions:
GET    /api/calendar-slots/by_course/?course_id=1
GET    /api/calendar-slots/by_student/?student_id=1
GET    /api/calendar-slots/by_day/?day=MON
```

## 📝 Example Usage

### Create a Student

**Request:**
```bash
POST http://127.0.0.1:8000/api/students/
Content-Type: application/json

{
  "student_id": "STU001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "123-456-7890"
}
```

**Response:**
```json
{
  "id": 1,
  "student_id": "STU001",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "123-456-7890",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Create a Course

**Request:**
```bash
POST http://127.0.0.1:8000/api/courses/
Content-Type: application/json

{
  "course_code": "CS101",
  "name": "Introduction to Computer Science",
  "description": "Basic programming concepts",
  "instructor": "Dr. Smith",
  "credits": 3
}
```

### Create a Calendar Slot

**Request:**
```bash
POST http://127.0.0.1:8000/api/calendar-slots/
Content-Type: application/json

{
  "course": 1,
  "student": 1,
  "day_of_week": "MON",
  "start_time": "09:00:00",
  "end_time": "10:30:00",
  "is_recurring": true,
  "room": "Room 101"
}
```

### Get All Slots for a Student

**Request:**
```bash
GET http://127.0.0.1:8000/api/calendar-slots/by_student/?student_id=1
```

### Search Students

**Request:**
```bash
GET http://127.0.0.1:8000/api/students/?search=john
```

## 🔍 Features

### 1. **Search & Filter**
- Search across multiple fields
- Filter by specific values
- Example: `/api/students/?search=john&email=john@example.com`

### 2. **Pagination**
- Results paginated (100 items per page)
- Use `?page=2` to get next page

### 3. **Browsable API**
- Visit any endpoint in browser for interactive API explorer
- Test endpoints directly from the web interface

### 4. **Validation**
- Email validation
- Unique constraints (student_id, email, course_code)
- Time validation (end_time must be after start_time)

## 🗄️ Database

- **Database**: SQLite (`db.sqlite3`)
- **Migrations**: Already applied
- **Admin Panel**: `/admin/` (create superuser with `python manage.py createsuperuser`)

## 🔄 Workflow Example

1. **Create a Student**
   ```bash
   POST /api/students/ → Get student ID (e.g., 1)
   ```

2. **Create a Course**
   ```bash
   POST /api/courses/ → Get course ID (e.g., 1)
   ```

3. **Schedule a Time Slot**
   ```bash
   POST /api/calendar-slots/
   {
     "course": 1,
     "student": 1,
     "day_of_week": "MON",
     "start_time": "09:00:00",
     "end_time": "10:30:00"
   }
   ```

4. **View Student's Schedule**
   ```bash
   GET /api/calendar-slots/by_student/?student_id=1
   ```

## 🛠️ Using with cURL

```bash
# Create student
curl -X POST http://127.0.0.1:8000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{"student_id":"STU001","first_name":"John","last_name":"Doe","email":"john@example.com"}'

# Get all students
curl http://127.0.0.1:8000/api/students/

# Get student by ID
curl http://127.0.0.1:8000/api/students/1/
```

## 🛠️ Using with Python requests

```python
import requests

# Create a student
response = requests.post('http://127.0.0.1:8000/api/students/', json={
    'student_id': 'STU001',
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john@example.com'
})
student = response.json()

# Get all courses
courses = requests.get('http://127.0.0.1:8000/api/courses/').json()
```

## 📚 Key Files

- `api/models.py` - Database models
- `api/serializers.py` - JSON conversion
- `api/views.py` - API endpoints logic
- `api/urls.py` - URL routing
- `config/urls.py` - Main URL configuration
- `config/settings.py` - Django settings

## 🎯 Summary

**TimePicker** is a REST API that lets you:
1. Manage students and courses
2. Schedule time slots connecting students to courses
3. Query schedules by student, course, or day
4. Use a browsable web interface or programmatic API

All endpoints support full CRUD operations (Create, Read, Update, Delete) and include search/filter capabilities.

