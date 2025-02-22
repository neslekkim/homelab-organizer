import logging

from django.db.models import Count
from django.http import HttpResponse
from django.urls import path
from django.views.generic.base import TemplateView
from taggit.models import Tag

from hlo import views
from hlo.urls import commontree, items, label, scan, utils
from hlo.urls.utils import handler404
from hlo.views import (
    AttachmentSearchView,
    TagDetailView,
    TagListView,
    item_search,
    items_with_tags,
)

logger = logging.getLogger(__name__)


class AboutView(TemplateView):
    template_name = "common/about.html"


def tag_list(_request):
    tags = None
    s = ""
    for tag in tags:
        s += f"{tag}" + "<br>"
        logger.debug(tag)
        logger.debug(tag.taggit_taggeditem_items.count())
        logger.debug(dir(tag))
    return HttpResponse(s)


def items_with_tags_list(_request):
    return HttpResponse("Hello world")


urlpatterns = [
    *[  # This is where dev happens
        path(
            "tags/list",
            TagListView.as_view(),
            name="tag-list",
        ),
        path(
            "tags/detail/<int:pk>",
            TagDetailView.as_view(),
            name="tag-detail",
        ),
        path(
            "tags/items",
            items_with_tags,
            name="tag-items",
        ),
        path(
            "search/items",
            item_search,
            name="item-search",
        ),
        path(
            "search/attachments",
            AttachmentSearchView.as_view(),
            name="attachment-search",
        ),
        path(
            "about",
            AboutView.as_view(),
            name="about",
        ),
    ],
    *label.urls,
    *items.urls,
    *utils.urls,
    *commontree.urls,
    *scan.urls,
]
__all__ = ["urlpatterns", "handler404"]
