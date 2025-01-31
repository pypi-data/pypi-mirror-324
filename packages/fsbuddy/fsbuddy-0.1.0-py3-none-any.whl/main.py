import argparse
import os
import time

from send2trash import send2trash


def handle_size(path):
    size = get_size(path)
    print(f"Total size: {size} bytes")


def get_size(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        return get_dir_size(path)


def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            try:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += get_dir_size(entry.path)
            except Exception as e: 
                print(f"Skipping {entry.path}, error: {e}")
    return total


def handle_list(path, size=False, date=False):
    paths = []
    with os.scandir(path) as it: 
        for entry in it:
            data = {
                "path": os.path.abspath(entry.path),
                "size": get_size(entry.path),
                "last_access_time": entry.stat().st_atime
            }
            data["last_access_time_readable"] = time.ctime(data["last_access_time"])
            paths.append(data)
    if size:
        sorted_paths = sorted(paths, key=lambda x: x['size'], reverse=True)
    elif date: 
        sorted_paths = sorted(paths, key=lambda x: x['last_access_time'], reverse=True)
    else:
        sorted_paths = sorted(paths, key=lambda x: x['path'])
    
    # Define column widths
    path_width = max(len(data['path']) for data in sorted_paths) + 2
    size_width = max(len(str(data['size'])) for data in sorted_paths) + 2

    # Print aligned output
    for data in sorted_paths:
        print(
            f"{data['path'].ljust(path_width)}"
            f"{str(data['size']).rjust(size_width)} "
            f"{data['last_access_time_readable']}"
        )


def handle_delete(path, soft=False):
    try:
        if soft:
            send2trash(path)
        else:
            os.remove(path)
            print(f"{os.path.abspath(path)} has been deleted.")
    except Exception as e:
        print(f"Failed to delete {path}, error: {e}")


def main():
    description = """
    Welcome to File System Buddy. 
    A CLI tool for managing your file system.
    """
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest="action", required=True)
    
    parser_size = subparsers.add_parser("size", help="Get the total size of the specified path.")
    parser_size.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Specify the path to calculate the size. Defaults to current directory."
    )

    parser_list = subparsers.add_parser("list", help="List the files and subdirectories in the specified path.")
    parser_list.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Specify the path to list files and subdirectories. Defaults to current directory."
    )
    group = parser_list.add_mutually_exclusive_group()
    group.add_argument(
        "--size",
        action="store_true",
        help="Sort files by size."
    )
    group.add_argument(
        "--date",
        action="store_true",
        help="Sort files by last access time."
    )

    parser_delete = subparsers.add_parser("delete", help="Delete files in the specified path.")
    parser_delete.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Specify the path to delete files. Defaults to current directory."
    )
    parser_delete.add_argument(
        "--soft",
        action="store_true",
        help="Soft delete. Move path to Trash."
    )

    args = parser.parse_args()

    if args.action == "size":
        handle_size(args.path)
    elif args.action == "list":
        handle_list(args.path, size=args.size, date=args.date)
    elif args.action == "delete":
        handle_delete(args.path, soft=args.soft)


if __name__ == "__main__":
    main()
