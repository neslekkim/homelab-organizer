from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin  # type: ignore[import-untyped]

from hlo.models import Project


@admin.register(Project)
class ProjectAdmin(
    DraggableMPTTAdmin,
):
    list_display = ("tree_actions", "indented_title")
    list_display_links = ("indented_title",)
