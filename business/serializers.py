from rest_framework import serializers
from model.models import CustomUser
from common.global_serializers.serializers import UserSerializer


class FeedBackReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField()


class WaiterReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    feedbacks = FeedBackReadSerializer(many=True, read_only=True)


class BusinessReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    address = serializers.CharField()
    nipt = serializers.CharField()
    business_admins = UserSerializer(many=True, read_only=True)
    business_waiters = WaiterReadSerializer(many=True, read_only=True)



class BusinessWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    address = serializers.CharField()
    nipt = serializers.CharField()

    def create(self, validated_data):
        return Business.objects.create(**validated_data)
