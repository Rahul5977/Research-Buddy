import shutil
from fastapi import UploadFile

def save_file(Upload_file: UploadFile,destination: str)->None:
    """Saves the file to the destination
    Args:
        file (UploadFile): _description_
        destination (str): _description_
    Returns:
        _type_: _description_
    """
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(Upload_file.file, buffer)
    except Exception as e:
        raise e
    finally:
        Upload_file.file.close()