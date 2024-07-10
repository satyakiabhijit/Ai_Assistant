import datetime
import pyttsx3
import speech_recognition as sr
import sys
import webbrowser
import random
import requests
import geocoder
import os
from sympy import sympify, SympifyError

# Configuration
<<<<<<< HEAD
API_KEY = "304530be4e148876f0eb5c9d3fc06a27"  # Hardcoded API key
ASSISTANT_NAME = "Jarvis"  # Default assistant name
=======
API_KEY = "YOUR API KEY"  # Hardcoded API key from OpenWeatherMap
ASSISTANT_NAME = "Jarvis"
>>>>>>> 2e2afd2ace1ed29c19d275722dad70e5b312df10

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
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't get that. Please try again.")
            speak("Sorry, I didn't get that. Please try again.")
            return ""
        except sr.RequestError as e:
            print(f"Sorry, there was an error during speech recognition: {e}")
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
        print(f"Error fetching weather: {e}")
        speak("Sorry, there was a network error fetching the weather data.")
    except KeyError as e:
        print(f"Error parsing weather data: {e}")
        speak("Sorry, there was an issue parsing the weather data.")

def list_voices():
    """List available TTS voices."""
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"{index + 1}: {voice.name}")
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


import random


def print_board(board):
    """
    Function to print the Tic-Tac-Toe board.
    """
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def check_win(board, player):
    """
    Function to check if the current player has won.
    """
    # Check rows
    for row in board:
        if all([cell == player for cell in row]):
            return True

    # Check columns
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True

    # Check diagonals
    if all([board[i][i] == player for i in range(3)]) or \
            all([board[i][2 - i] == player for i in range(3)]):
        return True

    return False


def is_board_full(board):
    """
    Function to check if the board is full.
    """
    return all([cell != " " for row in board for cell in row])


def ai_move(board, ai_player):
    """
    Function for the AI player to make a move.
    """
    # Simple strategy: random move
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == " ":
            board[row][col] = ai_player
            break


