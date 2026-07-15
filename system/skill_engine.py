from system.skill_loader import load_skills


# Load all skills when Nova starts
SKILLS = load_skills()



def execute_skill(function_name, target):

    """
    Search all loaded skills
    and execute the matching function
    """


    for skill_name, functions in SKILLS.items():


        if function_name in functions:


            print(
                f"Using skill: {skill_name}"
            )


            result = functions[function_name](target)


            return result



    print(
        "Skill function not found:",
        function_name
    )


    return None