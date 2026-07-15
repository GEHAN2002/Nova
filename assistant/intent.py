OPEN_WORDS = [
    "open",
    "start",
    "launch",
    "go",
    "show",
    "find",
    "bring"
]


REMOVE_WORDS = [
    "please",
    "my",
    "the",
    "a",
    "an",
    "folder",
    "file",
    "application"
]


def clean_target(text):

    words = text.split()

    cleaned = []

    for word in words:

        if word not in REMOVE_WORDS:

            cleaned.append(word)


    return " ".join(cleaned)



def extract_intent(command):

    command = command.lower()


    action = None


    for word in OPEN_WORDS:

        if word in command:

            action = "open"

            command = command.replace(
                word,
                ""
            )


    target = clean_target(command.strip())


    return {
        "action": action,
        "target": target
    }