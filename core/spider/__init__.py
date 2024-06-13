from curl_cffi.requests import Response
from selectolax.lexbor import LexborHTMLParser, LexborNode


def parse(response: Response) -> LexborHTMLParser:
    return LexborHTMLParser(response.text)


def build_proxies(url: str) -> dict[str, str]:
    return dict(https=url, http=url)