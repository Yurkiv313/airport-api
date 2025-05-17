from rest_framework import serializers, viewsets
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated
)


class UniqueFieldsValidatorMixin:
    def validate_unique_fields(
        self, model, unique_fields: dict, message: str, instance=None
    ):
        if not unique_fields:
            return

        queryset = model.objects.filter(**unique_fields)
        if instance is not None:
            queryset = queryset.exclude(pk=instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(message)


class ActionMixin(viewsets.ModelViewSet):
    action_serializers = {}

    def get_serializer_class(self):
        if (
            self.action_serializers
            and self.action in self.action_serializers
        ):
            return self.action_serializers[self.action]
        return super().get_serializer_class()


class CustomPermissionMixin(viewsets.ModelViewSet):
    action_permissions = {}

    def get_permissions(self):
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "upload_image",
        ]:
            if (
                self.__class__.__name__ == "OrderViewSet"
                and self.action == "create"
            ):
                return [IsAuthenticated()]
            return [IsAdminUser()]

        return [
            permission()
            for permission in self.action_permissions.get(
                self.action, [IsAdminUser]
            )
        ]
