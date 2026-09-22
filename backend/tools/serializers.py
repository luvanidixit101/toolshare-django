from rest_framework import serializers
from accounts.models import User
from .models import Category, Tool


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "description",
        )
        read_only_fields = fields

class ToolCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
    )

    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Tool
        fields = (
            "id",
            "owner",
            "category",
            "title",
            "description",
            "price_per_day",
            "security_deposit",
            "condition",
            "status",
            "address",
            "city",
            "latitude",
            "longitude",
            "is_available",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "owner",
            "created_at",
            "updated_at",
        )

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Tool title cannot be empty."
            )

        return value

    def validate_description(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Tool description cannot be empty."
            )

        return value

    def validate_city(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "City cannot be empty."
            )

        return value

    def validate_latitude(self, value):
        if value is not None and not (-90 <= value <= 90):
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90."
            )

        return value

    def validate_longitude(self, value):
        if value is not None and not (-180 <= value <= 180):
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180."
            )

        return value



class ToolOwnerSerializer(serializers.ModelSerializer):
    is_email_verified = serializers.BooleanField(
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "is_email_verified",
        )
        read_only_fields = fields


class ToolCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
        )
        read_only_fields = fields


class ToolListSerializer(serializers.ModelSerializer):
    owner = ToolOwnerSerializer(
        read_only=True,
    )

    category = ToolCategorySerializer(
        read_only=True,
    )

    class Meta:
        model = Tool
        fields = (
            "id",
            "owner",
            "category",
            "title",
            "description",
            "price_per_day",
            "security_deposit",
            "condition",
            "city",
            "is_available",
            "created_at",
        )

        read_only_fields = fields


class ToolDetailSerializer(serializers.ModelSerializer):
    owner = ToolOwnerSerializer(
        read_only=True,
    )

    category = ToolCategorySerializer(
        read_only=True,
    )

    class Meta:
        model = Tool
        fields = (
            "id",
            "owner",
            "category",
            "title",
            "description",
            "price_per_day",
            "security_deposit",
            "condition",
            "status",
            "city",
            "is_available",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields

class MyToolSerializer(serializers.ModelSerializer):
    category = ToolCategorySerializer(
        read_only=True,
    )

    class Meta:
        model = Tool
        fields = (
            "id",
            "category",
            "title",
            "description",
            "price_per_day",
            "security_deposit",
            "condition",
            "status",
            "address",
            "city",
            "latitude",
            "longitude",
            "is_available",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


class ToolUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
    )

    class Meta:
        model = Tool
        fields = (
            "category",
            "title",
            "description",
            "price_per_day",
            "security_deposit",
            "condition",
            "status",
            "address",
            "city",
            "latitude",
            "longitude",
            "is_available",
        )

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Tool title cannot be empty."
            )

        return value

    def validate_description(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Tool description cannot be empty."
            )

        return value

    def validate_address(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Address cannot be empty."
            )

        return value

    def validate_city(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "City cannot be empty."
            )

        return value

    def validate_latitude(self, value):
        if value is not None and not (-90 <= value <= 90):
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90."
            )

        return value

    def validate_longitude(self, value):
        if value is not None and not (-180 <= value <= 180):
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180."
            )

        return value