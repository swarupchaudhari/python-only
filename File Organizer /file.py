import os
import shutil

# Folder path to organize
folder_path = input("Enter folder path: ")

# Dictionary for file types
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"]
}

# Read all files
files = os.listdir(folder_path)

# Loop through files
for file in files:
    file_path = os.path.join(folder_path, file)

    # Ignore folders
    if os.path.isfile(file_path):

        # Get file extension
        extension = os.path.splitext(file)[1].lower()

        # Check category
        for folder, extensions in file_types.items():
            if extension in extensions:

                destination = os.path.join(folder_path, folder)

                # Create folder if it doesn't exist
                if not os.path.exists(destination):
                    os.makedirs(destination)

                # Move file
                shutil.move(file_path, os.path.join(destination, file))

                print(file, "moved to", folder)
                break

print("File organization completed!")