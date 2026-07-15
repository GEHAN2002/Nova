from assistant.whisper_listener import listen as whisper_listen


def listen():

    print("🎤 Nova is listening...")

    text = whisper_listen()


    if not text:
        return ""


    text = text.lower().strip()


    # Remove wake word
    text = text.replace("nova", "").strip()


    # Common Whisper mistakes correction
    corrections = {
        "what's up": "whatsapp",
        "whats up": "whatsapp",
        "what app": "whatsapp",
        "what apps": "whatsapp",
        "water sap": "whatsapp",
        "watts app": "whatsapp",

        "google chrome": "chrome",
        "chrom": "chrome",

        "note pad": "notepad",
        "calculator": "calculator"
    }


    for wrong, correct in corrections.items():

        if wrong in text:
            text = text.replace(
                wrong,
                correct
            )


    print("✅ Final command:", text)


    return text