def parse_tag(tags: list) -> list:
    parsed_tags = []
    for tag in tags:
        if not tag.get("male") and tag.get("female"):
            parsed_tags.append({"value": f"female:{tag['tag']}"})
        if tag.get("male") and not tag.get("female"):
            parsed_tags.append({"value": f"male:{tag['tag']}"})
        if not tag.get("male") and not tag.get("female"):
            parsed_tags.append({"value": f"tag:{tag['tag']}"})
        if tag.get("male") and tag.get("female"):
            pass  # 특별한 케이스

    return parsed_tags