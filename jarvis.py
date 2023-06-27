import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import smtplib
import webbrowser
import os
import requests
import json

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command

def play_song(song):
    talk('playing ' + song)
    pywhatkit.playonyt(song)

def get_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    talk('The current time is ' + current_time)

def get_date():
    current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
    talk('Today is ' + current_date)

def get_weather():
    api_key = '50245b2d3f0d67559e04921c8de63c13'  # Replace with your OpenWeatherMap API key

    talk("Which city's weather would you like to know?")
    city = take_command()  # Take user input for the city

    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}  # Request temperature in Celsius

    response = requests.get(base_url, params=params)
    weather_data = json.loads(response.text)

    if weather_data['cod'] == '404':
        talk("Sorry, I couldn't find the weather information for that city.")
    else:
        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']

        talk(f"The weather in {city} is {main_weather}. {description}.")
        talk(f"The temperature is {temperature} degrees Celsius.")
        talk(f"The humidity is {humidity}%.")

def greet():
    talk("Hello! My name is Jarvis. How may I help you?")

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        play_song(song)
    elif 'time' in command:
        get_time()
    elif 'date' in command:
        get_date()
    elif 'weather' in command:
        get_weather()
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        get_definition(person)
    elif 'are you single' in command:
        talk('I am in a relationship with Wi-Fi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'bye' in command:
        talk('Bye, See you Soon!')
        exit()
    else:
        talk('Please say the command again.')

greet()

while True:
    run_alexa()
