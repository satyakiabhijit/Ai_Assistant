import tkinter as tk
import threading
import sys
import datetime
import pyttsx3
import speech_recognition as sr
import webbrowser
import random
import requests
import geocoder
from sympy import sympify, SympifyError

# Configuration
API_KEY = "304530be4e148876f0eb5c9d3fc06a27"  # Hardcoded API key
ASSISTANT_NAME = "Friday"  # Default assistant name

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a voice command and return it as text."""
    with sr.Microphone() as source:
        update_output("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            update_output("Recognizing...")
            command = recognizer.recognize_google(audio)
            update_output(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            update_output("Sorry, I didn't get that. Please try again.")
            speak("Sorry, I didn't get that. Please try again.")
            return ""
        except sr.RequestError as e:
            update_output(f"Sorry, there was an error during speech recognition: {e}")
            speak(f"Sorry, there was an error during speech recognition: {e}")
            return ""

def get_current_location():
    """Get the current geographic location coordinates."""
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng[0], g.latlng[1]
    return None, None

def fetch_weather(latitude, longitude):
    """Fetch weather data from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        speak(f"The weather is currently {weather_description}.")
        speak(f"The temperature is {temperature:.1f} degrees Celsius.")
    except requests.exceptions.RequestException as e:
        update_output(f"Error fetching weather: {e}")
        speak("Sorry, there was a network error fetching the weather data.")
    except KeyError as e:
        update_output(f"Error parsing weather data: {e}")
        speak("Sorry, there was an issue parsing the weather data.")

def list_voices():
    """List available TTS voices."""
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        update_output(f"{index + 1}: {voice.name}")
    return voices

def set_voice_by_gender(gender):
    """Set TTS voice by gender."""
    voices = engine.getProperty('voices')
    for voice in voices:
        if gender in voice.name.lower():
            engine.setProperty('voice', voice.id)
            return True
    return False

def evaluate_expression(expression):
    """Evaluate a mathematical expression safely."""
    try:
        result = sympify(expression)
        return result
    except SympifyError:
        return "Invalid expression."

