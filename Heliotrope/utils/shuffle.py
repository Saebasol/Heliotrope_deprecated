import re

from sanic.response import json


def shuffle_image_url(url: str) -> str:
    url_parse_regex = re.compile(r"\/\/(..?)(\.hitomi\.la|\.pximg\.net)\/(.+?)\/(.+)")

    parsed_url: list[str] = url_parse_regex.findall(url)[0]

    prefix = parsed_url[0]
    main_url = parsed_url[1].replace(".", "_")
    type_ = parsed_url[2]
    image = parsed_url[3].replace("/", "_")

    main = f"{prefix}_{type_}{main_url}_{image}"

    return main


def solve_shuffle_image_url(shuffled_image_url: str) -> str:
    try:
        solve_regex: list[str] = re.findall(
            r"(.+?)_(.+?)_(.+?_net|.+?la)_(.+)_(.+?_.+)", shuffled_image_url
        )[0]
    except:
        return json({"code": 400, "message": "bad_request"}, 400)

    prefix = solve_regex[0]
    type_ = solve_regex[1]
    main_url = solve_regex[2].replace("_", ".")
    img_date_or_hitomi_url_etc = solve_regex[3].replace("_", "/")
    image = solve_regex[4]

    if "pximg" not in main_url:
        image = image.replace("_", "/")

    return f"https://{prefix}.{main_url}/{type_}/{img_date_or_hitomi_url_etc}/{image}"
