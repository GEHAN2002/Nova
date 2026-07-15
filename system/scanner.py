import os
import json
import win32com.client


APP_DATABASE = "data/app.json"


def scan_start_menu():

    apps = {}

    shell = win32com.client.Dispatch("WScript.Shell")


    locations = [
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs")
    ]


    for location in locations:

        for root, dirs, files in os.walk(location):

            for file in files:

                if file.endswith(".lnk"):

                    name = file.replace(".lnk", "").lower().strip()

                    shortcut_path = os.path.join(root, file)

                    shortcut = shell.CreateShortcut(shortcut_path)

                    target = shortcut.TargetPath


                    if target and target.endswith(".exe"):

                        apps[name] = target



    # Add aliases
    aliases = {
        "chrome": "google chrome",
        "google": "google chrome",
        "vscode": "visual studio code",
        "vs code": "visual studio code",
        "edge": "microsoft edge"
    }


    for alias, real_name in aliases.items():

        for app_name, path in apps.items():

            if real_name in app_name:

                apps[alias] = path
                break



    os.makedirs("data", exist_ok=True)


    with open(APP_DATABASE, "w", encoding="utf-8") as f:

        json.dump(
            apps,
            f,
            indent=4
        )


    print(f"Found {len(apps)} applications")
    print("Database saved!")



if __name__ == "__main__":

    scan_start_menu()