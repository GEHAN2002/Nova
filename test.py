from assistant.brain import ask_nova


while True:

    user = input("You: ")

    if user.lower() == "exit":
        break

    reply = ask_nova(user)

    print("Nova:", reply)