from heliotrope.utils.typed import Files, GalleryInfoJSON, Tags
from typing import Optional


class HitomiImageModel:
    def __init__(self, width: int, hash: str, haswebp: int, name: str, height: int):
        self.width = width
        self.hash = hash
        self.haswebp = haswebp
        self.name = name
        self.height = height

    @classmethod
    def image_model_generator(cls, files: list[Files]):
        for file_ in files:
            yield cls(
                file_["width"],
                file_["hash"],
                file_["haswebp"],
                file_["name"],
                file_["height"],
            )
