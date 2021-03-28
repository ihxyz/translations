import os


def generate_indexes(file):
    indexes = {}
    for f_line in file:
        parts = f_line.split(':', maxsplit=1)
        if len(parts) != 2:
            continue
        indexes[parts[0]] = parts[1]
    target_file.seek(0)  # reset pointer to start of file
    return indexes


print("NOTE: If any keys were renamed, the old value associated with them in target files will not be preserved!")

path = "./"

directory = input("Enter the directory to scan: ")

path += directory + '/'
files = [f for f in os.listdir(path) if f.endswith(".yml")]

origin = input("Enter the original file to copy from: ")
origin = origin + ".yml" if not origin.endswith(".yml") else origin

raw_target = input("Enter the target file(s) to update, each separated with a space. Use Enter to update all files: ")
raw_target = raw_target.split()
raw_target = [f.strip() for f in raw_target]
targets = []
if not raw_target:
    targets = files
    targets.remove(origin)
for f in raw_target:
    if not f.endswith(".yml"):
        targets.append(f + ".yml")
    else:
        targets.append(f)

with open(path + origin, encoding="utf-8") as origin_file:
    for target_file_name in targets:
        with open(path + target_file_name, "r+", encoding="utf-8") as target_file:
            target_indexes = generate_indexes(target_file)
            new_content = ""
            for line in origin_file:
                if line == '\n' or line.startswith('#'):
                    # blank line or comment
                    new_content += line
                else:
                    # i18n data
                    translation_parts = line.split(':', maxsplit=1)
                    translation = target_indexes.get(translation_parts[0], '\n')
                    new_content += f"{translation_parts[0]}:{translation}"
            target_file.truncate()  # clear file
            target_file.write(new_content)
        print(f"Updated {target_file_name}")
        origin_file.seek(0)  # reset origin file position so it can cycle through again
