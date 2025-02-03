from nonebot_plugin_alconna import Image
from httpx import AsyncClient


async def get_image_bytes(image: Image):
    try:
        return image.raw_bytes
    except:
        pass

    if image.url is None:
        return None

    async with AsyncClient() as client:
        resp = await client.get(image.url)
        return resp.content