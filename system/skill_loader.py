import os
import importlib
import inspect


SKILLS_FOLDER = "skills"



def load_skills():

    skills = {}


    for file in os.listdir(SKILLS_FOLDER):

        if file.endswith(".py") and file != "__init__.py":


            skill_name = file[:-3]


            module = importlib.import_module(
                f"skills.{skill_name}"
            )


            functions = {}


            for name, obj in inspect.getmembers(module):

                if inspect.isfunction(obj):

                    functions[name] = obj



            skills[skill_name] = functions


            print(
                f"Loaded skill: {skill_name}"
            )

            for function in functions:

                print(
                    "  Function:",
                    function
                )


    return skills