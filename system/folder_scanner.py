import os
import json


FOLDER_DATABASE = "data/folders.json"


def scan_folders():

    folders = {}

    home = os.path.expanduser("~")

    locations = [
        os.path.join(home, "Desktop"),
        os.path.join(home, "Documents"),
        os.path.join(home, "Downloads"),
        os.path.join(home, "Pictures"),
        os.path.join(home, "Videos")
    ]


    for location in locations:

        print("Checking:", location)

        if os.path.exists(location):

            name = os.path.basename(location).lower()

            folders[name] = location

            print("Added:", name)



    # Scan Desktop folders

    desktop = os.path.join(home, "Desktop")


    if os.path.exists(desktop):

        for item in os.listdir(desktop):

            path = os.path.join(desktop, item)


            if os.path.isdir(path):

                folders[item.lower()] = path

                print("Added desktop folder:", item)



    os.makedirs("data", exist_ok=True)


    with open(FOLDER_DATABASE, "w", encoding="utf-8") as f:

        json.dump(
            folders,
            f,
            indent=4
        )


    print("\nFound:", len(folders), "folders")
    print("Saved:", FOLDER_DATABASE)



if __name__ == "__main__":
    scan_folders()