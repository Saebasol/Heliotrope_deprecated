import re

from sanic.response import json


def shuffle_image_url(url: str):
    url_parse_regex = re.compile(r"\/\/(..?)(\.hitomi\.la|\.pximg\.net)\/(.+?)\/(.+)")

    parsed_url: list[str] = url_parse_regex.findall(url)[0]

    prefix = parsed_url[0]
    main_url = parsed_url[1].replace(".", "_")
    type_ = parsed_url[2]
    image = parsed_url[3]

    sliced_hash_regex = re.compile(r"[0-9a-f]\/([0-9a-f]{2})\/")
    sliced_hash = sliced_hash_regex.search("/" + image)

    replaced_sliced_hash = sliced_hash[0].replace("/", "_")
    image = url.rsplit("/", 1)[1]

    return f"{type_}_{prefix}{replaced_sliced_hash}{image}"


def solve_shuffle_image_url(shuffled_image_url: str):
    try:
        solve_regex = re.findall(r"(.+?)_(.+?)_(.+)", shuffled_image_url)[0]
    except:
        return json({"code": 400, "message": "bad_request"})

    type_ = solve_regex[0]
    prefix = solve_regex[1]
    image = solve_regex[2]

    return f"https://{prefix}.hitomi.la/{type_ }/{image}".replace("_", "/")
