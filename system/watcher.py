import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from system.database_manager import (
    add_folder,
    remove_folder,
    add_file,
    remove_file
)


class NovaWatcher(FileSystemEventHandler):


    def on_created(self, event):

        path = event.src_path


        if event.is_directory:

            name = os.path.basename(path).lower()

            print("New folder:", name)

            add_folder(
                name,
                path
            )


        else:

            name = os.path.splitext(
                os.path.basename(path)
            )[0].lower()


            print("New file:", name)

            add_file(
                name,
                path
            )



    def on_deleted(self, event):

        path = event.src_path


        name = os.path.basename(path)

        name = os.path.splitext(name)[0].lower()


        if event.is_directory:

            print("Folder deleted:", name)

            remove_folder(name)


        else:

            print("File deleted:", name)

            remove_file(name)



    def on_moved(self, event):

        old = os.path.basename(
            event.src_path
        )

        new = os.path.basename(
            event.dest_path
        )


        print(
            "Renamed:",
            old,
            "->",
            new
        )


        # add new item
        if event.is_directory:

            add_folder(
                new.lower(),
                event.dest_path
            )

        else:

            name = os.path.splitext(new)[0].lower()

            add_file(
                name,
                event.dest_path
            )



def start_watcher():


    watcher = NovaWatcher()

    observer = Observer()


    home = os.path.expanduser("~")


    locations = [

        os.path.join(home,"Desktop"),

        os.path.join(home,"Documents"),

        os.path.join(home,"Downloads"),

        os.path.join(home,"Pictures"),

        os.path.join(home,"Videos")

    ]


    for location in locations:


        if os.path.exists(location):

            observer.schedule(
                watcher,
                location,
                recursive=True
            )

            print(
                "Watching:",
                location
            )



    observer.start()


    print("\nNova Real-Time Watcher Started\n")


    try:

        while True:

            time.sleep(1)


    except KeyboardInterrupt:

        observer.stop()


    observer.join()



if __name__ == "__main__":

    start_watcher()