def start_tic_tac_toe():
    """Start the Tic-Tac-Toe game."""
    game_window = tk.Toplevel(root)
    game_window.title("Tic-Tac-Toe")

    def reset_board():
        for row in range(3):
            for col in range(3):
                buttons[row][col].config(text="", state=tk.NORMAL)
        current_player[0] = "X"
        update_status()

    def update_status():
        status_label.config(text=f"Player {current_player[0]}'s turn")

    def check_win():
        for row in range(3):
            if all(buttons[row][col]['text'] == current_player[0] for col in range(3)):
                return True
        for col in range(3):
            if all(buttons[row][col]['text'] == current_player[0] for row in range(3)):
                return True
        if all(buttons[i][i]['text'] == current_player[0] for i in range(3)) or \
                all(buttons[i][2 - i]['text'] == current_player[0] for i in range(3)):
            return True
        return False

    def is_board_full():
        return all(buttons[row][col]['text'] != "" for row in range(3) for col in range(3))

    def on_button_click(row, col):
        if buttons[row][col]['text'] == "" and current_player[0]:
            buttons[row][col].config(text=current_player[0])
            if check_win():
                status_label.config(text=f"Player {current_player[0]} wins!")
                disable_buttons()
            elif is_board_full():
                status_label.config(text="It's a draw!")
                disable_buttons()
            else:
                current_player[0] = "O" if current_player[0] == "X" else "X"
                update_status()
                if game_mode[0] == "single" and current_player[0] == "O":
                    ai_move()

    def disable_buttons():
        for row in range(3):
            for col in range(3):
                buttons[row][col].config(state=tk.DISABLED)

    def ai_move():
        empty_cells = [(row, col) for row in range(3) for col in range(3) if buttons[row][col]['text'] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            buttons[row][col].config(text="O")
            if check_win():
                status_label.config(text="Player O (AI) wins!")
                disable_buttons()
            elif is_board_full():
                status_label.config(text="It's a draw!")
                disable_buttons()
            else:
                current_player[0] = "X"
                update_status()

    def select_mode(mode):
        game_mode[0] = mode
        start_game()

    def start_game():
        global status_label
        for widget in game_window.winfo_children():
            widget.destroy()

        for row in range(3):
            for col in range(3):
                buttons[row][col] = tk.Button(game_window, text="", font='Arial 20', width=5, height=2,
                                              command=lambda r=row, c=col: on_button_click(r, c))
                buttons[row][col].grid(row=row, column=col)

        status_label = tk.Label(game_window, text="Player X's turn", font='Arial 15')
        status_label.grid(row=3, column=0, columnspan=3)

        reset_button = tk.Button(game_window, text="Reset", font='Arial 15', command=reset_board)
        reset_button.grid(row=4, column=0, columnspan=3)

        update_status()

    buttons = [[None for _ in range(3)] for _ in range(3)]
    current_player = ["X"]
    game_mode = [""]

    tk.Label(game_window, text="Select Game Mode", font='Arial 15').pack()
    tk.Button(game_window, text="Single Player", font='Arial 15', command=lambda: select_mode("single")).pack()
    tk.Button(game_window, text="Multiplayer", font='Arial 15', command=lambda: select_mode("multi")).pack()



def process_command(command):
    """Process a voice command."""
    global ASSISTANT_NAME
    if f"hello {ASSISTANT_NAME.lower()}" in command:
        speak("Hello! How can I assist you?")
    elif "what is your name" in command:
        speak(f"My name is {ASSISTANT_NAME}. I am your virtual assistant.")
    elif "who are you" in command:
        speak(f"I am {ASSISTANT_NAME}, your virtual assistant.")
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
        jokes = [
            "I found a lion in my closet the other day! When I asked what it was doing there, it said 'Narnia business.'",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why did the snail paint a giant S on his car? So when he drove by, people could say: 'Look at that S car go!'",
            "Why was the math book sad? Because it had too many problems."
        ]
        speak(random.choice(jokes))
    elif "give me a motivational quote" in command or "motivate me" in command:
        quotes = [
            "Believe in yourself and all that you are.",
            "The only limit to our realization of tomorrow is our doubts of today.",
            "The future belongs to those who believe in the beauty of their dreams."
        ]
        speak(random.choice(quotes))
    elif "tell me a fact" in command:
        facts = [
            "The shortest war in history lasted only 38 minutes.",
            "A single cloud can weigh more than 1 million pounds.",
            "The first oranges weren't orange."
        ]
        speak(random.choice(facts))
    elif "goodbye" in command or "exit" in command or "bye" in command:
        speak("Goodbye! Have a great day!")
        root.destroy()
        sys.exit()
    elif "open youtube" in command:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
        sys.exit()
    elif "open google" in command:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")
        sys.exit()
    elif "open facebook" in command:
        speak("Opening Facebook...")
        webbrowser.open("https://www.facebook.com")
        sys.exit()
    elif "evaluate" in command:
        expression = command.replace("evaluate", "").strip()
        result = evaluate_expression(expression)
        speak(f"The result is {result}")
    elif "list voices" in command:
        speak("Listing available voices:")
        list_voices()
    elif "set voice to male" in command:
        if set_voice_by_gender("male"):
            speak("Voice set to male.")
        else:
            speak("Male voice not found.")
    elif "set voice to female" in command:
        if set_voice_by_gender("female"):
            speak("Voice set to female.")
        else:
            speak("Female voice not found.")
    elif "change name to" in command:
        new_name = command.replace("change name to", "").strip()
        ASSISTANT_NAME = new_name
        speak(f"My name has been changed to {ASSISTANT_NAME}.")
    elif "play tic_tac_toe" in command or "play a game" in command:
        speak("Starting Tic-Tac-Toe game...")
        start_tic_tac_toe()
        sys.exit()
    elif "thank you" in command or "thanks" in command:
        speak("You're welcome!")
        root.destroy()
        sys.exit()
    elif "help" in command or "what can you do" in command:
        speak("You can ask me the current time, date, weather, or to evaluate a mathematical expression.")
        start_voice_assistant()
    else:
        speak("Sorry, I didn't understand that command.")

def start_voice_assistant():
    """Start the voice assistant."""
    while True:
        command = listen()
        if command:
            process_command(command)

def update_output(message):
    """Update the output box with a new message."""
    output_box.config(state=tk.NORMAL)
    output_box.insert(tk.END, message + "\n")
    output_box.config(state=tk.DISABLED)
    output_box.see(tk.END)

def on_close():
    """Handle closing the GUI."""
    root.destroy()
    sys.exit()

# Initialize the main GUI window
root = tk.Tk()
root.title("Voice Assistant")

# Output box for displaying messages
output_box = tk.Text(root, state=tk.DISABLED, height=20, width=50)
output_box.pack(padx=10, pady=10)

# Close button
close_button = tk.Button(root, text="Close", command=on_close)
close_button.pack(pady=10)

# Start the voice assistant in a separate thread
assistant_thread = threading.Thread(target=start_voice_assistant)
assistant_thread.daemon = True
assistant_thread.start()

# Start the Tkinter event loop
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
