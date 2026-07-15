import webbrowser


WEBSITE_MAP = {
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chat.openai.com"
}


def open_website(name):

    name = name.lower()

    remove_words = [
        "open",
        "go",
        "launch",
        "start",
        "visit"
    ]

    for word in remove_words:
        name = name.replace(word, "")

    name = name.strip()

    if name in WEBSITE_MAP:

        url = WEBSITE_MAP[name]

        webbrowser.open_new(url)

        print(f"Opening {name}")

        return True


    print("Website not found")

    return False