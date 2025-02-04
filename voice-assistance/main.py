import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import time
import webbrowser

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 160)  # Set speed of speech

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen_command():
    """Listen to user command via microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"🎙️ You said: {command}")
            return command
        except sr.UnknownValueError:
            print("😕 Sorry, I didn't understand.")
            return ""
        except sr.RequestError:
            print("❌ Could not request results.")
            return ""
        except sr.WaitTimeoutError:
            print("⌛ Timeout, please speak again.")
            return ""

def play_music_on_youtube(song_name):
    """Searches and plays music on YouTube"""
    speak(f"Playing {song_name} on YouTube.")
    print(f"🎵 Playing: {song_name}")
    pywhatkit.playonyt(song_name)

def set_alarm(time_str):
    """Sets an alarm at the given time"""
    speak(f"Setting alarm for {time_str}.")
    print(f"⏰ Alarm set for: {time_str}")

    # Convert string time to hour and minute
    try:
        alarm_time = datetime.datetime.strptime(time_str, "%I:%M %p").time()
        while True:
            now = datetime.datetime.now().time()
            if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
                speak("Wake up! Your alarm is ringing.")
                webbrowser.open("https://www.youtube.com/watch?v=UceaB4D0jpo")  # Play alarm sound on YouTube
                break
            time.sleep(30)  # Check every 30 seconds
    except ValueError:
        speak("Invalid time format. Please say time in HH:MM AM or PM format.")

def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen_command()

        if "play" in command:
            song = command.replace("play", "").strip()
            if song:
                play_music_on_youtube(song)
            else:
                speak("Please specify the song name.")

        elif "set alarm for" in command:
            time_part = command.replace("set alarm for", "").strip()
            set_alarm(time_part)

        elif "exit" in command or "quit" in command:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("Sorry, I didn't understand. Please try again.")

if __name__ == "__main__":
    main()
