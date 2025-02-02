"""just for fun"""
import argparse
import asyncio
import json
import logging

from ..schemas.config import ProxyConfig
from ..v12.hashes import generate_token
from ..v12.request import request_configs

logger = logging.getLogger(__name__)


async def main():
    parser = argparse.ArgumentParser(description="Gets some data from the URL.")
    parser.add_argument("url", help="The URL.")
    parser.add_argument("--code", help="An optional code", default=None)

    args = parser.parse_args()

    api_token = generate_token()
    returned_configs = []
    returned_hashes = set()
    try:
        response = await request_configs(
            args.url,
            api_token,
            provider_code=args.code or None
        )
    except OSError:
        raise
    else:
        for config in response["configs"]:
            if config["hash"] in returned_hashes:
                continue
            returned_configs.append(
                ProxyConfig(
                    link=config["url"],
                    hash=config["hash"],
                    fragment=config["use_fragment"],
                )
            )
            returned_hashes.add(config["hash"])
        return print(json.dumps([r.model_dump() for r in returned_configs]))


def entry():
    asyncio.run(main())


if __name__ == "__main__":
    entry()
