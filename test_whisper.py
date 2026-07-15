from assistant.whisper_listener import listen


while True:

    text = listen()

    if text:
        print("You:", text)