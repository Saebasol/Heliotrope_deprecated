class ImageModel:
    def __init__(self, width: int, hash_: str, haswebp: int, name: str, height: int):
        self.width = int(width)
        self.hash_ = str(hash_)
        self.haswebp = bool(haswebp)
        self.name = str(name)
        self.height = int(height)
