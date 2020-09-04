class HitomiGalleryInfoModel:
    def __init__(
        self,
        language_localname: str,
        language: str,
        date: str,
        files: list,
        tags: list,
        japanese_title: str,
        title: str,
        galleryid: int,
        type_: str,
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


def parse_galleryinfo(galleryinfo_json: dict) -> HitomiGalleryInfoModel:
    if not galleryinfo_json["tags"]:
        parsed_tags = []
    else:
        parsed_tags = []
        for tag in galleryinfo_json["tags"]:
            if not tag.get("male") and tag.get("female"):
                parsed_tags.append(
                    {"value": f"female:{tag['tag']}", "url": tag["url"]})
            elif tag.get("male") and not tag.get("female"):
                parsed_tags.append(
                    {"value": f"male:{tag['tag']}", "url": tag["url"]})
            elif not tag.get("male") and not tag.get("female"):
                parsed_tags.append(
                    {"value": f"tag:{tag['tag']}", "url": tag["url"]})
            elif tag.get("male") and tag.get("female"):
                pass  # 특별한 케이스
            else:
                raise Exception

    return HitomiGalleryInfoModel(
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
