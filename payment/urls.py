from rest_framework.routers import DefaultRouter

from payment.views import PaymentViewSet

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payments")

urlpatterns = router.urls

app_name = "payment"
