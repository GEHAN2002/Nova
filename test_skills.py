from system.skill_loader import load_skills


skills = load_skills()


print("\nAvailable skills:")


for skill in skills:

    print("-", skill)