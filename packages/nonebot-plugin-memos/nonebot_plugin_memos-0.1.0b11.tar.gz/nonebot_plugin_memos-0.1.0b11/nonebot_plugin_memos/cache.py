from .client import ApiClient


CLIENT_CACHE: dict[int, ApiClient] = {}


def get_client(id_: int, url: str, token: str) -> ApiClient:
    if id_ in CLIENT_CACHE:
        CLIENT_CACHE[id_].update_raw_data(url, token)
    CLIENT_CACHE[id_] = ApiClient(url, token)
    return CLIENT_CACHE[id_]
