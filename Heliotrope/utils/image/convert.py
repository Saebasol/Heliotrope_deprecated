import os
from PIL import Image


def convert_to_png(directory: str):
    filelist = os.listdir(directory)

    for file in filelist:
        if ".webp" in file:
            filename = directory + "/" + file
            Image.open(file).convert("RGB").save(
                filename.replace(".webp", ".png"), "png"
            )
            os.remove(filename)
