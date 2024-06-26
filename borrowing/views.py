from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
    BorrowingListSerializer
)
from payment.services import get_payment


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.select_related("book", "user")
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        else:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                queryset = queryset.filter(user__id=user_id)
        is_active = str(self.request.query_params.get("is_active"))

        if is_active == "True":
            queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.filter(is_active=False)
        return queryset

    def get_serializer_class(self):

        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "list":
            return BorrowingListSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=bool,
                description="Filter by borrowing status (ex. ?is_active=True)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=["POST"])
    @transaction.atomic
    def return_book(self, request, pk=None):
        """Endpoint for returning book"""
        borrowing = self.get_object()

        if borrowing.is_active:
            borrowing.is_active = False
            borrowing.actual_return_date = timezone.now().date()
            get_payment(borrowing)
            borrowing.book.inventory += 1
            borrowing.book.save()
            borrowing.save()

            return Response(
                {"status": "success", "message":
                    "Thank you! The book is returned "},
                status=status.HTTP_200_OK
            )

        return Response(
            {"status": "fail", "message": "Book is already returned"},
            status=status.HTTP_400_BAD_REQUEST
        )
