import webbrowser



WEBSITES = {

    "youtube": "https://www.youtube.com",

    "google": "https://www.google.com",

    "github": "https://github.com",

    "gmail": "https://mail.google.com"

}



def open_website(command):


    command = command.lower()


    for site, url in WEBSITES.items():


        if site in command:

            webbrowser.open(url)

            return f"Opening {site}"


    return None