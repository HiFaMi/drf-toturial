from django.contrib.auth import get_user_model
from rest_framework import serializers

__all__ = (
    'UserListSerializer',
)

User = get_user_model()


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
        )


class UserListSerializer(UserBaseSerializer):
    pass


