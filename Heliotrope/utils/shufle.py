import re

from sanic.response import json


def shufle_image_url(url: str):
    prefix_and_type_regex = re.compile(r"\/\/(..?)\.hitomi\.la\/(.+?)/")
    sliced_hash_regex = re.compile(r"\/[0-9a-f]\/([0-9a-f]{2})\/")

    prefix_and_type = prefix_and_type_regex.findall(url)[0]
    prefix = prefix_and_type[0]
    type_ = prefix_and_type[1]

    sliced_hash = sliced_hash_regex.search(url)
    replaced_sliced_hash = sliced_hash[0].replace("/", "_")

    image = url.rsplit("/", 1)[1]

    return f"{type_}_{prefix}{replaced_sliced_hash}{image}"


def solve_shufle_image_url(shufled_image_url: str):
    solve_regex = re.findall(r"(.+?)_(.+?)_(.+)", shufled_image_url)[0]

    type_ = solve_regex[0]
    prefix = solve_regex[1]
    image = solve_regex[2]

    try:
        return f"https://{prefix}.hitomi.la/{type_ }/{image}".replace("_", "/")
    except:
        return json({"code": 400, "message": "bad_request"})