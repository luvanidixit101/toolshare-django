from django.urls import path

from .views import (
    CategoryListAPIView,
    MyToolListAPIView,
    ToolDetailAPIView,
    ToolListCreateAPIView,
    ToolUpdateAPIView,
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
        "mine/",
        MyToolListAPIView.as_view(),
        name="my-tool-list",
    ),
    
    path(
        "<int:pk>/manage/",
        ToolUpdateAPIView.as_view(),
        name="tool-update",
    ),

    path(
        "<int:pk>/",
        ToolDetailAPIView.as_view(),
        name="tool-detail",
    ),
]