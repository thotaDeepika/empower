from gtts import gTTS
import os

def text_to_speech(text):
    if text:
        tts = gTTS(text=text, lang='en')  
        audio_file = "static/audio/output.mp3"  # Make sure the filename is correct
        tts.save(audio_file) 
        return "/static/audio/output.mp3" 
    else:
        return "Error: No text to speak." 