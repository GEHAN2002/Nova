from system.database_manager import *


add_folder(
    "test folder",
    r"C:\Users\DELL\Desktop\Test Folder"
)


result = search_folder("test")

print(result)