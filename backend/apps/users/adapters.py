from dataclasses import dataclass
from django.conf import settings
from rest_framework.exceptions import ValidationError

@dataclass(frozen=True)
class WechatIdentity:
    openid: str
    nickname: str

class WechatAuthAdapter:
    def exchange(self, payload: dict) -> WechatIdentity:
        raise NotImplementedError

class MockWechatAuthAdapter(WechatAuthAdapter):
    """Local-only adapter. It never calls WeChat."""
    def exchange(self, payload: dict) -> WechatIdentity:
        mock_user = payload.get("mock_user")
        if mock_user not in {"user_a", "user_b", "user_c"}:
            raise ValidationError({"mock_user": "must be user_a, user_b or user_c"})
        return WechatIdentity(openid=f"mock:{mock_user}", nickname=mock_user.upper())

class RealWechatAuthAdapter(WechatAuthAdapter):
    def exchange(self, payload: dict) -> WechatIdentity:
        raise ValidationError("Wechat code2Session adapter is not configured in this Demo")

def get_wechat_auth_adapter() -> WechatAuthAdapter:
    return MockWechatAuthAdapter() if settings.WECHAT_AUTH_MODE == "mock" else RealWechatAuthAdapter()
