from django.urls import path

from .views import (
    CategoryListAPIView,
    ToolDetailAPIView,
    ToolListCreateAPIView,
)


app_name = "tools"

urlpatterns = [
    path(
        "",
        ToolListCreateAPIView.as_view(),
        name="tool-list-create",
    ),
    path(
        "categories/",
        CategoryListAPIView.as_view(),
        name="category-list",
    ),

    path(
        "<int:pk>/",
        ToolDetailAPIView.as_view(),
        name="tool-detail",
    ),
]