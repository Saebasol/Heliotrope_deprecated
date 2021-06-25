from typing import Any, Iterator, Optional, Union

from bs4 import BeautifulSoup
from bs4.element import Tag

from heliotrope.utils.typed import FilesDict, GalleryInfoDict, TagsDict


class HitomiImageModel:
    def __init__(self, width: int, hash: str, haswebp: int, name: str, height: int):
        self.width = width
        self.hash = hash
        self.haswebp = haswebp
        self.name = name
        self.height = height

    @classmethod
    def image_model_generator(cls, files: list[FilesDict]):
        for file in files:
            yield cls(
                file["width"],
                file["hash"],
                file["haswebp"],
                file["name"],
                file["height"],
            )

    @classmethod
    def single(cls, hitomi_image_dict: FilesDict):
        return cls(
            hitomi_image_dict["width"],
            hitomi_image_dict["hash"],
            hitomi_image_dict["haswebp"],
            hitomi_image_dict["name"],
            hitomi_image_dict["height"],
        )


class HitomiGalleryInfoModel:
    def __init__(
        self,
        language_localname: str,
        language: str,
        date: str,
        files: list[FilesDict],
        tags: list[TagsDict],
        japanese_title: Optional[str],
        title: Optional[str],
        galleryid: str,
        type: str,
    ):
        self.language_localname = language_localname
        self.language = language
        self.date = date
        self.files = files
        self.tags = tags
        self.japanese_title = japanese_title
        self.title = title
        self.galleryid = galleryid
        self.type = type

    @classmethod
    def parse_galleryinfo(cls, galleryinfo_json: GalleryInfoDict, parse: bool = False):
        parsed_tags = []
        if galleryinfo_json["tags"]:

            for tag in galleryinfo_json["tags"]:
                if (
                    len(
                        value := list(
                            filter(
                                None,
                                [
                                    "male" if tag.get("male") else None,
                                    "female" if tag.get("female") else None,
                                ],
                            )
                        )
                    )
                    > 1
                ):
                    raise Exception
                parsed_tags.append(
                    {
                        "value": f"{value[0] if value else 'tag'}:{tag['tag']}",
                        "url": tag["url"],
                    }
                )

        return cls(
            galleryinfo_json["language_localname"],
            galleryinfo_json["language"],
            galleryinfo_json["date"],
            galleryinfo_json.get("files"),
            parsed_tags if parse else galleryinfo_json["tags"],
            galleryinfo_json.get("japanese_title"),
            galleryinfo_json["title"],
            galleryinfo_json["id"],
            galleryinfo_json["type"],
        )


class HitomiInfoModel:
    def __init__(
        self,
        title: str,
        img_link: str,
        artist: list[dict[str, str]],
        group: list[dict[str, str]],
        type: Optional[dict[str, str]],
        language: Optional[dict[str, str]],
        series: list[dict[str, str]],
        characters: list[dict[str, str]],
        tags: list[dict[str, str]],
        date: str,
    ):
        self.title = title
        self.thumbnail = img_link
        self.artist = artist
        self.group = group
        self.type = type
        self.language = language
        self.series = series
        self.characters = characters
        self.tags = tags
        self.date = date

    @staticmethod
    def parse_list_element(elements: list[Tag]):
        if not elements:
            return []
        return [{"value": element.text, "url": element["href"]} for element in elements]

    @staticmethod
    def parse_single_element(elements: Tag):
        if not elements:
            return None
        return {
            "value": elements.text.replace(" ", "").replace("\n", ""),
            "url": elements["href"],
        }

    @classmethod
    def parse_tags(cls, html: Union[str, bytes], hitomi_type: str):
        hitomi_type_mapping = {
            "manga": "manga",
            "doujinshi": "dj",
            "cg": "acg",
            "gamecg": "cg",
            "anime": "anime",
        }

        if isinstance(html, bytes):
            html = html.decode("utf-8")

        soup = BeautifulSoup(html, "lxml")

        if soup_type := hitomi_type_mapping.get(hitomi_type):
            if gallery_element := soup.find(
                "div", class_=f"gallery {soup_type}-gallery"
            ):

                galleryinfo = gallery_element.find("div", class_="gallery-info")
                infos = galleryinfo.find_all("tr")

                title = gallery_element.find("h1").find("a").text
                img_link = soup.find("picture").find("img")["src"]

                artist_elements = gallery_element.find("h2").find_all("a")
                group_elements = infos[0].find_all("a")
                type_element = infos[1].find("a")
                language_element = infos[2].find("a")
                series_elements = infos[3].find_all("a")
                characters_elements = infos[4].find_all("a")
                tags_elements = infos[5].find_all("a")
                date = soup.find("span", class_="date").text

                return cls(
                    title,
                    img_link,
                    cls.parse_list_element(artist_elements),
                    cls.parse_list_element(group_elements),
                    cls.parse_single_element(type_element),
                    cls.parse_single_element(language_element),
                    cls.parse_list_element(series_elements),
                    cls.parse_list_element(characters_elements),
                    cls.parse_list_element(tags_elements),
                    date,
                )

    def to_dict(self):
        return {
            "title": self.title,
            "thumbnail": self.thumbnail,
            "artist": self.artist,
            "group": self.group,
            "type": self.type,
            "language": self.language,
            "series": self.series,
            "characters": self.characters,
            "tags": self.tags,
            "date": self.date,
        }
