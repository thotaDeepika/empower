from flask import Flask, render_template, request
from gtts import gTTS


text = "DEMO TEXT" 

tts = gTTS(text=text, lang='hi')
tts.save("output.mp3")

app = Flask(__name__)

# Home route
@app.route('/')
def home():
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
        return 'Form submitted successfully!'
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

