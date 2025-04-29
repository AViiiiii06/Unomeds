import os
import time
import pyaudio
import playsound
from gtts import gTTS
import google.generativeai as genai
import speech_recognition as sr

# Configure Gemini API
genai.configure(api_key="AIzaSyBWhUT8W4Y9YQOKS-Ww8qYcd3R2TYfRbOw")  # 🔹 Replace with your actual Gemini API Key

# Define language for text-to-speech
lang = 'en'

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech and play it."""
    speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
    speech.save("response.mp3")
    playsound.playsound("response.mp3")
    os.remove("response.mp3")  # Cleanup after playing

def get_audio():
    """Capture and recognize user speech"""
    with sr.Microphone() as source:
        print("\n Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)

        try:
            said = recognizer.recognize_google(audio)
            print(f" You said: {said}")
            return said.lower()
        except sr.UnknownValueError:
            print(" Sorry, I didn't catch that. Please repeat.")
            return None
        except sr.RequestError:
            print(" Could not request results, check your internet connection.")
            return None

def chat_with_ai(user_input):
    """Send user input to Gemini AI and get a response."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        print(f" Gemini API Error: {e}")
        return "Sorry, I am having trouble responding right now."

# Main interaction loop
while True:
    user_input = get_audio()

    if user_input:
        if "stop" in user_input:  # Exit condition
            print(" Stopping program...")
            speak("Goodbye! Have a great day!")
            break

        ai_response = chat_with_ai(user_input)
        print(f" AI: {ai_response}")

        # Speak the AI's response
        speak(ai_response)