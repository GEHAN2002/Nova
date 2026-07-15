import json
import os
from datetime import datetime


MEMORY_FILE = "data/memory.json"



def load_memory():

    if not os.path.exists(MEMORY_FILE):

        return {
            "commands": {},
            "history": []
        }


    with open(
        MEMORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def save_memory(memory):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4
        )



def remember_command(command):

    memory = load_memory()

    command = command.lower()


    if command in memory["commands"]:

        memory["commands"][command] += 1

    else:

        memory["commands"][command] = 1



    memory["history"].append(
        {
            "command": command,
            "time": str(datetime.now())
        }
    )


    save_memory(memory)



def get_history():

    memory = load_memory()

    return memory["history"]