import json
from datetime import timedelta
from uuid import uuid4

import requests
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterService:
    @staticmethod
    def check_unique_username(username: str):
        username = "".join(username.split(" ")).lower()

        if not User.objects.filter(username=username).exists():
            return username
        else:
            random_username = username + str(uuid4().hex[:12])
            return RegisterService.check_unique_username(random_username)

    @staticmethod
    def get_location(ip_address: str):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()
            return data
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def filter_meta(meta):
        serializable_meta = {}
        for key, value in meta.items():
            try:
                json.dumps({key: value})
                serializable_meta[key] = value
            except (TypeError, ValueError):
                continue
        return serializable_meta

    @staticmethod
    def get_client_ip(request):
        """
        Extract client IP address from request metadata.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        return ip

    @staticmethod
    def get_expired_at():
        return timezone.now() + timedelta(days=30)

    @staticmethod
    def get_token(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user.id,
            "expired_at": RegisterService.get_expired_at(),
        }
