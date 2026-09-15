from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128)


class UserInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    role = serializers.CharField()


def serialize_user(user) -> dict:
    role = user.profile.role if hasattr(user, 'profile') else ''
    return {'id': user.id, 'username': user.username, 'role': role}
