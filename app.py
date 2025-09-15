from flask import Flask, request, redirect, url_for, render_template, session
import mysql.connector
import hashlib
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
import pickle
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, session
import datetime
import pandas as pd
import joblib
import spacy              # NLP library import
import json
import docx2txt
import PyPDF2

nlp = spacy.load("en_core_web_sm")
with open('career_mapping.json', 'r') as f:
    career_mapping = json.load(f)
all_skills = list({skill.lower() for skills in career_mapping.values() for skill in skills})


# Resume text extraction functions using nlp

def extract_text_from_pdf(path):
    text = ""
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_text_from_docx(path):
    return docx2txt.process(path)

# Skill extraction from text
def extract_skills(text):
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    matched_skills = list(set([token for token in tokens if token in all_skills]))
    return matched_skills

# Career suggestion logic
def suggest_career(skills_found):
    best_match = None
    max_matches = 0
    for career, skills_required in career_mapping.items():
        matches = len(set(skills_found).intersection(set(skills_required)))
        if matches > max_matches:
            max_matches = matches
            best_match = career
    return best_match if best_match else "No suitable career found"



app = Flask(__name__)
app.secret_key = 'saurabhpatil123!'  # unique key 



# Load model  encoder 
model = joblib.load('model.pkl')
encoder = joblib.load('encoder.pkl')


# Load trained model and label encoder
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)
   
@app.route('/predict', methods=['POST'])
def predict():
    answers = [1 if request.form.get(f'q{i+1}') == 'yes' else 0 for i in range(24)]

    # Load trained model and label encoder
    model = joblib.load('model.pkl')
    encoder = joblib.load('encoder.pkl')

    #  Convert answers to DataFrame to match training format
    input_data = pd.DataFrame([answers], columns=[f'q{i+1}' for i in range(24)])
    prediction = model.predict(input_data)[0]
    predicted_career = encoder.inverse_transform([prediction])[0]

    # Show prediction on reports page
    return render_template('reports.html', prediction=predicted_career)




# Upload folder path
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check allowed files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




# Upload route
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return ' Resume not found'

    file = request.files['resume']
    
    if file.filename == '':
        return ' No file selected'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            return ' Unsupported file type'

        # NLP skill extraction
        skills = extract_skills(text)
        career = suggest_career(skills)

        return render_template('resume_result.html', skills=skills, career=career)
    
    return ' Allowed file types: pdf, doc, docx'


# Serve uploaded file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



# MySQL connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Patil@123",
        database="career_db"
    )

# Home route
@app.route('/')
def home():
    return render_template("start.html")

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('fullName')
        email_or_mobile = request.form.get('emailOrMobile')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        role = request.form.get('role')

        # Simple server-side validation
        if password != confirm_password:
            return " Passwords do not match"

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users (full_name, email_or_mobile, password_hash, role)
                VALUES (%s, %s, %s, %s)
            """, (full_name, email_or_mobile, hashed_password, role))

            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/login')
        except mysql.connector.Error as err:
            return f" Error: {err}"

    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_mobile = request.form['email_or_mobile']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM users 
            WHERE email_or_mobile = %s AND password_hash = %s
        """, (email_or_mobile, hashed_password))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['username'] = user['full_name']
            return redirect('/dashboard')
        else:
            return " Invalid credentials"
    
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['username'])



# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Patil@123',
        database='career_db'
    )

# Route to display the test
@app.route('/test')
def test():
    return render_template('test.html')

# Route to handle form submission

@app.route('/submit_test', methods=['POST'])
def submit_test():
    username = session.get('username')
    answers = [request.form.get(f'q{i+1}') for i in range(24)]

    # Convert 'yes'/'no' to 1/0
    numeric_answers = [1 if ans == 'yes' else 0 for ans in answers]

    # Prediction
    input_data = pd.DataFrame([numeric_answers], columns=[f'q{i+1}' for i in range(24)])
    prediction = model.predict(input_data)[0]
    prediction = int(prediction)

    #  Career label
    career_label = encoder.inverse_transform([prediction])[0]

    # Insert into DB
    query = """
        INSERT INTO career_test_results 
        (username, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
         q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
         q21, q22, q23, q24, career_prediction, submitted_on)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, NOW())
    """
    values = [username] + answers + [career_label]

    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        return f" Database error: {err}"

    return redirect('/reports')



@app.route('/reports')
def reports():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM career_test_results 
        WHERE username = %s 
        ORDER BY submitted_on DESC 
        LIMIT 1
    """, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    predicted_career = None
    if result:
        answers = []
        for i in range(1, 25):
            answer = result[f'q{i}']
            answers.append(1 if answer == 'yes' else 0)

        input_data = np.array([answers])
        prediction = model.predict(input_data)
        predicted_career = label_encoder.inverse_transform(prediction)[0]

    return render_template('reports.html', result=result, predicted_career=predicted_career)
# Roadmap route
career_data = {
    "Data Scientist": {
        "skills": {
            "Python": [
                ("Python Basics & Syntax", "https://www.w3schools.com/python/python_intro.asp"),
                ("Variables, Data Types", "https://www.w3schools.com/python/python_variables.asp"),
                ("Conditional Statements", "https://www.w3schools.com/python/python_conditions.asp"),
                ("Functions", "https://www.w3schools.com/python/python_functions.asp"),
                ("OOP in Python", "https://www.w3schools.com/python/python_classes.asp")
            ],
            "Machine Learning": [
                ("ML Basics", "https://www.w3schools.com/python/python_ml_getting_started.asp"),
                ("Data Preprocessing", "https://www.w3schools.com/python/python_ml_data_preprocessing.asp")
            ]
        }
    },
    "Engineer": {
        "skills": {
            "C++": [
                ("Intro & Syntax", "https://www.w3schools.com/cpp/cpp_intro.asp"),
                ("Variables & Data Types", "https://www.w3schools.com/cpp/cpp_variables.asp"),
                ("OOP Concepts", "https://www.w3schools.com/cpp/cpp_oop.asp")
            ],
            "Java": [
                ("Java Basics", "https://www.w3schools.com/java/java_intro.asp"),
                ("OOP in Java", "https://www.w3schools.com/java/java_oop.asp")
            ]
        }
    }
}
@app.route('/roadmap')
def roadmap():
    career = request.args.get('career')
    return render_template('roadmap.html', career=career)


if __name__ == '__main__':
    app.run(debug=True)
    
