from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from oauth2.encoder import PrettyJSONEncoder

User = get_user_model()


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RegisterTypeChoices(models.TextChoices):
    GOOGLE = "GOOGLE", _("Google")
    GITHUB = "GITHUB", _("GitHub")
    FACEBOOK = "FACEBOOK", _("Facebook")


class UserData(AbstractBaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="data",
        verbose_name=_("User"),
        db_index=True,
    )
    provider = models.CharField(
        choices=RegisterTypeChoices,
        max_length=20,
        verbose_name=_("Provider"),
        db_index=True,
    )
    uid = models.CharField(max_length=100, verbose_name=_("Provider ID"), db_index=True)
    extra_data = models.JSONField(
        verbose_name=_("Extra data"), null=True, blank=True, db_index=True, encoder=PrettyJSONEncoder
    )

    class Meta:
        verbose_name = _("User data")
        verbose_name_plural = _("User data")
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.username} {self.user.email}"
            if self.user.email
            else str(_("User"))
        )
