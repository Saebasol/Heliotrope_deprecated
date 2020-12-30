import re

from sanic.response import json


def shuffle_image_url(url: str):
    url_parse_regex = re.compile(r"\/\/(..?)(\.hitomi\.la|\.pximg\.net)\/(.+?)\/(.+)")

    parsed_url: list[str] = url_parse_regex.findall(url)[0]

    prefix = parsed_url[0]
    main_url = parsed_url[1].replace(".", "_")
    type_ = parsed_url[2]
    image = parsed_url[3].replace("/", "_")

    main = f"{prefix}_{type_}{main_url}_{image}"

    return main


def solve_shuffle_image_url(shuffled_image_url: str):
    try:
        solve_regex: list[str] = re.findall(
            r"(.+?)_(.+?)_(.+?_net|.+?la)_(.+)", shuffled_image_url
        )[0]
    except:
        return json({"code": 400, "message": "bad_request"})

    prefix = solve_regex[0]
    type_ = solve_regex[1]
    main_url = solve_regex[2].replace("_", ".")
    image = solve_regex[3].replace("_", "/")

    return f"https://{prefix}.{main_url}/{type_}/{image}"
