from bs4 import BeautifulSoup
from bs4 import element


class HitomiTagsModel:
    def __init__(
        self,
        title: str,
        artist: list,
        group: list,
        type_: str,
        language: str,
        series: list,
        characters: list,
        tags: list,
    ):
        self.title = title
        self.artist = artist
        self.group = group
        self.type_ = type_
        self.language = language
        self.series = series
        self.characters = characters
        self.tags = tags


def parse_tags(html: str):
    soup = BeautifulSoup(html, "lxml").find("div", class_="gallery dj-gallery")

    galleryinfo = soup.find("div", class_="gallery-info")
    infos = galleryinfo.find_all("tr")

    title = soup.find("h1").find("a").text

    artist_elements = soup.find("h2").find_all("a")
    group_elements = infos[0].find_all("a")
    type_elements = infos[1].find("a")
    language_elements = infos[2].find("a")
    series_elements = infos[3].find_all("a")
    characters_elements = infos[4].find_all("a")
    tags_elements = infos[5].find_all("a")

    return HitomiTagsModel(
        title,
        check_element(artist_elements),
        check_element(group_elements),
        check_element(type_elements),
        check_element(language_elements),
        check_element(series_elements),
        check_element(characters_elements),
        check_element(tags_elements),
    )


def check_element(elements):
    if isinstance(element, list):
        if not element:
            return []
        else:
            return [
                {"value": element.text, "url": element["href"]} for element in elements
            ]
    else:
        if not element:
            return None
        else:
            return {"value": element.text, "url": element["href"]}
