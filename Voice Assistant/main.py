import speech_recognition as sr
import pyttsx3
import openai
import webbrowser
import datetime

openai.api_key = "Enter your API key here"

recognizer = sr.Recognizer()
engine = pyttsx3.init()

conversation_history = []


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="en-US")
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Error: {e}")


def speak(text):
    engine.say(text)
    engine.runAndWait()


def get_gpt_response(prompt):
    conversation_history.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content.strip()})
    return response.choices[0].message.content.strip()


def process_command(command):
    command = command.lower()

    if "Goodbye!" in command or "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    elif "question" in command or "ask" in command:
        question = command.replace("question", "").replace("ask", "").strip()
        prompt = f"In Istanbul, {question}"
        answer = get_gpt_response(prompt)
        speak(answer)
    elif "search google for" in command:
        query = command.replace("search google for", "").strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Searching Google for {query}.")
    elif "what time is it" in command:
        now = datetime.datetime.now()
        speak(f"It is {now.hour}:{now.minute}")
    else:
        speak("I didn't understand.")


while True:
    command = listen()
    if command:
        process_command(command)