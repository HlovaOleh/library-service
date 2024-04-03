from rest_framework.routers import DefaultRouter

from book.views import BookViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")


urlpatterns = router.urls

app_name = "book"
