import os
import re

def extract_imports(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    imports = re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)', content, re.MULTILINE)
    return set(imports)

def main():
    directory = '.'  # Change this to your directory path
    all_imports = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                all_imports.update(extract_imports(file_path))

    with open('requirements.txt', 'w') as req_file:
        for imp in sorted(all_imports):
            req_file.write(f"{imp}\n")

if __name__ == "__main__":
    main()