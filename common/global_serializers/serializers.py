from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
