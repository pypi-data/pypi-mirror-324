from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.utils.translation import gettext_lazy as _

from .pfx_models import PFXModelMixin


class AbstractPFXBaseUser(PFXModelMixin, AbstractBaseUser):
    """The base abstract user for PFX."""

    class Meta:
        abstract = True

    def auth_json_repr(self):
        return self.json_repr()

    @classmethod
    def auth_json_repr_schema(cls):
        return cls.json_repr_schema()

    def get_user_jwt_signature_key(self):
        """
        Return a user secret to sign JWT token.

        If not empty, the JWT token validity depends on all values
        user to build the return string. So, each time the returned value
        changes, the previously issued tokens will no longer be valid.
        """
        return self.password


class AbstractPFXUser(AbstractUser, AbstractPFXBaseUser):
    """The base abstract user for PFX with permissions mixin."""

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True
