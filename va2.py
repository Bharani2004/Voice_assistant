import speech_recognition as sr
import datetime
import pyttsx3
import webbrowser
import pywhatkit

# Define the dataset with intents
dataset = {
    "intents": {
        "open_google": {
            "keywords": ["google", "chrome"],
            "response": "Opening Chrome...",
        },
        "get_time": {
            "keywords": ["time", "current time", "clock"],
            "response": "The current time is {}.",
        },
        "play_youtube": {
            "keywords": ["play", "YouTube", "video"],
            "response": "Playing a YouTube video...",
        },
        "open_youtube": {
            "keywords": ["YouTube"],
            "response": "Opening YouTube...",
        },
        "exit": {
            "keywords": ["end", "exit", "quit"],
            "response": "Exiting the voice assistant.",
        },
    }
}

def clear_background_noise(recognizer):
    with sr.Microphone(device_index=0) as source:
        print("Clearing background noises... Please wait")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

def recognize_speech(recognizer):
    with sr.Microphone(device_index=0) as source:
        print("Ask me anything")
        recorded_audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(recorded_audio, language='en_US').lower()
        print('Your message:', text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    return None

def speak_text(text, engine):
    engine.say(text)
    engine.runAndWait()

def main():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    recognizer = sr.Recognizer()

    while True:
        clear_background_noise(recognizer)
        text = recognize_speech(recognizer)

        if text:
            matched_intent = None
            for intent, data in dataset["intents"].items():
                for keyword in data["keywords"]:
                    if keyword in text:
                        matched_intent = intent
                        break
                if matched_intent:
                    break
            
            if matched_intent:
                response = dataset["intents"][matched_intent]["response"]
                if '{}' in response:
                    response = response.format(datetime.datetime.now().strftime('%I:%M %p'))
                print(response)
                speak_text(response, engine)

                if matched_intent == 'open_google':
                    print('Opening Chrome...')
                    webbrowser.open('https://www.google.com')
                elif matched_intent == 'play_youtube':
                    query = text.replace('play', '')
                    pywhatkit.playonyt(query)
                elif matched_intent == 'open_youtube':
                    print('Opening YouTube...')
                    webbrowser.open('https://www.youtube.com')
                elif matched_intent == 'exit':
                    print("Exiting the voice assistant.")
                    break

if __name__ == '__main__':
    main()
