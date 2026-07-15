import os
import subprocess

from system.database_manager import (
    load_database,
    search_folder,
    search_file
)


def find_app(name):

    apps = load_database("apps")

    name = name.lower().strip()


    if name in apps:
        return apps[name]


    for app_name, path in apps.items():

        if name in app_name:
            return path


    return None



def open_path(path):

    if os.path.exists(path):

        print("Opening:", path)

        os.startfile(path)

        return True


    return False



def open_anything(name):

    name = name.lower().strip()

    print("Searching:", name)

    # Core Windows folders work even before the first index has completed.
    known_folders = {
        "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
        "videos": os.path.join(os.path.expanduser("~"), "Videos"),
    }
    if name in known_folders and os.path.exists(known_folders[name]):
        return open_path(known_folders[name])


    # 1. Search application

    app_path = find_app(name)

    if app_path:

        print("Application found")

        return open_path(app_path)



    # 2. Search folder

    folder_path = search_folder(name)

    if folder_path:

        print("Folder found")

        return open_path(folder_path)



    # 3. Search file

    file_path = search_file(name)

    if file_path:

        print("File found")

        return open_path(file_path)



    print("Not found:", name)

    return False
