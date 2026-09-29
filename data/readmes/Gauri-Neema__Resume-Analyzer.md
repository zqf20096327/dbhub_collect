# AI Career Copilot

AI Career Copilot is an AI-powered Resume Analyzer and Career Assistance web application built using Python and Flask.

The application allows users to upload their resume in PDF or DOCX format, or paste their resume text manually. Based on the user's desired career role, the application analyzes the resume using Google Gemini AI and provides relevant skills, missing skills, a personalized learning roadmap, and interview questions.

## Features

- User Signup
- User Login
- User Logout
- Forgot Password
- Resume text input
- PDF resume upload
- DOCX resume upload
- AI-powered resume analysis
- Career-specific skill analysis
- Missing skill identification
- Personalized learning roadmap
- Interview question generation
- Analysis history
- Clear analysis history
- TiDB Cloud database integration
- Google Gemini API integration
- Simple and responsive user interface

## How the Application Works

1. User creates an account using the Signup page.
2. User logs in to the application.
3. User enters their resume manually or uploads a PDF/DOCX file.
4. User enters their desired career role, such as Backend Engineer.
5. The application extracts the resume content.
6. The resume and career goal are sent to Google Gemini AI.
7. Gemini analyzes the resume according to the selected career goal.
8. The application displays:
   - Relevant Skills
   - Missing Skills
   - Career Roadmap
   - Interview Questions
9. The analysis is stored in the database.
10. Users can view their previous analyses from the History page.
11. Users can also clear their analysis history.

## Tech Stack

- Python
- Flask
- SQLAlchemy
- MySQL
- TiDB Cloud
- Google Gemini API
- HTML
- CSS
- Jinja2
- PyPDF2
- python-docx

## Project Structure

Resume Analyzer/
│
├── app.py
├── ai.py
├── db.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
├── isrgrootx1.pem
│
├── static/
│   ├── style.css
│   └── images/
│       └── robot.png
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── history.html
│   ├── login.html
│   ├── signup.html
│   └── forgot_password.html
│
└── venv/

## Installation

First, clone the repository:

git clone <your-repository-url>

Move into the project directory:

cd "Resume Analyzer"

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows PowerShell:

.\venv\Scripts\Activate.ps1

Install the required dependencies:

pip install -r requirements.txt

## Environment Variables

The application uses environment variables for sensitive information such as the Gemini API key and database connection details.

Create a file named:

.env

inside the main project folder.

Add:

GEMINI_API_KEY=your_gemini_api_key

DATABASE_URL=your_database_url

Never upload the .env file to GitHub.

## Running the Application

Activate the virtual environment:

.\venv\Scripts\Activate.ps1

Start the Flask application:

python app.py

Then open the following address in your browser:

http://127.0.0.1:5000/

## AI Resume Analysis

The application uses Google Gemini AI to analyze resumes according to the user's career goal.

For example, if the user enters:

Backend Engineer

the AI focuses on backend-related skills and identifies relevant missing skills instead of treating every skill in the resume as equally important.

The AI generates four main sections:

### Skills

Relevant skills detected from the resume for the selected career goal.

### Missing Skills

Important skills that may be required for the selected career goal but are missing or insufficiently represented in the resume.

### Roadmap

A learning roadmap focused on the identified skill gaps.

### Interview Questions

Interview questions related to the target career role and the skills being analyzed.

## Database

The application uses SQLAlchemy for database operations.

The database is hosted using TiDB Cloud and uses a MySQL-compatible connection.

The application stores:

- User information
- Resume text
- AI analysis results

The main database tables are:

### Users

Stores user account information.

### Reports

Stores resume analysis reports associated with users.

## Resume File Support

The application supports:

- PDF files
- DOCX files
- Direct resume text input

PDF files are processed using PyPDF2.

DOCX files are processed using python-docx.

## Security

Sensitive configuration such as API keys and database credentials should be stored in the .env file.

The .env file is excluded from GitHub using .gitignore.

For production use, additional security improvements should be implemented, including:

- Password hashing
- Secure password reset using email verification
- OTP verification
- Session security
- Input validation
- Production database security

## Future Improvements

Possible future improvements include:

- ATS resume scoring
- Job recommendations
- Resume improvement suggestions
- Resume keyword optimization
- Job description comparison
- Skill-based job matching
- User profile management
- Email-based password reset
- OTP verification
- Secure password hashing
- Deployment to a cloud platform
- Improved UI and dashboard analytics

## Purpose of the Project

The purpose of AI Career Copilot is to help job seekers understand how their current resume matches their desired career path.

Instead of only analyzing the resume, the application connects the user's existing skills with their career goal and provides actionable information about missing skills, learning direction, and interview preparation.

## Author

Gauri Neema


A Resume Analyzer and AI Career Assistance Project built with Python, Flask, Gemini AI, and TiDB Cloud.