def tic_tac_toe():
    """
    Function to run the Tic-Tac-Toe game with AI.
    """
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']
    current_player = 0

    while True:
        print_board(board)
        player = players[current_player]

        if player == 'X':
            print(f"Player {player}, enter your move (row and column): ")
            # Get player input
            while True:
                try:
                    row = int(input("Row (1-3): ")) - 1
                    col = int(input("Column (1-3): ")) - 1
                    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
                        board[row][col] = player
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            print(f"AI Player {player} is making a move...")
            ai_move(board, player)

        # Check win condition
        if check_win(board, player):
            print_board(board)
            print(f"Congratulations! Player {player} wins!")
            break

        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch players
        current_player = 1 - current_player


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
        ASSISTANT_NAME = new_name
        speak(f"My name has been changed to {ASSISTANT_NAME}.")
    elif "list of voices" in command:
        voices = list_voices()
        speak("Here are the available voices:")
        for index, voice in enumerate(voices):
            speak(f"{index + 1}. {voice.name}")
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
    elif "evaluate" in command:
        expression = command.split("evaluate ")[-1].strip()
        result = evaluate_expression(expression)
        speak(f"The result of the expression {expression} is {result}")
    elif "i love you" in command:
        speak("Aww, thank you! I'm here to help you.")
    elif "open code" in command:
        speak("Opening Visual Studio Code...")
        os.system("code")
    elif "do you love me" in command:
        speak("I'm here to assist you. I'm not capable of love like humans.")
    elif "will you marry me" in command:
        speak("I'm flattered, but I'm not capable of marriage.")
    elif "who is siri" in command:
        speak("Siri is a virtual assistant created by Apple Inc.")
    elif "who is alexa" in command:
        speak("Alexa is a virtual assistant created by Amazon.")
    elif "who is cortana" in command:
        speak("Cortana is a virtual assistant created by Microsoft.")
    elif "who is google assistant" in command:
        speak("Google Assistant is a virtual assistant created by Google.")
    elif "who is jarvis" in command:
        speak(f"{ASSISTANT_NAME} is a virtual assistant created by Satyaki Abhijit.")
    elif "set an alarm" in command:
        speak("Sorry, I'm not capable of setting alarms.")
    elif "set a timer" in command:
        speak("Sorry, I'm not capable of setting timers.")
    elif "set a reminder" in command:
        speak("What should I remind you about?")
        reminder = listen()
        speak("When should I remind you?")
        reminder_time = listen()  # Here you might want to parse the time and set up a reminder logic
        speak(f"Reminder set for {reminder_time}: {reminder}")
    elif "send an email" in command:
        speak("Sorry, I'm not capable of sending emails.")
    elif "play a game" in command:
        speak("Sure, let's play a game. let's play Tic-Tac-Toe.")
        tic_tac_toe()
        sys.exit()
    elif "open calculator" in command:
        speak("Opening calculator...")
        os.system("calc")
        sys.exit()
    elif "open notepad" in command:
        speak("Opening Notepad...")
        os.system("notepad")
        sys.exit()
    elif "open command prompt" in command:
        speak("Opening Command Prompt...")
        os.system("cmd")
        sys.exit()
    elif "what is the capital of" in command:
        country = command.split("capital of ")[-1].strip()
        url = f"https://restcountries.com/v3.1/name/{country}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            capital = data[0]["capital"][0]  # Fixed the key access
            speak(f"The capital of {country} is {capital}.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching country data: {e}")
            speak("Sorry, there was a network error fetching the country data.")
        except (KeyError, IndexError) as e:
            print(f"Error parsing country data: {e}")
            speak("Sorry, there was an issue parsing the country data.")
    elif "play music" in command or "play a song" in command:
        speak("Playing music on YouTube...")
        webbrowser.open("https://www.youtube.com/watch?v=5qap5aO4i9A")
        sys.exit()
    elif "Who is the prime minister of" in command:
        country = command.split("prime minister of ")[-1].strip()
        url = f"https://restcountries.com/v3.1/name/{country}"
        try:
            rsponse = requests.get(url)
            response.raiseraise_for_status()
            data = response.json()
            prime_minister = data[0]["government"]["head of state"]
            speak(f'The prime minister of {country} is {prime_minister}.')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching country data: {e}")
            speak("Sorry, there was a network error fetching the country data.")
        except (KeyError, IndexError) as e:
            print(f'Error passing country data: {e}')
            speak("Sorry there was an error parsing the country data.")
    elif "Who is the president of" in command:
        country =command.split("president of ")[-1].strip()
        url = f"https://restcountries.com/v3.1/name/{country}"
        try:
            respose = requests.get(url)
            response.raiseraise_for_status()
            data = response.json()
            president = data[0]["government"]["head of state"]
            speak(f"The president of {country} is {president}.")
        except requests.exceptions.RequestException as e:
            print(f"Error feching country data: {e}")
            speak("Sorry, there was a network error fetching the country data.")
        except (KeyError, IndexError) as e:
            print(f"Error parsing country data: {e}")
            speak("Sorry, there was an issue parsing the country data.")
    elif "Who is the founder of" in command:
        company = command.split("founder of ")[-1].strip()
        url = f"https://restcountries.com/v3.1/name/{company}"
        try:
            response =requests.get(url)
            response.raiseraise_for_status()
            data = response.json()
            founder = data[0]["founder"]
            speak(f"The founder of {company} is {founder}.")
        except requests.exceptions.RequestException as e:
            print (f"Error fetching company data: {e}")
            speak("Sorry, there was a network error fetching the company data.")
        except (KeyError, IndexError) as e:
            print(f"Error parsing company data: {e}")
            speak("Sorry, there was an issue parsing the company data.")
    else:
        speak("Sorry, I didn't understand that command.")

# Main program loop
if __name__ == "__main__":
    while True:
        command = listen()
        if command:  # Check if command is not empty
            process_command(command)
