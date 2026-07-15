import os
import subprocess

from system.database_manager import (
    load_database,
    search_folder,
    search_file
)


def open_path(path):

    if os.path.exists(path):

        print("Opening:", path)

        os.startfile(path)

        return True

    return False



def search_app(name):

    apps = load_database("apps")

    name = name.lower().strip()


    # exact match
    if name in apps:
        return apps[name]


    # partial match
    for app_name, path in apps.items():

        if name in app_name:
            return path


    return None



def open_app(name):

    path = search_app(name)

    if path:
        return open_path(path)

    return False



def open_anything(name):

    name = name.lower().strip()


    print("Searching Nova database:", name)


    # 1. Application
    app = search_app(name)

    if app:

        print("Found application")

        return open_path(app)



    # 2. Folder
    folder = search_folder(name)

    if folder:

        print("Found folder")

        return open_path(folder)



    # 3. File
    file = search_file(name)

    if file:

        print("Found file")

        return open_path(file)



    print("Nothing found:", name)

    return False