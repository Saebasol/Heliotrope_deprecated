from typing import Literal, Optional, TypedDict


class Files(TypedDict):
    width: int
    hash: str
    haswebp: int
    name: str
    height: int


class Tags(TypedDict):
    male: Literal["", "1"]
    female: Literal["", "1"]
    url: str
    tag: str


class GalleryInfoJSON(TypedDict):
    language_localname: str
    language: str
    date: str
    files: list[Files]
    tags: list[Tags]
    japanese_title: Optional[str]
    title: str
    type_: str