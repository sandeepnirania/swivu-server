from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<slug>[a-z-]+)/?$', views.BoardActionView.as_view(), name="board_action"),
]
