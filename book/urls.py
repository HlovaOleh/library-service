from django.urls import include, path
from rest_framework import routers

from book import views

router = routers.DefaultRouter()
router.register("books", views.BookViewSet)


urlpatterns = [
    path("", include(router.urls))
]

app_name = "book"
