import json
import os


DATA_FOLDER = "data"


FILES = {
    "apps": "data/app.json",
    "folders": "data/folders.json",
    "files": "data/files.json"
}



def load_database(database):

    path = FILES[database]

    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



def save_database(database, data):

    path = FILES[database]

    os.makedirs(DATA_FOLDER, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4
        )



# ---------- FOLDERS ----------


def add_folder(name, path):

    folders = load_database("folders")

    folders[name.lower()] = path

    save_database(
        "folders",
        folders
    )



def remove_folder(name):

    folders = load_database("folders")

    name = name.lower()

    if name in folders:

        del folders[name]

        save_database(
            "folders",
            folders
        )



# ---------- FILES ----------


def add_file(name, path):

    files = load_database("files")

    files[name.lower()] = path

    save_database(
        "files",
        files
    )



def remove_file(name):

    files = load_database("files")

    name = name.lower()

    if name in files:

        del files[name]

        save_database(
            "files",
            files
        )



# ---------- SEARCH ----------


def search_folder(name):

    folders = load_database("folders")

    name = name.lower()

    # direct match
    if name in folders:
        return folders[name]


    # word matching
    search_words = name.split()


    for folder_name, path in folders.items():

        folder_words = folder_name.split()


        matches = 0


        for word in search_words:

            if word in folder_words or word in folder_name:

                matches += 1


        if matches > 0:

            return path


    return None



def search_file(name):

    files = load_database("files")

    name = name.lower()

    for key, path in files.items():

        if name in key:
            return path

    return None