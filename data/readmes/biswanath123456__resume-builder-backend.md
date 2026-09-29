# Resume Builder - Full Stack Application

A production-ready full-stack resume builder application that allows users to create, manage, and customize professional resumes with real-time preview.

## 🚀 Features

- **User Authentication**: Secure JWT-based authentication with bcrypt password hashing
- **Resume Management**: Create, read, update, and delete multiple resumes
- **Dynamic Sections**: 
  - Education (multiple entries)
  - Work Experience (multiple entries)
  - Skills with proficiency levels
  - Projects with links
- **RESTful API**: Clean, well-documented API endpoints
- **Relational Database**: Properly normalized schema with cascade deletes
- **Production Ready**: Deployed on Railway with TiDB Cloud MySQL

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: MySQL (TiDB Cloud) / SQLite (development)
- **ORM**: SQLAlchemy 3.1
- **Authentication**: Flask-JWT-Extended
- **Password Hashing**: Flask-Bcrypt
- **Server**: Gunicorn (production)

### Frontend (Coming Soon)
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **HTTP Client**: Axios

## 📋 Prerequisites

- Python 3.11+
- pip
- Virtual environment (venv)
- MySQL database (TiDB Cloud) or SQLite for local development

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/resume-builder-backend.git
cd resume-builder-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:
```env
# Database Configuration
DATABASE_URL=sqlite:///instance/app.db
# For production MySQL:
# DATABASE_URL=mysql+pymysql://username:password@host:port/database?charset=utf8mb4

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
SECRET_KEY=your-super-secret-flask-key-change-this-in-production

# Flask Configuration
FLASK_ENV=development

# CORS Configuration
FRONTEND_URL=http://localhost:5173

# Port
PORT=5000
```

### 5. Run the Application
```bash
# Development
python run.py

# Production
gunicorn run:app --bind 0.0.0.0:5000
```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Base URL
```
Local: http://localhost:5000/api
Production: https://your-app.railway.app/api
```

### Endpoints

#### Authentication

**Register User**
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}

Response: 201 Created
{
  "message": "User registered successfully",
  "user": { "id": 1, "name": "John Doe", "email": "john@example.com" },
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

**Login**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}

Response: 200 OK
{
  "message": "Login successful",
  "user": { ... },
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

**Get Current User**
```http
GET /api/auth/me
Authorization: Bearer {access_token}

Response: 200 OK
{
  "user": { "id": 1, "name": "John Doe", "email": "john@example.com" }
}
```

#### Resumes

**Create Resume**
```http
POST /api/resumes/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Software Engineer Resume",
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "location": "San Francisco, CA",
  "linkedin": "https://linkedin.com/in/johndoe",
  "github": "https://github.com/johndoe",
  "summary": "Experienced software engineer...",
  "education": [
    {
      "institution": "Stanford University",
      "degree": "Bachelor of Science",
      "field_of_study": "Computer Science",
      "start_date": "2015",
      "end_date": "2019",
      "grade": "3.8 GPA"
    }
  ],
  "experience": [
    {
      "company": "Google",
      "position": "Software Engineer",
      "location": "Mountain View, CA",
      "start_date": "2019",
      "current": true,
      "description": "Working on search algorithms"
    }
  ],
  "skills": [
    {
      "name": "Python",
      "category": "Programming Languages",
      "proficiency": "Expert"
    }
  ],
  "projects": [
    {
      "name": "Resume Builder",
      "description": "Full-stack resume builder app",
      "technologies": "React, Flask, MySQL",
      "current": true,
      "github_url": "https://github.com/johndoe/resume-builder"
    }
  ]
}

Response: 201 Created
```

**Get All User Resumes**
```http
GET /api/resumes/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "resumes": [ ... ]
}
```

**Get Single Resume**
```http
GET /api/resumes/{resume_id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "resume": { ... }
}
```

**Update Resume**
```http
PUT /api/resumes/{resume_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Updated Title",
  "summary": "Updated summary"
}

Response: 200 OK
```

**Delete Resume**
```http
DELETE /api/resumes/{resume_id}
Authorization: Bearer {access_token}

Response: 200 OK
{
  "message": "Resume deleted successfully"
}
```

## 🗄️ Database Schema

### Users Table
```sql
- id (Primary Key)
- name (String, 100)
- email (String, 120, Unique, Indexed)
- password_hash (String, 255)
- created_at (DateTime)
- updated_at (DateTime)
```

### Resumes Table
```sql
- id (Primary Key)
- user_id (Foreign Key → users.id)
- title (String, 200)
- full_name (String, 100)
- email (String, 120)
- phone (String, 20)
- location (String, 100)
- linkedin (String, 200)
- github (String, 200)
- website (String, 200)
- summary (Text)
- created_at (DateTime)
- updated_at (DateTime)
```

### Education, Experience, Skills, Projects Tables
Each linked to `resumes.id` with cascade delete.

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Tests
```bash
pytest tests/test_auth.py -v
pytest tests/test_resume.py -v
```

### Manual API Testing
```bash
python test_api_manual.py
```

### Test Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

## 🚀 Deployment

### Railway Deployment

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git push -u origin main
```

2. **Create Railway Project**
- Go to [Railway](https://railway.app)
- Click "New Project" → "Deploy from GitHub repo"
- Select your repository

3. **Set Environment Variables**

In Railway Dashboard → Variables:
```
DATABASE_URL=mysql+pymysql://user:pass@host:port/db?charset=utf8mb4
JWT_SECRET_KEY=your-secret-key
SECRET_KEY=your-secret-key
FLASK_ENV=production
FRONTEND_URL=https://your-frontend-url.vercel.app
```

4. **Deploy**
Railway will automatically deploy. Your API will be available at:
```
https://your-app.up.railway.app
```

### TiDB Cloud Setup

1. Create account at [TiDB Cloud](https://tidbcloud.com)
2. Create a new Serverless cluster
3. Get connection string and add to Railway environment variables

## 📁 Project Structure
```
resume-builder-backend/
├── app/
│   ├── __init__.py           # App factory
│   ├── config.py             # Configuration
│   ├── models/               # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── resume.py
│   │   ├── education.py
│   │   ├── experience.py
│   │   ├── skill.py
│   │   └── project.py
│   ├── routes/               # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── resume.py
│   └── utils/                # Utilities
│       ├── __init__.py
│       └── decorators.py
├── tests/                    # Test files
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_resume.py
│   └── test_basic.py
├── instance/                 # SQLite database (dev)
├── .env                      # Environment variables
├── .gitignore
├── Procfile                  # Railway deployment
├── requirements.txt          # Dependencies
├── run.py                    # Application entry point
└── README.md
```

## 🔐 Security Features

- JWT token-based authentication
- Bcrypt password hashing
- Protected routes with token verification
- CORS configuration
- SQL injection prevention (SQLAlchemy ORM)
- Input validation

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author


Project Link: [https://github.com/biswanath123456/resume-builder-backend](https://github.com/biswanath123456/resume-builder-backend)

## 🙏 Acknowledgments

- Flask documentation
- SQLAlchemy documentation
- Railway deployment platform
- TiDB Cloud for MySQL database

## 📞 Support

For support, email biswanath2048@gmail.com or open an issue in the repository.

---

Made with ❤️ for building better resumes
