from system.skill_engine import execute_skill



def run_skill(action, target):


    if action != "open":

        return False



    functions = [

        "open_website",

        "open_app",

        "open_file_or_folder"

    ]


    for function in functions:


        result = execute_skill(
            function,
            target
        )


        if result:

            return True



    return False