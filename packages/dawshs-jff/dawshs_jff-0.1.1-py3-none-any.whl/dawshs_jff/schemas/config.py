from pydantic import BaseModel


class ProxyConfig(BaseModel):
    link: str
    hash: str
    fragment: bool
