from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AssetType(str, Enum):
    prompt = "prompt"
    context_pack = "context_pack"
    skill = "skill"
    workflow = "workflow"


class VersionStatus(str, Enum):
    draft = "draft"
    approved = "approved"
    active = "active"
    deprecated = "deprecated"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ReviewStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    skipped = "skipped"


# ====================== 请求模型 ======================
class AssetCreate(BaseModel):
    name: str
    asset_type: AssetType
    description: str = ""
    owner: str
    tags: List[str] = Field(default_factory=list)


class AssetUpdate(BaseModel):
    description: Optional[str] = None
    owner: Optional[str] = None
    tags: Optional[List[str]] = None


class AssetVersionCreate(BaseModel):
    version_tag: str
    system_prompt: str = ""
    context_template: str = ""
    workflow_spec: Dict[str, Any] = Field(default_factory=dict)
    examples: List[Any] = Field(default_factory=list)
    guardrails: List[Any] = Field(default_factory=list)
    variables_schema: Dict[str, Any] = Field(default_factory=dict)
    change_summary: str = ""
    created_by: str
    set_active: bool = True


class ExecutionLogCreate(BaseModel):
    asset_version_id: int
    request_id: Optional[str] = None
    model_name: str = ""
    input_variables: Dict[str, Any] = Field(default_factory=dict)
    llm_output: str = ""
    latency_ms: int = 0
    token_usage: int = 0
    created_by: str = ""


class ChangeRequestCreate(BaseModel):
    commit_sha: str
    pr_id: Optional[str] = None
    asset_id: Optional[int] = None
    asset_version_id: Optional[int] = None
    risk_level: RiskLevel = RiskLevel.low
    impact_scope: List[str] = Field(default_factory=list)
    review_required: bool = False
    review_status: ReviewStatus = ReviewStatus.pending
    notes: str = ""
    created_by: str


class GateCheckRequest(BaseModel):
    commit_sha: str
    is_ai_related: bool = False


# ====================== 响应模型（可选，但推荐） ======================
class AssetResponse(BaseModel):
    id: int
    name: str
    asset_type: AssetType
    description: str
    owner: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime


class AssetVersionResponse(BaseModel):
    id: int
    asset_id: int
    version_tag: str
    status: VersionStatus
    system_prompt: str
    context_template: str
    workflow_spec: Dict[str, Any]
    examples: List[Any]
    guardrails: List[Any]
    variables_schema: Dict[str, Any]
    change_summary: str
    created_by: str
    created_at: datetime
    updated_at: datetime


class ActiveAssetResponse(BaseModel):
    asset_name: str
    asset_type: AssetType
    version_id: int
    version_tag: str
    system_prompt: str
    context_template: str
    workflow_spec: Dict[str, Any]
    examples: List[Any]
    guardrails: List[Any]
    variables_schema: Dict[str, Any]
    change_summary: str


# 你可以继续扩展其他响应模型...
