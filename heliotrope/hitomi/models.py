from typing import Literal, Optional
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
    def to_generator(cls, files: list[HitomiFilesJSON]) -> list["HitomiFiles"]:
        for file in files:
            yield cls(file)


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
    def parse_tags(cls, tags: list[HitomiTagsJSON]) -> list[dict[str, str]]:
        if not tags:
            return []

        parsed_tags: list[dict[str, str]] = []
        for tag in tags:
            parsed_tags.append(
                {
                    "value": f"{'female' if tag['female'] else 'male' if tag['male'] else 'tag'}: {tag['tag']}",
                    "url": tag["url"],
                }
            )
        return parsed_tags


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
    def files(self) -> list[HitomiFiles]:
        return HitomiFiles.to_generator(self.__response["files"])

    @property
    def tags(self) -> list[dict[str, str]]:
        return HitomiTags.parse_tags(self.__response["tags"])

    @property
    def japanese_title(self) -> Optional[str]:
        return self.__response.get("japanese_title")

    @property
    def title(self) -> Optional[str]:
        return self.__response["title"]

    @property
    def id(self) -> str:
        return self.__response["id"]

    @property
    def type(self) -> str:
        return self.__response["type"]
