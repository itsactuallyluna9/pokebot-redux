from os import environ
from dotenv import load_dotenv

from .client import client


def run():
    load_dotenv()
    client.run(environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    run()
