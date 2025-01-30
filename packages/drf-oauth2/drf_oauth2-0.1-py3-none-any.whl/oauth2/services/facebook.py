import urllib.parse

import requests
from django.contrib.auth import get_user_model

from oauth2.config import facebook_config
from oauth2.models import RegisterTypeChoices, UserData
from oauth2.services.register import RegisterService

User = get_user_model()


class FaceBook:
    @staticmethod
    def authenticate(code):
        try:
            token_data = FaceBook._fetch_token(code)
            user_info = FaceBook._fetch_user_info(token_data["access_token"])
            user = FaceBook._get_or_create_user(user_info)
            FaceBook._update_user_data(user, token_data, user_info)
            return RegisterService.get_token(user)
        except (ValueError, requests.RequestException) as e:
            raise ValueError(f"Authentication failed: {str(e)}")

    @staticmethod
    def _fetch_token(code):
        response = requests.post(
            "https://graph.facebook.com/v21.0/oauth/access_token",
            params={
                "client_id": facebook_config["client_id"],
                "client_secret": facebook_config["client_secret"],
                "redirect_uri": facebook_config["redirect_uri"],
                "code": code,
            },
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _fetch_user_info(access_token):
        response = requests.get(
            "https://graph.facebook.com/me",
            params={
                "access_token": access_token,
                "fields": "id,name,email",
            },
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _get_or_create_user(user_info):
        user, created = User.objects.get_or_create(
            email=user_info["email"],
            defaults={
                "username": RegisterService.check_unique_username(
                    user_info["email"].split("@")[0]
                ),
                "first_name": user_info.get("name", "").split()[0],
                "last_name": " ".join(user_info.get("name", "").split()[1:]),
                "is_active": True,
            },
        )
        return user

    @staticmethod
    def _update_user_data(user, token_data, user_info):
        UserData.objects.update_or_create(
            user=user,
            defaults={
                "provider": RegisterTypeChoices.FACEBOOK,
                "uid": user_info["id"],
                "extra_data": {
                    "access_token": token_data["access_token"],
                    "user_info": user_info,
                },
            },
        )

    @staticmethod
    def get_auth_url():
        redirect_uri = facebook_config["redirect_uri"]
        client_id = facebook_config["client_id"]
        api_version = facebook_config["api_version"]
        scopes = [
            # "FaceBook_business_management",
            # "FaceBook_business_messaging",
            "email",
            "public_profile",
        ]
        scope = urllib.parse.quote(" ".join(scopes))
        url = (
            f"https://www.facebook.com/{api_version}/dialog/oauth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}"
        )
        return url


__all__ = ["FaceBook"]
