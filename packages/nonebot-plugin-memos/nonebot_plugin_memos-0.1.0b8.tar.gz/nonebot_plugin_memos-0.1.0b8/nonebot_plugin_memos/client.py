from typing import Any, Type, TypeVar
from nonebot.compat import TypeAdapter
from httpx import AsyncClient, Response
from pydantic import BaseModel
from yarl import URL

from .model import Memo, Visibility

T = TypeVar("T", bound=BaseModel)

TYPE_ADAPTER_CACHE: dict[int, TypeAdapter] = {}


def get_type_adapter(model: Type[T]) -> TypeAdapter[T]:
    model_hash = hash(model)
    if model_hash not in TYPE_ADAPTER_CACHE:
        TYPE_ADAPTER_CACHE[model_hash] = TypeAdapter(model)
    return TYPE_ADAPTER_CACHE[model_hash]


class UnSet:
    pass


class ApiClient:
    def __init__(self, base_url: str, token: str):
        self.base_url: URL = URL(base_url)
        self.client: AsyncClient = AsyncClient(headers={"Authorization": f"Bearer {token}"})
        self.raw_data: list[str] = [base_url, token]

    def update_raw_data(self, base_url: str, token: str):
        if self.raw_data != [base_url, token]:
            self.base_url = URL(base_url)
            self.client.headers["Authorization"] = f"Bearer {token}"
            self.raw_data = [base_url, token]

    async def getAuthStatus(self, token: str | None = None) -> Response:
        return await self.client.post(
            str(self.base_url / "api/v1/auth/status"),
            headers={"Authorization": f"Bearer {token}" if token else self.client.headers.get("Authorization")},
        )

    async def checkAuthStatus(self, token: str | None = None) -> bool:
        try:
            response = await self.getAuthStatus(token)
            return response.status_code == 200
        except Exception:
            return False

    async def createMemo(self, content: str, visibility: str = "VISIBILITY_UNSPECIFIED") -> Response:
        return await self.client.post(
            str(self.base_url / "api/v1/memos"),
            json={"content": content, "visibility": visibility},
        )

    async def createMemoWithModel(self, content: str, visibility: str = "VISIBILITY_UNSPECIFIED") -> Memo:
        response = await self.createMemo(content, visibility)
        response.raise_for_status()
        return get_type_adapter(Memo).validate_json(response.text)

    def buildMemoUrl(self, memo_uid: str) -> str:
        return str(self.base_url / f"m/{memo_uid}")

    async def getMemoByUid(self, uid: str) -> Response:
        return await self.client.get(str(self.base_url / f"api/v1/memos:by-uid/{uid}"))

    async def getMemoByUidWithModel(self, uid: str) -> Memo:
        response = await self.getMemoByUid(uid)
        response.raise_for_status()
        return get_type_adapter(Memo).validate_json(response.text)

    async def createComment(
        self, memo_name: str, content: str, visibility: Visibility | Type[UnSet] = UnSet, resources: list | None = None
    ) -> Response:
        data: dict[str, Any] = {
            "content": content,
        }
        if visibility is not UnSet:
            data["visibility"] = visibility
        if resources:
            data["resources"] = resources
        return await self.client.post(
            str(self.base_url / f"api/v1/{memo_name}/comments"),
            json=data,
        )

    async def createCommentWithModel(
        self, memo_name: str, content: str, visibility: Visibility | Type[UnSet] = UnSet, resources: list | None = None
    ) -> Memo:
        response = await self.createComment(memo_name, content, visibility, resources)
        response.raise_for_status()
        return get_type_adapter(Memo).validate_json(response.text)
