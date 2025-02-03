from nonebot_plugin_alconna import Image
from httpx import AsyncClient
from filetype import guess_mime

async def get_image_bytes(image: Image):
    try:
        content = image.raw_bytes
        return content, guess_mime(content) or ""
    except Exception:
        pass

    if image.url is None:
        return None

    async with AsyncClient() as client:
        resp = await client.get(image.url)
        content = resp.content
        return resp.content, guess_mime(content) or ""