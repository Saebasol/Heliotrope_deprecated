from heliotrope.server import heliotrope
import argparse

parser = argparse.ArgumentParser("heliotrope")

parser.add_argument(
    "--host",
    "-H",
    type=str,
    default="0.0.0.0",
    help="the hostname to listen on (default: 0.0.0.0)",
)
parser.add_argument(
    "--port",
    "-P",
    type=int,
    default=8000,
    help="the port of the webserver (default: 8000)",
)

args = parser.parse_args()

heliotrope.run(args.host, args.port)