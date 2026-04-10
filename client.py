import httpx
from typing import Optional, Dict, Any, List
from .models import *
from .exceptions import EchoSaasError, EchoSaasAPIError


class EchoSaasClient:
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"  # 未来后端加认证后直接可用

        self.client = httpx.Client(base_url=base_url, headers=headers, timeout=timeout)
        self.async_client = httpx.AsyncClient(base_url=base_url, headers=headers, timeout=timeout)

    # ==================== 资产管理 ====================
    def create_asset(self, payload: AssetCreate) -> AssetResponse:
        r = self.client.post("/api/assets/", json=payload.model_dump())
        self._raise_for_status(r)
        return AssetResponse.model_validate(r.json())

    def list_assets(
        self,
        q: Optional[str] = None,
        asset_type: Optional[AssetType] = None,
        owner: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[AssetResponse]:
        params = {k: v for k, v in locals().items() if k != "self" and v is not None}
        r = self.client.get("/api/assets/", params=params)
        self._raise_for_status(r)
        return [AssetResponse.model_validate(item) for item in r.json()]

    def get_asset(self, asset_id: int) -> Dict[str, Any]:
        r = self.client.get(f"/api/assets/{asset_id}")
        self._raise_for_status(r)
        return r.json()

    def update_asset(self, asset_id: int, payload: AssetUpdate) -> AssetResponse:
        r = self.client.patch(f"/api/assets/{asset_id}", json=payload.model_dump(exclude_unset=True))
        self._raise_for_status(r)
        return AssetResponse.model_validate(r.json())

    # ==================== 版本控制 ====================
    def create_version(self, asset_id: int, payload: AssetVersionCreate) -> AssetVersionResponse:
        r = self.client.post(f"/api/assets/{asset_id}/versions/", json=payload.model_dump())
        self._raise_for_status(r)
        return AssetVersionResponse.model_validate(r.json())

    def list_versions(self, asset_id: int) -> List[AssetVersionResponse]:
        r = self.client.get(f"/api/assets/{asset_id}/versions/")
        self._raise_for_status(r)
        return [AssetVersionResponse.model_validate(item) for item in r.json()]

    def activate_version(self, asset_id: int, version_id: int) -> AssetVersionResponse:
        r = self.client.post(f"/api/assets/{asset_id}/versions/{version_id}/activate")
        self._raise_for_status(r)
        return AssetVersionResponse.model_validate(r.json())

    def get_active_version(self, name: str) -> ActiveAssetResponse:
        """最常用接口：获取当前激活版本"""
        r = self.client.get(f"/api/services/assets/{name}/active")
        self._raise_for_status(r)
        return ActiveAssetResponse.model_validate(r.json())

    # ==================== 执行日志 ====================
    def log_execution(self, payload: ExecutionLogCreate) -> Dict[str, Any]:
        r = self.client.post("/api/logs/", json=payload.model_dump())
        self._raise_for_status(r)
        return r.json()

    def list_logs(
        self,
        asset_version_id: Optional[int] = None,
        request_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        params = {"limit": limit}
        if asset_version_id is not None:
            params["asset_version_id"] = asset_version_id
        if request_id is not None:
            params["request_id"] = request_id
        r = self.client.get("/api/logs/", params=params)
        self._raise_for_status(r)
        return r.json()

    # ==================== 变更 & 门禁 ====================
    def create_change_request(self, payload: ChangeRequestCreate) -> Dict[str, Any]:
        r = self.client.post("/api/changes/", json=payload.model_dump())
        self._raise_for_status(r)
        return r.json()

    def list_change_requests(
        self, review_status: Optional[ReviewStatus] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        params = {"limit": limit}
        if review_status:
            params["review_status"] = review_status.value
        r = self.client.get("/api/changes/", params=params)
        self._raise_for_status(r)
        return r.json()

    def get_change_request(self, commit_sha: str) -> Dict[str, Any]:
        r = self.client.get(f"/api/changes/{commit_sha}")
        self._raise_for_status(r)
        return r.json()

    def gate_check(self, payload: GateCheckRequest) -> Dict[str, Any]:
        r = self.client.post("/api/gates/check", json=payload.model_dump())
        self._raise_for_status(r)
        return r.json()

    # ==================== 异步方法（推荐 LLM 调用时使用） ====================
    async def aget_active_version(self, name: str) -> ActiveAssetResponse:
        r = await self.async_client.get(f"/api/services/assets/{name}/active")
        self._raise_for_status(r)
        return ActiveAssetResponse.model_validate(r.json())

    async def alog_execution(self, payload: ExecutionLogCreate) -> Dict[str, Any]:
        r = await self.async_client.post("/api/logs/", json=payload.model_dump())
        self._raise_for_status(r)
        return r.json()

    # ==================== 工具方法 ====================
    def _raise_for_status(self, response: httpx.Response):
        if response.status_code >= 400:
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            raise EchoSaasAPIError(response.status_code, detail)

    def close(self):
        self.client.close()
        self.async_client.aclose()

    async def aclose(self):
        await self.async_client.aclose()


# 方便导入
__all__ = ["EchoSaasClient"]
