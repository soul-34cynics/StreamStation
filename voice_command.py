# voice_command.py
import speech_recognition as sr
import pyttsx3
import webbrowser

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts = pyttsx3.init()

def speak(text):
    print("🎤 Bot:", text)
    tts.say(text)
    tts.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        speak("I'm listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("🗣️ You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
    except sr.RequestError as e:
        speak("Speech service is unavailable. Please check your internet connection.")
        print(f"Error: {e}")
    return ""

def open_browser(url):
    try:
        webbrowser.get().open_new(url)
    except webbrowser.Error:
        # Fallback to regular open
        webbrowser.open(url)

def main():
    speak("Voice Assistant Ready! Try saying: Play Perfect, Detect mood now, or Show videos.")
    while True:
        command = listen_command()

        if command:
            if "play perfect" in command:
                song = "perfect"
                speak(f"Playing {song}!")
                open_browser(f"http://127.0.0.1:5000/?autoplay={song}")

            elif "detect mood" in command:
                speak("Opening mood detector...")
                open_browser("http://127.0.0.1:5000/mood")

            elif "show videos" in command:
                speak("Taking you to the videos section...")
                open_browser("http://127.0.0.1:5000/videos")

            elif "exit" in command or "stop" in command:
                speak("Goodbye!")
                break

            else:
                speak("I didn't understand that. Please try a different command.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Exiting the voice assistant. Goodbye!")
    except Exception as e:
        speak("An unexpected error occurred.")
        print(f"Error: {e}")
