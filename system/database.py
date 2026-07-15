import json

APP_DATABASE = "data/app.json"


def find_app(name):

    with open(APP_DATABASE, "r", encoding="utf-8") as file:
        apps = json.load(file)

    name = name.lower()

    for app, path in apps.items():

        if name in app:
            return path

    return None


if __name__ == "__main__":

    result = find_app("chrome")

    if result:
        print("Found:")
        print(result)
    else:
        print("Application not found")