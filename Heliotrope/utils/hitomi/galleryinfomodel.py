from typing import Optional, Union

from Heliotrope.utils.hitomi.common import Files


class HitomiGalleryInfoModel:
    def __init__(
        self,
        language_localname: Optional[str],
        language: Optional[str],
        date: Optional[str],
        files: Optional[list[Files]],
        tags: Optional[list[dict[str, str]]],
        japanese_title: Optional[str],
        title: Optional[str],
        galleryid: Optional[str],
        type_: Optional[str],
    ):
        self.language_localname = language_localname
        self.language = language
        self.date = date
        self.files = files
        self.tags = tags
        self.japanese_title = japanese_title
        self.title = title
        self.galleryid = galleryid
        self.type_ = type_

    @classmethod
    def parse_galleryinfo(cls, galleryinfo_json: dict):
        if not galleryinfo_json["tags"]:
            parsed_tags: list[dict] = []
        else:
            parsed_tags = []
            for tag in galleryinfo_json["tags"]:
                if not tag.get("male") and tag.get("female"):
                    parsed_tags.append(
                        {"value": f"female:{tag['tag']}", "url": tag["url"]}
                    )
                elif tag.get("male") and not tag.get("female"):
                    parsed_tags.append(
                        {"value": f"male:{tag['tag']}", "url": tag["url"]}
                    )
                elif not tag.get("male") and not tag.get("female"):
                    parsed_tags.append(
                        {"value": f"tag:{tag['tag']}", "url": tag["url"]}
                    )
                elif tag.get("male") and tag.get("female"):
                    raise Exception
                else:
                    raise Exception

        return cls(
            galleryinfo_json.get("language_localname"),
            galleryinfo_json.get("language"),
            galleryinfo_json.get("date"),
            galleryinfo_json.get("files"),
            parsed_tags,
            galleryinfo_json.get("japanese_title"),
            galleryinfo_json.get("title"),
            galleryinfo_json.get("id"),
            galleryinfo_json.get("type"),
        )
