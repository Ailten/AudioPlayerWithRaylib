

# ---------->
import json

def getJsonObj(mainPath: str):

    output = None

    # get json path.
    pathJsonFile = f"{mainPath}/json/param.json"

    # get json obj.
    fileJson = None
    try:
        fileJson = open(pathJsonFile, "r")
        strJson = fileJson.read()
        output = json.loads(strJson)
    except Exception as e:
        print(e)
    finally:
        if(fileJson != None and not fileJson.closed):
            fileJson.close()
        else:
            raise Exception("error ro read file json.")

    return output


# ---------->
import pathlib

def getAllFilesName(pathFolder: str):

    output = [n.stem for n in pathlib.Path(pathFolder).iterdir() if (
        n.is_file() and 
        n.suffix == ".mp3"
    )]

    return output


# ---------->
#import pathlib

def isHasMusicTexture(pathFile: str):

    return pathlib.Path(pathFile).exists()
