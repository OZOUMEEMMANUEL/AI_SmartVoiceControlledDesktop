import speech_recognition as sr
import pyttsx3
import pywhatkit
import random
try:
    import pyjokes
    def get_joke():
        return pyjokes.get_joke()
except Exception:
    # Fallback jokes if pyjokes is not installed or can't be imported
    def get_joke():
        jokes = [
            "I would tell you a joke about UDP, but you might not get it.",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "There are only 10 types of people in the world: those who understand binary and those who don't."
        ]
        return random.choice(jokes)
import webbrowser
from datetime import datetime
import time
import sys

# ========== SETTINGS ==========
user_name = "Brown"      # 🧍 Change this to your name if needed
assistant_name = "Brown V 001"  # Give your assistant a name too
# ==============================

def speak(text: str):
    """
    Use a fresh pyttsx3 engine per utterance to avoid Windows/SAPI issues
    where the engine speaks only once. Add a short pause so the mic
    doesn't pick up the assistant's own speech.
    """
    print(f"{assistant_name}: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("TTS error:", e)
    time.sleep(0.25)


def listen(timeout: float = 5.0, phrase_time_limit: float = 8.0) -> str:
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening... 🎧")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}\n")
            return command.lower()
        except sr.UnknownValueError:
            # No understandable speech
            return ""
        except sr.RequestError:
            speak("Network error. Please check your internet connection.")
            return ""
    except sr.WaitTimeoutError:
        # nothing heard in timeout
        return ""
    except Exception as e:
        print("Microphone/recognition error:", e)
        return ""


def greet_user():
    greetings = [
        f"Hey {user_name}, good to see you!",
        f"Hello {user_name}, ready to do some coding?",
        f"Hi {user_name}! How’s your day going?",
        f"Yo {user_name}! What’s up?"
    ]
    speak(random.choice(greetings))


def main():
    greet_user()
    while True:
        command = listen()
        if not command:
            # no command recognized; continue listening
            continue

        if "hello" in command:
            speak(f"Hi {user_name}! How are you doing today?")
        elif "your name" in command or "who are you" in command:
            speak(f"My name is {assistant_name}. I was built by you, {user_name}.")
        elif "time" in command:
            time_now = datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time_now}.")
        elif "open youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
        elif "open google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")
        elif "search" in command:
            query = command.replace("search", "").strip()
            if query:
                speak(f"Searching Google for {query}")
                try:
                    pywhatkit.search(query)
                except Exception as e:
                    speak("I couldn't complete the search.")
                    print("pywhatkit.search error:", e)
            else:
                speak("Please tell me what to search for.")
        elif "joke" in command:
            try:
                joke = get_joke()
                speak(joke)
            except Exception as e:
                speak("I couldn't get a joke right now.")
                print("joke error:", e)
        elif "stop" in command or "exit" in command or "quit" in command:
            speak(f"Goodbye {user_name}! Talk to you later.")
            break
        else:
            speak("Sorry, I don’t understand that yet.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Shutting down.")
        sys.exit(0)
