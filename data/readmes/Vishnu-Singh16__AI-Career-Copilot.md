\# 🚀 AI Career Copilot



An AI-powered career assistant that analyzes resumes, identifies skill gaps, generates personalized learning roadmaps, and provides interview questions based on the user's target job role.



Built using \*\*Flask\*\*, \*\*SQLAlchemy\*\*, \*\*TiDB Cloud\*\*, and \*\*Groq LLM API\*\*.



\---



\## ✨ Features



\- 🔐 User Authentication (Sign Up / Login / Logout)

\- 📄 Resume Upload (PDF \& DOCX)

\- 📝 Resume Text Input

\- 🤖 AI Resume Analysis

\- 🎯 Role-Specific Skill Evaluation

\- 📊 Skill Gap Analysis

\- 🛣 Personalized Learning Roadmap

\- 💼 Interview Question Generation

\- 📚 Resume Analysis History

\- ☁️ Cloud Database using TiDB



\---



\## 🛠 Tech Stack



\### Backend

\- Python

\- Flask

\- SQLAlchemy



\### Database

\- TiDB Cloud (MySQL Compatible)



\### AI

\- Groq API

\- Llama Model (via OpenAI-compatible SDK)



\### Frontend

\- HTML

\- CSS

\- Jinja2 Templates



\### Other Libraries

\- PyPDF2

\- python-docx

\- python-dotenv

\- PyMySQL



\---



\## 📂 Project Structure



```

AI-Career-Copilot/

│

├── static/

│   └── style.css

│

├── templates/

│   ├── base.html

│   ├── login.html

│   ├── signup.html

│   ├── dashboard.html

│   └── history.html

│

├── ai.py

├── app.py

├── db.py

├── models.py

├── .env

├── .gitignore

└── README.md

```



\---



\## ⚙️ Installation



\### 1. Clone Repository



```bash

git clone https://github.com/Vishnu-Singh16/AI-Career-Copilot.git



cd AI-Career-Copilot

```



\---



\### 2. Create Virtual Environment



```bash

python -m venv .venv

```



Activate



Windows



```bash

.venv\\Scripts\\activate

```



Linux/Mac



```bash

source .venv/bin/activate

```



\---



\### 3. Install Dependencies



```bash

pip install -r requirements.txt

```



\---



\### 4. Create `.env`



Create a `.env` file in the project root.



```env

DATABASE\_URL=YOUR\_TIDB\_DATABASE\_URL



GROQ\_API\_KEY=YOUR\_GROQ\_API\_KEY



SECRET\_KEY=YOUR\_SECRET\_KEY

```



\---



\### 5. Run the Application



```bash

python app.py

```



Open



```

http://127.0.0.1:5000

```



\---



\## 🗄 Database Schema



\### Users



| Field | Type |

|-------|------|

| id | Integer |

| email | String |

| password | String |



\---



\### Reports



| Field | Type |

|-------|------|

| id | Integer |

| user\_id | Integer |

| resume\_text | Text |

| result | Text(JSON) |



\---



\## 📸 Screenshots



\### Login Page



\_Add screenshot here\_



\---



\### Dashboard



\_Add screenshot here\_



\---



\### Resume Analysis



\_Add screenshot here\_



\---



\### History



\_Add screenshot here\_



\---



\## 🚀 Future Improvements



\- Password Hashing

\- Forgot Password via Email

\- Resume Score

\- ATS Compatibility Score

\- Skill Progress Tracker

\- Resume Comparison

\- Multiple AI Models

\- Dark Mode

\- Docker Deployment



\---



\## 🔒 Environment Variables



Never upload your `.env` file.



Required variables:



```

DATABASE\_URL



GROQ\_API\_KEY



SECRET\_KEY

```



\---



\## 👨‍💻 Author



\*\*Vishnu Singh\*\*



GitHub: https://github.com/Vishnu-Singh16



\---



\## ⭐ If you found this project useful



Give this repository a ⭐ on GitHub.

