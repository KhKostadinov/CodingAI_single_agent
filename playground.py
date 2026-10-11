import os

def open_dir(dirName: str):
    """ Opens either specified existing directory in current working dir OR specified path."""
    initial_dir = os.getcwd() # get the name of current directory
    last_dir = initial_dir
    if os.path.exists(dirName):
        os.chdir(dirName)
        last_dir = os.getcwd() # get the name of current directory
        return initial_dir, last_dir
    else:
        return "No such directory."


def create_dir(dirName: str, replace: bool = False):
    """ Creates new directory if not already existing. If already existing you 
    can decide if overwriting is fine with adjusting 'replace' argument."""
    if os.path.exists(dirName):
        if not replace:
            return "Folder exists, do not replace."
        else:
            os.rmdir(dirName)
            os.mkdir(dirName)
            return f"{dirName} - Directory overwritten."
    else:
        os.mkdir(dirName)
        return f"{dirName} - Directory created."

def remove_dir(dirName: str):
    """ Removes given directory if already existing. """
    if os.path.exists(dirName):
        os.rmdir(dirName)
        return f"{dirName} - Directory removed."
    else:
        return f"{dirName} - Directory does not exist."

def open_file(fileName: str):
    """ Loads the selected file to be edited. """
    if os.path.isfile(fileName):
        with open(fileName,'r') as f:
            return f.read()
    else:
        return "No such file."


def create_file(fileName: str, fileContent: str, replace: bool = False):
    """ Creates new file if not already existing. If already existing you 
    can decide if overwriting is fine with adjusting 'replace' argument."""
    if os.path.isfile(fileName):
        if not replace:
            return "File exists, do not replace."
        else:
            os.remove(fileName)
            with open(fileName,'w') as f:
                f.write(fileContent)
            return f"{fileName} - File overwritten."
    else:
        with open(fileName,'w') as f:
            f.write(fileContent)
        return f"{fileName} - File created."

def remove_file(fileName: str):
    """ Removes given file if already existing. """
    if os.path.isfile(fileName):
        os.remove(fileName)
        return f"{fileName} - File removed."
    else:
        return f"{fileName} - File does not exist."

def main():
    fContent = """print('Hello, world!')"""
    act = remove_file("test.py")
    print(act)

if __name__ == "__main__":
    main()