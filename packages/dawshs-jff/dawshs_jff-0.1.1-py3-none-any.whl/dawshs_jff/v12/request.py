import json
import logging
import random
import time
from datetime import datetime

import httpx
from tzlocal import get_localzone

from ..utils.captcha import solve_mng_captcha
from . import (
    generate_hash,
    decrypt_response,
    encrypt_request,
)

logger = logging.getLogger("__main__")
logger.setLevel(logging.DEBUG)


def generate_ip():
    return (
        ".".join([str(random.randint(5, 255)) for _ in range(3)])
        + ".0"
    )


def generate_request(
    client_ip: str,
    provider_code: str = "",
    current_hashes: list | None = None,
    captcha_id: str = "",
    captcha_input: str = "",
):
    if current_hashes is None:
        current_hashes = ["aaa", "bbb"]
    request_timestamp = int(time.time())
    request_time = str(request_timestamp)
    local_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    timezone = get_localzone().key
    h1_hash = generate_hash(client_ip, request_time)
    return {
        "hashes": current_hashes,
        "h1": h1_hash,
        "provider_code": provider_code,
        "timezone": timezone,
        "request_time": request_time,
        "request_timestamp": request_timestamp,
        "local_time": local_time,
        "client_ip": client_ip,
        "client_version": "12",
        "client_source": "a",
        "captcha_id": captcha_id,
        "captcha_input": captcha_input,
    }


async def send_api_request(url, payload):
    async with httpx.AsyncClient() as client:
        headers = {
            # "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; Redmi Note 9 Build/TQ2B.230505.005.A1)",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
        }
        response = await client.post(
            url, headers=headers, content=payload
        )
    return response


async def request_configs(endpoint: str, token: str, provider_code: str = ""):
    ip = generate_ip()
    url = (
        endpoint + "/backend/app_api/v7/config_fetch/?token=" + token
    )
    req = generate_request(ip, provider_code=provider_code)
    for i in range(3):
        payload = encrypt_request(json.dumps(req))
        try:
            response = await send_api_request(
                url,
                payload,
            )
            plain_response = decrypt_response(response.text)
            response_dict = json.loads(plain_response.decode())
            if response_dict["is_captcha"] is True:
                logger.debug("solving captcha")
                captcha_answer = solve_mng_captcha(
                    response_dict["captcha_img"]
                ).strip()
                logger.debug(captcha_answer)
                req = generate_request(
                    ip,
                    captcha_id=response_dict["captcha_id"],
                    captcha_input=captcha_answer,
                    provider_code=provider_code
                )
                continue
        except OSError:
            continue
        except Exception as e:
            logger.debug(e, type(e))
            continue
        else:
            return response_dict

    logger.info(
        "didn't work after the fifth time! raising an exception."
    )
    raise ConnectionRefusedError
