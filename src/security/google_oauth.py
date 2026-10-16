from urllib.parse import urlencode

from fastapi import HTTPException
import httpx

from src.config.settings import settings

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

def build_authorize_url(state: str) -> str:
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "prompt": "select_account"
    }
    return f"{AUTH_URL}?{urlencode(params)}"

async def fetch_google_userinfo(code: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(TOKEN_URL, data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            })

            if r.status_code >= 500:
                raise HTTPException(502, "Google đang gặp sự cố, vui lòng thử lại sau")
            if r.status_code != 200:
                raise HTTPException(400, "Mã xác thực Google không hợp lệ hoặc đã hết hạn")

            google_access_token = r.json()["access_token"]

            u = await client.get(USERINFO_URL,
                                 headers={"Authorization": f"Bearer {google_access_token}"})
            if u.status_code != 200:
                raise HTTPException(502, "Không lấy được thông tin người dùng từ Google")

            return u.json()
    except httpx.RequestError:
        raise HTTPException(503, "Không thể kết nối đến máy chủ Google")