**#  Smart Career Recommender System  **

> An AI-powered **Career Guidance Platform** built with **Flask, MySQL, and Machine Learning** that recommends the most suitable career path for students based on a career test, skills, and resumes.  

---

## ✨ Features
- 🔐 Secure **user authentication** (Registration & Login)  
- 📝 **Career assessment test** with 24+ yes/no questions  
- 🤖 **ML-based predictions** using `model.pkl` + `encoder.pkl`  
- 📄 **Resume upload** (`.pdf`, `.docx`) with skill extraction  
- 📊 **Reports dashboard** to view predictions  
- 📈 **Power BI integration** for advanced analytics  

---

🔹 Frontend

HTML5, CSS3, Bootstrap – For user interface (login, dashboard, test pages)

🔹 Backend

Python (Flask) – Web framework

Flask-CORS – Cross-origin resource sharing

Werkzeug – Secure file handling

🔹 Database

MySQL – For storing user details, test results, and predictions

mysql-connector-python – To connect Flask with MySQL

🔹 Machine Learning

Scikit-learn – Model training & evaluation

XGBoost – Advanced model for predictions

Pandas & NumPy – Data handling & preprocessing

Pickle / Joblib – Model serialization (model.pkl, encoder.pkl)

🔹 Natural Language Processing (NLP)

spaCy – Resume text processing & skill extraction

PyPDF2 – Extract text from PDF resumes

docx2txt – Extract text from DOCX resumes

🔹 Utilities

Hashlib – Password hashing (security)

Datetime – Handling timestamps

OS – File & path handling

JSON – Skill-to-career mapping

🔹 Visualization

Power BI – Career trend dashboards & analytics
---

## 📂 Project Structure
Smart-Career-Recommender/
│
├── app.py # Main Flask app
├── model.pkl # Trained ML model
├── encoder.pkl # Label encoder
├── uploads/ # Uploaded resumes
├── templates/ # HTML pages
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── test.html
│ ├── reports.html
├── static/ # CSS / JS / Images
├── career_mapping.json # Resume skill-to-career mapping
├── requirements.txt # Dependencies
└── README.md # Documentation




---

---

---

## ⚡ Setup & Run

1. **Clone Repo**
   ```bash
   git clone https://github.com/Patil8554/Smart-Career-Recommender.git
   cd Smart-Career-Recommender
Create Virtual Environment

bash
Copy code
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Configure MySQL Database

sql
Copy code
CREATE DATABASE career_system;
(Add users and career_test_results tables as per schema in app.py)

Run App

bash
Copy code
python app.py
Open 👉 http://127.0.0.1:5000/        # copy this and open project

📊 Power BI Dashboard
Visual insights include:

Career trends

Skills vs career mapping

Territory-wise participation

Test response analytics

