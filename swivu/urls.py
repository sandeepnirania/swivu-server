from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("board/", include("boards.urls")),
]
