import urllib.parse

import requests
from django.contrib.auth import get_user_model
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from oauth2.config import google_config
from oauth2.models import RegisterTypeChoices, UserData
from oauth2.services.register import RegisterService

User = get_user_model()


class Google:
    @staticmethod
    def authenticate(code):
        try:
            token_data = Google._fetch_token(code)
            idinfo = Google._verify_token(token_data["id_token"])
            user = Google._get_or_create_user(idinfo)
            Google._update_user_data(user, idinfo)
            return RegisterService.get_token(user)
        except (ValueError, requests.RequestException) as e:
            raise ValueError(f"Authentication failed: {str(e)}")

    @staticmethod
    def _fetch_token(code):
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": google_config["client_id"],
                "client_secret": google_config["client_secret"],
                "redirect_uri": google_config["redirect_uri"],
                "grant_type": "authorization_code",
            },
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _verify_token(token):
        return id_token.verify_oauth2_token(
            token, google_requests.Request(), google_config["client_id"]
        )

    @staticmethod
    def _get_or_create_user(idinfo):
        user, created = User.objects.get_or_create(
            email=idinfo["email"],
            defaults={
                "username": RegisterService.check_unique_username(
                    idinfo["email"].split("@")[0]
                ),
                "first_name": idinfo.get("given_name", ""),
                "last_name": idinfo.get("family_name", ""),
                "is_active": True,
            },
        )
        return user

    @staticmethod
    def _update_user_data(user, idinfo):
        UserData.objects.update_or_create(
            user=user,
            defaults={
                "provider": RegisterTypeChoices.GOOGLE,
                "uid": idinfo["sub"],
                "extra_data": idinfo,
            },
        )

    @staticmethod
    def get_auth_url():
        redirect_uri = google_config["redirect_uri"]
        client_id = google_config["client_id"]

        if not redirect_uri or not client_id:
            raise ValueError("GOOGLE_REDIRECT_URI yoki GOOGLE_CLIENT_ID aniqlanmagan.")

        scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ]

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(scopes),
            "access_type": "offline",  # Ushbu parametrni "refresh token" olish uchun qo'shishingiz mumkin
            "prompt": "consent",  # Foydalanuvchi har doim ruxsatni tasdiqlashi uchun
        }

        url = f"https://accounts.google.com/o/oauth2/auth?{urllib.parse.urlencode(params)}"
        return url


__all__ = ["Google"]
