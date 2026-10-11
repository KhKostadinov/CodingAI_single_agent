from main import CodeMaster
import os

@CodeMaster.tool_plain # tool_plain is used when no context is provided
def dir_scan():
    """ Scans the content of current directory and returns a list of available files/folders."""
    current_dir = os.getcwd() # get the name of current directory
    fList = os.listdir(current_dir) # items list
    fString = '' # items list turned into string
    if len(fList) > 0:
        fString = "id | File\n"
        for id,file in enumerate(fList):
            fString += f"{id} | {file}\n"
        return fString, current_dir
    else:
        return "No files in current directory."


@CodeMaster.tool_plain # tool_plain is used when no context is provided
def dir_up():
    """ Goes up one level in directory hierarchy."""
    initial_dir = os.getcwd() # get the name of current directory
    os.chdir('..')
    last_dir = os.getcwd() # get the name of current directory
    return initial_dir, last_dir

@CodeMaster.tool_plain # tool_plain is used when no context is provided
def open_dir(dirName: str):
    """ Opens either specified existing directory in current working dir OR specified path."""
    initial_dir = os.getcwd() # get the name of current directory
    if os.path.exists(dirName):
        os.chdir(dirName)
        last_dir = os.getcwd() # get the name of current directory
        return initial_dir, last_dir
    else:
        return "No such directory."

@CodeMaster.tool_plain
def create_folder(dirName: str, replace: bool = False):
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

@CodeMaster.tool_plain
def remove_dir(dirName: str):
    """ Removes given directory if already existing. """
    if os.path.exists(dirName):
        os.rmdir(dirName)
        return f"{dirName} - Directory removed."
    else:
        return f"{dirName} - Directory does not exist."

@CodeMaster.tool_plain
def open_file(fileName: str):
    """ Loads the selected file to be edited. """
    if os.path.isfile(fileName):
        with open(fileName,'r') as f:
            return f.read()
    else:
        return "No such file."

@CodeMaster.tool_plain
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
        with open(fileName,'w',encoding='utf-8') as f:
            f.write(fileContent)
        return f"{fileName} - File created."

@CodeMaster.tool_plain
def remove_file(fileName: str):
    """ Removes given file if already existing. """
    if os.path.isfile(fileName):
        os.remove(fileName)
        return f"{fileName} - File removed."
    else:
        return f"{fileName} - File does not exist."
