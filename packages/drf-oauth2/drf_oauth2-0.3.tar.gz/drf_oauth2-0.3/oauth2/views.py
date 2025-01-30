from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from oauth2.config import facebook_config, github_config, google_config
from oauth2.serializers import SocialAuthSerializer
from oauth2.services.facebook import FaceBook
from oauth2.services.github import Github
from oauth2.services.google import Google

OAUTH_PROVIDERS = {}

if google_config.get("client_id") and google_config.get("client_secret"):
    OAUTH_PROVIDERS["google"] = Google

if facebook_config.get("client_id") and facebook_config.get("client_secret"):
    OAUTH_PROVIDERS["facebook"] = FaceBook

if github_config.get("client_id") and github_config.get("client_secret"):
    OAUTH_PROVIDERS["github"] = Github


class SocialAuthView(GenericAPIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]
    serializer_class = SocialAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider_name = serializer.validated_data.get("provider")
        code = serializer.validated_data.get("code")

        provider = self.get_provider(provider_name)
        if not provider:
            return Response(
                {"success": False, "message": "Unsupported provider"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            jwt_token = provider.authenticate(code)
            return Response(
                {
                    "success": True,
                    "message": "Authentication successful",
                    "data": jwt_token,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return self.error_response(str(e), status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return self.error_response(
                f"Missing key: {str(e)}", status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return self.error_response(
                f"An unexpected error occurred: {str(e)}",
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider_name = serializer.validated_data.get("provider")
        provider = self.get_provider(provider_name)
        if not provider:
            return self.error_response(
                "Unsupported provider", status.HTTP_400_BAD_REQUEST
            )

        try:
            url = provider.get_auth_url()
            return Response(
                {
                    "success": True,
                    "message": "Redirecting to provider",
                    "data": {"url": url},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return self.error_response(
                f"An unexpected error occurred: {str(e)}",
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def get_provider(provider_name):
        """Retrieve the provider class dynamically."""
        return OAUTH_PROVIDERS.get(provider_name.lower())

    @staticmethod
    def error_response(message, status_code):
        """Reusable error response helper."""
        return Response({"success": False, "message": message}, status=status_code)


class AvailableProvidersView(APIView):
    def get(self, request):
        return Response(
            {
                "success": True,
                "message": "Available providers",
                "data": list(OAUTH_PROVIDERS.keys()),
            }
        )
