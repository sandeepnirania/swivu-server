from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<slug>[a-z-]+)/sync/?$', views.BoardSyncView.as_view(), name="board_sync"),
]
