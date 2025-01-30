import importlib
import os

from django.conf import settings


def get_admin_model(name):
    """
    Check if the given name is a custom admin.

    Args:
        name (str): The name to check.

    Returns:
        ModelAdmin: The appropriate ModelAdmin class.
    """
    if name in settings.INSTALLED_APPS:
        from unfold.admin import ModelAdmin

        return ModelAdmin

    from django.contrib.admin import ModelAdmin

    return ModelAdmin


def load_providers():
    providers = {}
    services_dir = os.path.dirname(__file__) + "/services"

    for filename in os.listdir(services_dir):
        if filename.endswith(".py") and filename not in ["__init__.py", "base.py"]:
            module_name = f"oauth2.services.{filename[:-3]}"
            module = importlib.import_module(module_name)

            if hasattr(module, "Provider"):
                provider_instance = getattr(module, "Provider")()
                if provider_instance.client_id and provider_instance.client_secret:
                    providers[filename[:-3]] = provider_instance

    return providers


OAUTH_PROVIDERS = load_providers()
