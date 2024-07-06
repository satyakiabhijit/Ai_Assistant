import datetime
import pyttsx3
import speech_recognition as sr
import sys
import webbrowser
import random
import requests
import geocoder
import os

# Initialize the recognizer and TTS engine
r = sr.Recognizer()
engine = pyttsx3.init()

# OpenWeatherMap API key from environment variable (replace with your method of securing the API key)
api_key = os.getenv('OPENWEATHERMAP_API_KEY')

# Assistant's name
assistant_name = "Jarvis"

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen and recognize speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = r.listen(source)

        try:
            print("Recognizing...")
            command = r.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't get that. Please try again.")
            return ""
        except sr.RequestError as e:
            print(f"Sorry, there was an error during speech recognition: {e}")
            return ""

# Function to get current location coordinates (latitude and longitude)
def get_current_location():
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng[0], g.latlng[1]
    else:
        return None, None

# Function to fetch weather data from OpenWeatherMap API based on coordinates
def fetch_weather(latitude, longitude):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        speak(f"The weather is currently {weather_description}.")
        speak(f"The temperature is {temperature:.1f} degrees Celsius.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        speak("Sorry, there was a network error fetching the weather data.")
    except KeyError as e:
        print(f"Error parsing weather data: {e}")
        speak("Sorry, there was an issue parsing the weather data.")

# Function to list available voices
def list_voices():
    voices = engine.getProperty('voices')
    voice_list = [(index, voice.name) for index, voice in enumerate(voices)]
    return voice_list

# Function to set voice by gender
def set_voice_by_gender(gender):
    voices = engine.getProperty('voices')
    for voice in voices:
        if gender in voice.name.lower():
            engine.setProperty('voice', voice.id)
            return True
    return False

#Function to evaluate mathematical expressions saflly
def evaluate_expression(expression):
    allowed_chars = "0123456789+-*/(). "
    if all(char in allowed_chars for char in expression):
        try:
            result = eval(expression)
            return result
        except Exception as e:
            return str(e)
    else:
        return "Invalid characters in expression."


# Function to process user commands
def process_command(command):
    global assistant_name
    if f"hello {assistant_name.lower()}" in command:
        speak("Hello! How can I assist you?")
    elif "what is your name" in command:
        speak(f"My name is {assistant_name}. I am your virtual assistant.")
    elif "who are you" in command:
        speak(f"I am {assistant_name}, your virtual assistant.")
    elif "how are you" in command:
        speak("I'm doing great! Thanks for asking.")
    elif "who created you" in command:
        speak("I was created by Satyaki Abhijit.")
    elif "what is the current time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    elif "what is the current date" in command or "date" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}")
    elif "what is my current location" in command:
        latitude, longitude = get_current_location()
        if latitude and longitude:
            speak(f"Your current location is latitude {latitude} and longitude {longitude}.")
        else:
            speak("Sorry, I couldn't determine your current location.")
    elif "what is the weather like" in command:
        speak("Fetching weather for your current location...")
        latitude, longitude = get_current_location()
        if latitude and longitude:
            fetch_weather(latitude, longitude)
        else:
            speak("Sorry, I couldn't determine your current location.")
    elif "tell me a joke" in command:
        speak("I'm not a comedian, but I can try to make you laugh!")
        jokes = [
            "I found a lion in my closet the other day! When I asked what it was doing there, it said 'Narnia business.'",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why did the snail paint a giant S on his car? So when he drove by, people could say: 'Look at that S car go!'",
            "Why was the math book sad? Because it had too many problems."
        ]
        speak(random.choice(jokes))
    elif "goodbye" in command:
        speak("Goodbye! Have a great day!")
        sys.exit()
    elif "open youtube" in command:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
        sys.exit()
    elif "search on youtube" in command:
        speak("What would you like to search for on YouTube?")
        search_query = listen()
        if search_query:
            speak(f"Searching for {search_query} on YouTube...")
            search_url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(search_url)
            sys.exit()
    elif "search on google" in command:
        speak("What would you like to search for on Google?")
        search_query = listen()
        if search_query:
            speak(f"Searching for {search_query} on Google...")
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
            sys.exit()
    elif "thanks" in command or "thank you" in command:
        speak("You're welcome! If you need any more help, feel free to ask.")
    elif "change your name to" in command:
        new_name = command.split("change your name to ")[-1].strip()
        assistant_name = new_name
        speak(f"My name has been changed to {assistant_name}.")
    elif "list of voices" in command:
        voices = list_voices()
        speak("Here are the available voices:")
        for index, name in voices:
            speak(f"{index + 1}. {name}")
    elif "change voice to male" in command:
        if set_voice_by_gender("male"):
            speak("Voice has been changed to male.")
        else:
            speak("Sorry, no male voices are available.")
    elif "change voice to female" in command:
        if set_voice_by_gender("female"):
            speak("Voice has been changed to female.")
        else:
            speak("Sorry, no female voices are available.")
    else:
        speak("Sorry, I didn't understand that command.")

# Main program loop
while True:
    command = listen()
    if command:  # Check if command is not empty
        process_command(command)
