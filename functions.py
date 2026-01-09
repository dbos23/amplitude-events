import os

#function to check if a directory exists; if not, make it
def mkdir_if_not_exists(path):
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)