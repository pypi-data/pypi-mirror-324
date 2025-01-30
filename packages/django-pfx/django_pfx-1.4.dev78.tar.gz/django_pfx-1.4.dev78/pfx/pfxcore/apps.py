import logging

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from pfx.pfxcore.shortcuts import permissions, settings

logger = logging.getLogger(__name__)


def update_groups_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group

    groups = {g.name: g for g in Group.objects.all()}

    for name, perms in settings.PFX_AUTH_GROUPS.items():
        created = name not in groups
        group = Group.objects.create(name=name) if created else groups[name]
        if created or not settings.PFX_AUTH_GROUPS_CREATE_ONLY:
            group.permissions.set(permissions(*perms))

    if not settings.PFX_AUTH_GROUPS_CREATE_ONLY:
        names = groups.keys() - settings.PFX_AUTH_GROUPS.keys()
        Group.objects.filter(name__in=names).delete()


class PfxAppConfig(AppConfig):
    def ready(self):
        if settings.PFX_AUTH_GROUPS is not None:
            post_migrate.connect(update_groups_permissions, sender=self)
        return super().ready()


class PfxCoreConfig(AppConfig):
    name = 'pfx.pfxcore'
    default = True
