from django.contrib import admin

from .models import Category, Tool


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "category",
        "price_per_day",
        "condition",
        "status",
        "city",
        "is_available",
        "created_at",
    )

    list_filter = (
        "status",
        "condition",
        "is_available",
        "category",
        "city",
    )

    search_fields = (
        "title",
        "description",
        "owner__email",
        "city",
        "address",
    )

    autocomplete_fields = (
        "owner",
        "category",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "owner",
        "category",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "owner",
                    "category",
                    "title",
                    "description",
                ),
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "price_per_day",
                    "security_deposit",
                ),
            },
        ),
        (
            "Tool Status",
            {
                "fields": (
                    "condition",
                    "status",
                    "is_available",
                ),
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "address",
                    "city",
                    "latitude",
                    "longitude",
                ),
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )