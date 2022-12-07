import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    is_folder: bool
    size: int
    name: str
    parent: Optional[object]
    children: dict[str, object]


def pretty_print(item: Item, indent: int):
    print(indent * " ", end="")
    print(f"- {item.name} ", end="")
    if item.is_folder:
        print("(dir)")
        for child in item.children.values():
            pretty_print(child, indent + 2)
    else:
        print(f"(file, size={item.size})")

def get_total_folder_size_under(folder: Item, max_size: int):
    res = 0
    if folder.size < max_size:
        res = folder.size
    for child in folder.children.values():
        if child.is_folder:
            res += get_total_folder_size_under(child, max_size)
    return res


root_folder = Item(True, 0, "/", None, {})

cur_folder = root_folder

lines = [l.strip() for l in sys.stdin.readlines()]

i = 0
while i < len(lines):
    line = lines[i]
    i += 1

    if line[2:] == "ls":
        while i < len(lines):
            line = lines[i].strip()
            i += 1
            if line[0] == "$":
                i -= 1
                break
            if line[0] == "d":
                folder_name = line[len("dir ") :]
                if folder_name not in cur_folder.children:
                    cur_folder.children[folder_name] = Item(
                        True, 0, folder_name, cur_folder, {}
                    )
                continue
            file_parts = line.split(" ")
            filename = file_parts[1]
            filesize = int(file_parts[0])
            if filename not in cur_folder.children:
                cur_folder.children[filename] = Item(
                    False, filesize, filename, cur_folder, {}
                )
                parent_folder = cur_folder
                while parent_folder:
                    parent_folder.size += filesize
                    parent_folder = parent_folder.parent
    else:
        # else, cd command
        destination = line.split(" ")[-1]
        if destination == "..":
            cur_folder = cur_folder.parent
            continue

        if destination == "/":
            cur_folder = root_folder
            continue

        if destination not in cur_folder.children:
            cur_folder.children[destination] = Item(True, 0, destination, cur_folder, {})

        cur_folder = cur_folder.children[destination]

pretty_print(root_folder, 0)

print(get_total_folder_size_under(root_folder, 100_000))
