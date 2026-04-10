from echo_saas_sdk import EchoSaasClient
from echo_saas_sdk.models import AssetCreate, AssetVersionCreate, ExecutionLogCreate

client = EchoSaasClient(base_url="http://localhost:8000")   # 生产换成你的域名

# 1. 创建资产
asset = client.create_asset(AssetCreate(
    name="my_chat_prompt",
    asset_type="prompt",
    owner="team-ai",
    tags=["gpt-4o"]
))

# 2. 创建版本并激活
version = client.create_version(
    asset_id=asset.id,
    payload=AssetVersionCreate(
        version_tag="v1.0",
        system_prompt="你是专业的助手...",
        created_by="dev1",
        set_active=True
    )
)

# 3. 获取当前激活版本（最常用！）
active = client.get_active_version("my_chat_prompt")
print(active.system_prompt)

# 4. 记录执行日志（异步推荐）
await client.alog_execution(ExecutionLogCreate(
    asset_version_id=version.id,
    request_id="req-123",
    model_name="gpt-4o",
    llm_output="回复内容...",
    latency_ms=245,
    token_usage=128,
    created_by="user123"
))echo-saas-sdk/
├── echo_saas_sdk/
│   ├── __init__.py          from .client import EchoSaasClient
│   ├── client.py
│   ├── models.py
│   └── exceptions.py
├── pyproject.toml
├── README.md
├── LICENSE                  
├── .gitignore
├── .github/workflows/publish.yml   
└── tests/                   

# Echo SaaS SDK (Python)

Official Python SDK for [Echo Prompt Manager](https://github.com/PeterShanxin/echo-saas)

```bash
pip install echo-saas-sdk
