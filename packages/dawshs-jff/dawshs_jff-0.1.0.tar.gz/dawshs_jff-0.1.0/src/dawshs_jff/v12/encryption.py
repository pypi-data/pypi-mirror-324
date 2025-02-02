import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

from .constants import request_key, response_key, hh_iv


def gen_req_cipher():
    return AES.new(
        request_key.encode(), AES.MODE_CBC, iv=hh_iv.encode()
    )


def gen_res_cipher():
    return AES.new(
        response_key.encode(), AES.MODE_CBC, iv=hh_iv.encode()
    )


def decrypt_request(payload: str):
    return unpad(
        gen_req_cipher().decrypt(base64.b64decode(payload)),
        block_size=AES.block_size,
    )


def encrypt_request(payload: str):
    return base64.b64encode(
        gen_req_cipher().encrypt(
            pad(payload.encode(), AES.block_size)
        )
    )


def decrypt_response(payload: str):
    return unpad(
        gen_res_cipher().decrypt(base64.b64decode(payload)),
        block_size=AES.block_size,
    )


def encrypt_response(payload: str):
    return base64.b64encode(
        gen_req_cipher().encrypt(
            pad(payload.encode(), AES.block_size)
        )
    )
