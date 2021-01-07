from bs4 import BeautifulSoup

from Heliotrope.utils.shuffle import shuffle_image_url


class HitomiTagsModel:
    def __init__(
        self,
        title: str,
        img_link: str,
        artist: list,
        group: list,
        type_: str,
        language: str,
        series: list,
        characters: list,
        tags: list,
    ):
        self.title = title
        self.thumbnail = img_link
        self.artist = artist
        self.group = group
        self.type_ = type_
        self.language = language
        self.series = series
        self.characters = characters
        self.tags = tags


def parse_tags(html: str, type_: str):
    if type_ == "manga":
        soup_type = "manga"
    elif type_ == "doujinshi":
        soup_type = "dj"
    elif type_ == "cg":
        soup_type = "acg"
    elif type_ == "gamecg":
        soup_type = "cg"
    elif type_ == "anime":
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

    return HitomiTagsModel(
        title,
        shuffle_image_url(img_link),
        check_element(artist_elements),
        check_element(group_elements),
        check_element(type_element),
        check_element(language_element),
        check_element(series_elements),
        check_element(characters_elements),
        check_element(tags_elements),
    )


def check_element(elements):
    if isinstance(elements, list):
        if not elements:
            return []
        return [{"value": element.text, "url": element["href"]} for element in elements]
    if not elements:
        return None
    return {
        "value": elements.text.replace(" ", "").replace("\n", ""),
        "url": elements["href"],
    }
