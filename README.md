# Healthcare Backend API

Django REST Framework based healthcare management system with JWT authentication.

## 🚀 Features

- User Authentication (Register & Login with JWT)
- Patient Management (Full CRUD operations)
- Doctor Management (Complete profile management)
- Patient-Doctor Assignment System
- User-specific data access control
- Comprehensive data validation

## 🛠️ Tech Stack

- **Backend**: Django 5.0.1
- **API**: Django REST Framework
- **Database**: PostgreSQL 18
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Language**: Python 3.13

## ⚙️ Installation

### 1. Clone repository
```bash
git clone https://github.com/AyushKhatri-Dev/healthcare-backend-api.git
cd healthcare-backend-api
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```sql
CREATE DATABASE healthcare_db;
```

### 5. Environment Variables
Create `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Start Server
```bash
python manage.py runserver
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - Login (returns JWT tokens)

### Patients (Protected)
- `POST /api/patients/` - Create patient
- `GET /api/patients/` - List all patients
- `GET /api/patients/{id}/` - Get patient details
- `PUT /api/patients/{id}/` - Update patient
- `DELETE /api/patients/{id}/` - Delete patient

### Doctors (Protected)
- `POST /api/doctors/` - Add doctor
- `GET /api/doctors/` - List all doctors
- `GET /api/doctors/{id}/` - Get doctor details
- `PUT /api/doctors/{id}/` - Update doctor
- `DELETE /api/doctors/{id}/` - Delete doctor

### Mappings (Protected)
- `POST /api/mappings/` - Assign doctor to patient
- `GET /api/mappings/` - List all mappings
- `GET /api/mappings/patient/{id}/` - Get patient's doctors
- `DELETE /api/mappings/{id}/` - Remove assignment

## 🔐 Authentication

Protected endpoints require JWT token in header:
```
Authorization: Bearer <access_token>
```

## 📊 Database Models

- **User**: Custom user with email authentication
- **Patient**: Patient records (linked to user)
- **Doctor**: Doctor profiles
- **PatientDoctorMapping**: Many-to-many relationships

## 🧪 Testing

All endpoints tested with Postman. APIs fully functional:
- ✅ User Registration & Login
- ✅ Patient CRUD Operations
- ✅ Doctor CRUD Operations
- ✅ Patient-Doctor Assignment

## 👨‍💻 Author

**Ayush Khatri**
- Echelon Institute of Technology
- B.Tech CSE (AI/ML), 2024-2028

---

**Assignment for Backend Developer Intern Position - WhatBytes**
