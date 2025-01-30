from django.conf import settings

try:
    SOCIAL_AUTH_CONFIG = settings.SOCIAL_AUTH_CONFIG
except AttributeError:
    SOCIAL_AUTH_CONFIG = {}

google_config = SOCIAL_AUTH_CONFIG.get("google", {})
github_config = SOCIAL_AUTH_CONFIG.get("github", {})
facebook_config = SOCIAL_AUTH_CONFIG.get("facebook", {})
