from assistant.whisper_listener import listen
from assistant.brain import ask_nova
from assistant.speaker import speak


def start_conversation():

    print("Nova is ready. Speak to me.")

    while True:

        user_text = listen()

        if user_text:

            print("You:", user_text)

            if "exit" in user_text.lower() or "quit" in user_text.lower():
                speak("Goodbye. See you later.")
                break


            response = ask_nova(user_text)

            print("Nova:", response)

            speak(response)


if __name__ == "__main__":
    start_conversation()