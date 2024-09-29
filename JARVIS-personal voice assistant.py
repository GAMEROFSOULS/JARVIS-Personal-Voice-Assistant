import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess
from datetime import datetime, timedelta
from threading import Timer

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()  # Ensure the speech engine processes the text

def open_website(url, name):
    webbrowser.open(url)
    speak(f"Opening {name}")

def play_music(playlist_url):
    webbrowser.open(playlist_url)
    speak("Playing music from your playlist")

def set_alarm(time_str):
    try:
        alarm_time = datetime.strptime(time_str, '%H:%M')
        now = datetime.now()
        alarm_datetime = datetime.combine(now.date(), alarm_time.time())
        if alarm_datetime < now:
            alarm_datetime += timedelta(days=1)
        delta = (alarm_datetime - now).total_seconds()
        Timer(delta, lambda: speak("Alarm ringing!")).start()
        speak(f"Alarm set for {time_str}")
    except ValueError:
        speak("Invalid time format. Please use HH:MM.")

def shutdown_laptop():
    speak("Shutting down the laptop.")
    os.system("shutdown /s /t 1")

def close_window():
    speak("Closing the window.")
    subprocess.run("taskkill /im chrome.exe /f", shell=True)  # Example for closing Chrome; we can adjust for other apps.

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Searching Google for {query}")

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        with sr.Microphone() as source:
            print("Listening jarvis sir ...")
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
                command = recognizer.recognize_google(audio).lower()
                print("You said: " + command)

                if "open google" in command:
                    open_website("https://www.google.com", "Google")
                elif "open facebook" in command:
                    open_website("https://www.facebook.com", "Facebook")
                elif "open linkedin" in command:
                    open_website("https://www.linkedin.com", "LinkedIn")
                elif "open twitter" in command:
                    open_website("https://www.twitter.com", "Twitter")
                elif "play music" in command:
                    play_music("https://www.youtube.com/watch?v=KgpFBdapobY&list=PLFf8TzRO75ohtOvfHmKUlblBiLZqUX2Kw")  # Replace with your playlist URL
                elif "set alarm" in command:
                    time_str = command.split("set alarm for")[-1].strip()
                    set_alarm(time_str)
                elif "off the laptop" in command:
                    shutdown_laptop()
                    speak("off the laptop")
                elif "close window" in command:
                    close_window()
                elif "search google" in command:
                    query = command.split("search google for")[-1].strip()
                    search_google(query)
                else:
                    speak("Sorry, I didn't understand that command.")

            except sr.UnknownValueError:
                speak("Can you repeat that again, sir?")
            except sr.RequestError as e:
                speak(f"Error; {e}")
            except Exception as e:
                speak(f"An unexpected error occurred; {e}")
