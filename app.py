from flask import Flask, render_template, redirect, request , url_for, send_file
from forms.job_form import JobForm
from forms.job_form import JobForm
from utils.accessibility import text_to_speech
from config import Config  # Import the Config class
from gtts import gTTS
import os
app = Flask(__name__)
app.config.from_object(Config)  # Load configurations

# In-memory list to store job postings
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy(app)

# Define the Job model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    salary_range = db.Column(db.String(50), nullable=True)
    skills = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    diversity_initiative = db.Column(db.Boolean, default=False)

# Home route
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upskill')
def upskill():
    return render_template('upskill.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Do something with the form data, e.g., send an email
        print(f"Name: {name}, Email: {email}, Message: {message}")
        return 'Form submitted successfully!'  # Consider redirecting to a thank-you page
    return render_template('contact.html')

# Job posting routes
@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form.get('job-title')
        company_name = request.form.get('company-name')
        location = request.form.get('location')
        job_type = request.form.get('job-type')
        salary_range = request.form.get('salary-range')
        skills = request.form.get('skills')
        description = request.form.get('description')
        diversity_initiative = 'diversity-initiative' in request.form

        # Create a new job object
        new_job = Job(
            title=title,
            company_name=company_name,
            location=location,
            job_type=job_type,
            salary_range=salary_range,
            skills=skills,
            description=description,
            diversity_initiative=diversity_initiative
        )

        # Add the job to the database
        db.session.add(new_job)
        db.session.commit()

        return redirect('/jobs')  # Redirect to the job list page

    return render_template('job_post.html')

@app.route('/jobs')
def job_list():
    # Fetch all jobs from the database
    all_jobs = Job.query.all()
    return render_template('job_list.html', jobs=all_jobs)

@app.route('/job')
def job():
    return render_template('job.html')

@app.route('/gethired')
def ghired():
    return render_template('getjob.html')
# Text-to-speech route for reading page content

@app.route('/getlist')
def getlist():
    all_jobs = Job.query.all()
    return render_template('getjob_list.html',jobs=all_jobs)

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data['text']
    
    tts = gTTS(text=text, lang='en')
    audio_file = 'output.mp3'
    tts.save(audio_file)
    
    return send_file(audio_file, mimetype='audio/mpeg', as_attachment=True)
@app.route('/delete-job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('job_list'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
