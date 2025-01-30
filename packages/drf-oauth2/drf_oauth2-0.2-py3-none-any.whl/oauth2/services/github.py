import requests
from django.contrib.auth import get_user_model

from oauth2.config import github_config
from oauth2.models import UserData, RegisterTypeChoices
from oauth2.services.register import RegisterService

User = get_user_model()


class Github:
    @staticmethod
    def authenticate(code):
        try:
            token_data = Github._fetch_token(code)
            user_info, email = Github._fetch_user_info(token_data["access_token"])
            user = Github._get_or_create_user(user_info, email)
            Github._update_user_data(user, user_info)
            return RegisterService.get_token(user)
        except (ValueError, requests.RequestException) as e:
            raise ValueError(f"Authentication failed: {str(e)}")

    @staticmethod
    def _fetch_token(code):
        response = requests.post(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id": github_config["client_id"],
                "client_secret": github_config["client_secret"],
                "code": code,
                "redirect_uri": github_config["redirect_uri"],
            },
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _fetch_user_info(access_token):
        user_response = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"},
        )
        user_response.raise_for_status()
        user_info = user_response.json()

        email = user_info.get("email")
        if not email:
            emails_response = requests.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"token {access_token}"},
            )
            emails_response.raise_for_status()
            emails = emails_response.json()
            email = next((email["email"] for email in emails if email["primary"]), None)

        if not email:
            raise ValueError("GitHub email not found")

        return user_info, email

    @staticmethod
    def _get_or_create_user(user_info, email):
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": RegisterService.check_unique_username(user_info["login"]),
                "first_name": (
                    user_info.get("name", "").split()[0]
                    if user_info.get("name")
                    else ""
                ),
                "last_name": (
                    user_info.get("name", "").split()[-1]
                    if user_info.get("name")
                    else ""
                ),
                "is_active": True,
            },
        )
        return user

    @staticmethod
    def _update_user_data(user, user_info):
        UserData.objects.update_or_create(
            user=user,
            defaults={
                "provider": RegisterTypeChoices.GITHUB,
                "uid": user_info["id"],
                "extra_data": user_info,
            },
        )

    @staticmethod
    def get_auth_url():
        client_id = github_config["client_id"]
        redirect_uri = github_config["redirect_uri"]
        scopes = "user:email"
        return f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}"


__all__ = ["Github"]
