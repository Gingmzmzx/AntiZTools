import pathlib, os
def makeSurePathExists(pathToFile):
    pathlib.Path(os.path.join(pathlib.Path().home(), ".AntiZTools", pathToFile)).mkdir(parents=True, exist_ok=True)

def path(pathToFile):
    return os.path.join(pathlib.Path().home(), ".AntiZTools", pathToFile)

def cwdPath(pathToFile):
    return os.path.join(pathlib.Path().cwd(), pathToFile)