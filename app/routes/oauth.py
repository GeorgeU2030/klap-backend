from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.auth.oauth import oauth
from app.database import get_db
from app.services.user_service import get_user_by_google_id, get_user_by_email, create_oauth_user
from app.auth.jwt import create_access_token, create_refresh_token
from app.config import settings
from datetime import timedelta

router = APIRouter(tags=["OAuth"])

@router.get("/login/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for('auth_via_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google")
async def auth_via_google(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token['userinfo']
        
        user = get_user_by_google_id(db, user_info['sub'])
        
        if not user:
            
            existing_user = get_user_by_email(db, user_info['email'])
            
            if existing_user and not existing_user.is_oauth:
                error_url = f"{settings.FRONTEND_URL}/login?error=email_exists_traditional"
                return RedirectResponse(url=error_url)
            elif existing_user:
                existing_user.google_id = user_info['sub']
                existing_user.profile_image = user_info.get('picture')
                db.commit()
                user = existing_user
            else:
                user = create_oauth_user(
                    db, 
                    user_info['email'], 
                    user_info.get('name', ''),
                    user_info['sub'], 
                    user_info.get('picture')
                )
        else:
            if user.profile_image != user_info.get('picture'):
                user.profile_image = user_info.get('picture')
                db.commit()
        
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        refresh_token = create_refresh_token(
            data={"sub": user.email}
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )
        
        frontend_url = f"{settings.FRONTEND_URL}/auth/callback?token={access_token}&user={user.email}"
        return RedirectResponse(url=frontend_url)
        
    except Exception:
        error_url = f"{settings.FRONTEND_URL}/login?error=auth_failed"
        return RedirectResponse(url=error_url)
