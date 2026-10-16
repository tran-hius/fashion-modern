import secrets

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse

from src.config.settings import settings
from src.dependencies import (
    get_auth_service,
    get_current_user,
    get_current_user_id,
)
from src.models.user import User
from src.schemas.token import RefreshRequest, TokenResponse
from src.schemas.user import UserMeResponse
from src.security.google_oauth import build_authorize_url
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

STATE_COOKIE = "oauth_state"


@router.get("/google/login")
async def google_login():
    """Bước 1-2: chuyển hướng người dùng sang Google."""
    state = secrets.token_urlsafe(16)
    response = RedirectResponse(build_authorize_url(state))
    response.set_cookie(
        STATE_COOKIE,
        state,
        max_age=600,
        httponly=True,
        samesite="lax",   # cần lax để cookie đi kèm lúc Google redirect về
        secure=(settings.app_env == "production"),
    )
    return response


# TODO: khi có frontend, chuyển sang POST /auth/google/callback nhận GoogleLoginRequest(code); frontend tự tạo và kiểm tra state. KHÔNG đưa token lên query string của URL.
@router.get("/google/callback", response_model=TokenResponse)
async def google_callback(
    request: Request,
    response: Response,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    service: AuthService = Depends(get_auth_service),
):
    """Bước 4-6: Google gọi về đây kèm code, ta đổi lấy thông tin rồi cấp token."""
    if error or not code:
        raise HTTPException(400, "Bạn đã từ chối hoặc Google trả về lỗi")

    saved_state = request.cookies.get(STATE_COOKIE)
    if not state or not saved_state or not secrets.compare_digest(state, saved_state):
        raise HTTPException(400, "State không hợp lệ")

    tokens = await service.login_with_google(code)
    response.delete_cookie(STATE_COOKIE)   # state chỉ dùng một lần
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    body: RefreshRequest,
    service: AuthService = Depends(get_auth_service),
):
    return await service.refresh(body.refresh_token)


@router.post("/logout", status_code=204)
async def logout(
    body: RefreshRequest,
    service: AuthService = Depends(get_auth_service),
):
    await service.logout(body.refresh_token)


@router.post("/logout-all", status_code=204)
async def logout_all(
    user_id: int = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service),
):
    await service.logout_all(user_id)


@router.get("/me", response_model=UserMeResponse)
async def me(user: User = Depends(get_current_user)):
    return user