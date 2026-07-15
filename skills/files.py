import os
import json


FOLDER_DATABASE = "data/folders.json"
FILE_DATABASE = "data/files.json"



def load_json(file):

    if not os.path.exists(file):

        return {}


    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def open_folder(target):

    folders = load_json(FOLDER_DATABASE)

    target = target.lower().strip()


    for name, path in folders.items():

        if target in name or name in target:

            print("Opening folder:", path)

            os.startfile(path)

            return True


    return False



def find_file(target):

    files = load_json(FILE_DATABASE)

    target = target.lower()


    for name, path in files.items():

        if target in name:

            print("Opening file:", path)

            os.startfile(path)

            return True


    return False



def open_file_or_folder(target):


    if open_folder(target):

        return True


    if find_file(target):

        return True


    return False