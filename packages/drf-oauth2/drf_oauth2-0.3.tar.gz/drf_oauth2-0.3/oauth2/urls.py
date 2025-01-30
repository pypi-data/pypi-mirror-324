from django.urls import path

from oauth2.views import SocialAuthView, AvailableProvidersView

urlpatterns = [
    path("social/register/", SocialAuthView.as_view(), name="social-register"),
    path("social/list/", AvailableProvidersView.as_view(), name="social-list"),
]
