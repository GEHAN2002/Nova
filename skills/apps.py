import os


APPS = {

    "whatsapp": r"shell:AppsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",

    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",

    "notepad": "notepad",

    "calculator": "calc"

}


def open_app(command):

    command = command.lower()


    for app, path in APPS.items():

        if app in command:

            if app == "whatsapp":

                os.system(
                    f'explorer "{path}"'
                )

            elif app == "chrome":

                os.startfile(path)

            else:

                os.system(path)


            return f"Opening {app}"


    return None