import os
import json

FILE_DATABASE = "data/files.json"

# File types to index
EXTENSIONS = [
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".jpg",
    ".jpeg",
    ".png",
    ".mp3",
    ".mp4",
    ".zip",
    ".py"
]


def scan_files():

    files = {}

    home = os.path.expanduser("~")

    locations = [
        os.path.join(home, "Desktop"),
        os.path.join(home, "Documents"),
        os.path.join(home, "Downloads")
    ]

    for location in locations:

        if not os.path.exists(location):
            continue

        for root, dirs, filenames in os.walk(location):

            for filename in filenames:

                if filename.lower().endswith(tuple(EXTENSIONS)):

                    name = os.path.splitext(filename)[0].lower()

                    path = os.path.join(root, filename)

                    files[name] = path

    os.makedirs("data", exist_ok=True)

    with open(FILE_DATABASE, "w", encoding="utf-8") as f:
        json.dump(files, f, indent=4)

    print(f"Found {len(files)} files")
    print("Database saved!")


if __name__ == "__main__":
    scan_files()