from typing import Any, Literal, Optional, Iterator, Union
from heliotrope.typing import HitomiFilesJSON, HitomiGalleryInfoJSON, HitomiTagsJSON


class HitomiFiles:
    def __init__(self, response: HitomiFilesJSON) -> None:
        self.__response = response

    @property
    def width(self) -> int:
        return self.__response["width"]

    @property
    def hash(self) -> str:
        return self.__response["hash"]

    @property
    def haswebp(self) -> int:
        return self.__response["haswebp"]

    @property
    def name(self) -> str:
        return self.__response["name"]

    @property
    def height(self) -> int:
        return self.__response["height"]

    @classmethod
    def to_generator(cls, files: list[HitomiFilesJSON]) -> Iterator["HitomiFiles"]:
        for file in files:
            yield cls(file)

    def to_dict(self) -> HitomiFilesJSON:
        return {
            "width": self.width,
            "hash": self.hash,
            "haswebp": self.haswebp,
            "name": self.name,
            "height": self.height,
        }


class HitomiTags:
    def __init__(self, response: HitomiTagsJSON) -> None:
        self.__response = response

    @property
    def male(self) -> Literal["", "1"]:
        return self.__response["male"]

    @property
    def female(self) -> Literal["", "1"]:
        return self.__response["female"]

    @property
    def url(self) -> str:
        return self.__response["url"]

    @property
    def tag(self) -> str:
        return self.__response["tag"]

    @classmethod
    def to_generator(cls, tags: list[HitomiTagsJSON]) -> Iterator["HitomiTags"]:
        for tag in tags:
            yield HitomiTags(tag)

    @classmethod
    def parse_tags(cls, tag: HitomiTagsJSON) -> dict[str, str]:
        return {
            "value": f"{'female' if tag['female'] else 'male' if tag['male'] else 'tag'}: {tag['tag']}",
            "url": tag["url"],
        }

    def to_parse_dict(self) -> dict[str, str]:
        return self.parse_tags(self.to_dict())

    def to_dict(self) -> HitomiTagsJSON:
        return {
            "male": self.male,
            "female": self.female,
            "url": self.url,
            "tag": self.tag,
        }


class HitomiGalleryInfo:
    def __init__(self, response: HitomiGalleryInfoJSON) -> None:
        self.__response = response

    @property
    def language_localname(self) -> str:
        return self.__response["language_localname"]

    @property
    def language(self) -> str:
        return self.__response["language"]

    @property
    def date(self) -> str:
        return self.__response["date"]

    @property
    def files(self) -> Iterator[HitomiFiles]:
        return HitomiFiles.to_generator(self.__response["files"])

    @property
    def tags(self) -> Iterator[HitomiTags]:
        return HitomiTags.to_generator(self.__response["tags"])

    @property
    def japanese_title(self) -> Optional[str]:
        return self.__response.get("japanese_title")

    @property
    def title(self) -> str:
        return self.__response["title"]

    @property
    def id(self) -> str:
        return self.__response["id"]

    @property
    def type(self) -> str:
        return self.__response["type"]

    def to_dict(self) -> HitomiGalleryInfoJSON:
        return {
            "language_localname": self.language_localname,
            "language": self.language,
            "date": self.date,
            "files": [file.to_dict() for file in self.files],
            "tags": [tag.to_dict() for tag in self.tags],
            "japanese_title": self.japanese_title,
            "title": self.title,
            "id": self.id,
            "type": self.type,
        }
