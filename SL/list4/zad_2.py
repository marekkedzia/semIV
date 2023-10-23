import os
import sys


def get_env_paths(path_variable):
    directories = path_variable.split(os.pathsep)
    return directories


def print_executables(path_variable):
    directories = get_env_paths(path_variable)

    def file_exist(file):
        return file.is_file()
    
    def has_access(file):
        return os.access(file.path, os.X_OK)

    for directory in directories:
        print(f"{directory}:")
        try:
            for entry in os.scandir(directory):
                if file_exist(entry) and has_access(entry):
                    print(f"{entry.name}")
        except FileNotFoundError:
            print("Directory not found")
        except PermissionError:
            print("Permission denied")


def main(args):
    print_directories = "a"
    print_execs = "b"

    def commands(arg, command_code):
        return arg[0] == command_code

    path_variable = os.environ.get("PATH", "")

    if not args or commands(args, print_directories):
        print(get_env_paths(path_variable))
    elif commands(args, print_execs):
        print_executables(path_variable)
    else:
        print("Invalid option. Choose 'a' or 'b'")


if __name__ == "__main__":
    main(sys.argv[1:])
