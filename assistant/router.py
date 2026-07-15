from system.skill_manager import run_skill
from assistant.intent import extract_intent
from system.memory_manager import remember_command



def route(command):

    remember_command(command)

    intent = extract_intent(command)


    action = intent["action"]
    target = intent["target"]


    print("Action:", action)
    print("Target:", target)


    if run_skill(action, target):

     return True


    print("Command not understood")

    return False