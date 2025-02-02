import os

def save_folder_structure(root_folder, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for folder, _, files in os.walk(root_folder):
            for file in files:
                if file.endswith((".css", ".js", ".html", ".py",".map",".svg")):
                    relative_path = os.path.relpath(os.path.join(folder, file), root_folder)
                    f.write(f"FILE: {relative_path}\n")  # Store file path
                    with open(os.path.join(folder, file), "r", encoding="utf-8") as file_content:
                        f.write(file_content.read() + "\n---END_FILE---\n")  # Store content
    
    full_output_path = os.path.abspath(output_file)
    print(f"Folder structure and file contents saved to: {full_output_path}")

if __name__ == "__main__":
    root_folder = input("Enter the folder path to convert: ")
    output_file = "folder_structure.txt"
    
    save_folder_structure(root_folder, output_file)
