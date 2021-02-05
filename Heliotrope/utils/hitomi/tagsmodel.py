from typing import Any, Optional, Union

from bs4 import BeautifulSoup

from Heliotrope.utils.shuffle import shuffle_image_url


class HitomiTagsModel:
    def __init__(
        self,
        title: str,
        img_link: str,
        artist: Optional[Union[list[Any], list[dict[str, str]], dict[str, str]]],
        group: Optional[Union[list[Any], list[dict[str, str]], dict[str, str]]],
        type: Optional[Union[list[Any], list[dict[str, str]], dict[str, str]]],
        language: Optional[Union[list[Any], list[dict[str, str]], dict[str, str]]],
        series: Optional[Union[list[Any], list[dict[str, str]], dict[str, str]]],
        characters: Optional[Union[list[Any], list[dict[str, str]], dict[str, str]]],
        tags: Optional[Union[list[Any], list[dict[str, str]], dict[str, str]]],
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

    @staticmethod
    def check_element(elements):
        if isinstance(elements, list):
            if not elements:
                return []
            return [
                {"value": element.text, "url": element["href"]} for element in elements
            ]
        if not elements:
            return None
        return {
            "value": elements.text.replace(" ", "").replace("\n", ""),
            "url": elements["href"],
        }

    @classmethod
    def parse_tags(cls, html: Union[str, bytes], type: str):
        if type == "manga":
            soup_type = "manga"
        elif type == "doujinshi":
            soup_type = "dj"
        elif type == "cg":
            soup_type = "acg"
        elif type == "gamecg":
            soup_type = "cg"
        elif type == "anime":
            soup_type = "anime"
        else:
            return None

        if isinstance(html, bytes):
            html = html.decode("utf-8")

        soup = BeautifulSoup(html, "lxml")

        gallery_element = soup.find("div", class_=f"gallery {soup_type}-gallery")

        if not soup:
            return None

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

        return cls(
            title,
            shuffle_image_url(img_link),
            cls.check_element(artist_elements),
            cls.check_element(group_elements),
            cls.check_element(type_element),
            cls.check_element(language_element),
            cls.check_element(series_elements),
            cls.check_element(characters_elements),
            cls.check_element(tags_elements),
        )
