import os


def execute_command(command):

    command = command.lower()


    if "open chrome" in command:

        os.startfile(
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        )

        return "Opening Chrome"


    elif "open calculator" in command:

        os.system("calc")

        return "Opening calculator"


    elif "open notepad" in command:

        os.system("notepad")

        return "Opening Notepad"


    else:

        return None