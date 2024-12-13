from flask import Flask, render_template, redirect, request
from forms.job_form import JobForm
from utils.accessibility import text_to_speech
from config import Config  # Import the Config class

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

# Text-to-speech route for reading page content
@app.route('/read-aloud', methods=['POST'])
def read_aloud():
    text = request.form.get('text')
    audio_file = text_to_speech(text)
    return redirect(audio_file)

if __name__ == '__main__':
    app.run(debug=True)