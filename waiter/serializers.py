from django.db.models import Avg
from model.models import WaiterRating, Waiter
from rest_framework import serializers


class WaiterRatingReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField()


class WaiterReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    waiter_ratings = WaiterRatingReadSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        average_rating = WaiterRating.objects.filter(waiter=obj.id).aggregate(Avg('rating'))
        return average_rating.get('rating__avg', None)


class WaiterWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def create(self, validated_data):
        return Waiter.objects.create(**validated_data)
