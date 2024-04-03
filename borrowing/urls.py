from rest_framework.routers import DefaultRouter

from borrowing.views import BorrowingViewSet

router = DefaultRouter()
router.register("borrowings", BorrowingViewSet, basename="borrowing")

urlpatterns = router.urls

app_name = "borrowing"
