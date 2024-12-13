from flask import Flask, render_template, redirect, request, send_file
from forms.job_form import JobForm
from utils.accessibility import text_to_speech
from config import Config  # Import the Config class
from gtts import gTTS
import os
app = Flask(__name__)
app.config.from_object(Config)  # Load configurations

# In-memory list to store job postings
jobs = []

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/job')
def job():
    return render_template('job.html')
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
        return 'Form submitted successfully!'
    return render_template('contact.html')

# Job posting routes
@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    form = JobForm()
    if form.validate_on_submit():
        job = {
            'title': form.title.data,
            'description': form.description.data,
            'domain': form.domain.data
        }
        jobs.append(job)  # Add job to the list
        return redirect('/jobs')
    return render_template('job_post.html', form=form)

@app.route('/jobs')
def job_list():
    return render_template('job_list.html', jobs=jobs)

# Text-to-speech route (for specific text submissions)
@app.route('/text-to-speech', methods=['POST'])
def tts():
    text = request.form.get('text')
    audio_file = text_to_speech(text)
    return redirect(audio_file)

# Text-to-speech route for reading page content
@app.route('/read-aloud', methods=['POST'])
def read_aloud():
    text = request.form.get('text')
    audio_file = text_to_speech(text)
    return redirect(audio_file)
@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data['text']
    
    tts = gTTS(text=text, lang='en')
    audio_file = 'output.mp3'
    tts.save(audio_file)
    
    return send_file(audio_file, mimetype='audio/mpeg', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
