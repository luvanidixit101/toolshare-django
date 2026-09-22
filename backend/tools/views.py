from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Category, Tool
from .permissions import IsOwner
from .serializers import (
    CategorySerializer,
    ToolCreateSerializer,
    ToolListSerializer,
)


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get_queryset(self):
        return Category.objects.filter(
            is_active=True
        )


class ToolListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        return (
            Tool.objects
            .filter(
                status=Tool.Status.ACTIVE,
                is_available=True,
                category__is_active=True,
                owner__is_active=True,
            )
            .select_related(
                "owner",
                "category",
            )
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ToolCreateSerializer

        return ToolListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [
            IsAuthenticated(),
            IsOwner(),
        ]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )