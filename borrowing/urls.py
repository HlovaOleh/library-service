from django.urls import path, include
from rest_framework import routers

from borrowing import views
from borrowing.views import borrowing_return

router = routers.DefaultRouter()
router.register("borrowings", views.BorrowingViewSet)

urlpatterns = [
    path("/", include(router.urls)),
    path("borrowings/<int:pk>/return/",
         borrowing_return,
         name="borrowings-return")
]

app_name = "borrowing"
