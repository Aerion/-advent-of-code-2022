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


def get_smallest_folder_above(folder: Item, min_size: int):
    res = None
    if folder.size > min_size:
        res = folder
    for child in folder.children.values():
        if child.is_folder:
            smallest_child = get_smallest_folder_above(child, min_size)
            if smallest_child and (not res or smallest_child.size < res.size):
                res = smallest_child
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
            cur_folder.children[destination] = Item(
                True, 0, destination, cur_folder, {}
            )

        cur_folder = cur_folder.children[destination]


total_space = 70_000_000
unused_space = total_space - root_folder.size
space_to_free = 30_000_000 - unused_space
print(f"root folder size: {root_folder.size}")
print(f"space to free: {space_to_free}")
print(get_smallest_folder_above(root_folder, space_to_free).size)
