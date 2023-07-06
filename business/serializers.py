from rest_framework import serializers
from model.models import CustomUser, ProductFeedback, WaiterFeedback
from common.global_serializers.serializers import UserSerializer
from django.db.models import Avg, Case, When

class WaiterFeedBackReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField()


class ProductFeedBackReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_type = serializers.CharField()
    rating = serializers.IntegerField()



class WaiterReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    waiter_feedbacks = WaiterFeedBackReadSerializer(many=True, read_only=True)
    average_feedback = serializers.SerializerMethodField()

    def get_average_feedback(self, obj):
        average_feedback = WaiterFeedback.objects.filter(waiter=obj.id).aggregate(Avg('rating'))
        return average_feedback.get('rating__avg', None)


class BusinessReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    address = serializers.CharField()
    nipt = serializers.CharField()
    admins = UserSerializer(many=True, read_only=True)
    waiters = WaiterReadSerializer(many=True, read_only=True)
    business_feedbacks = ProductFeedBackReadSerializer(many=True, read_only=True)
    average_food_rating = serializers.SerializerMethodField()
    average_beverage_rating = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_average_food_rating(self, obj):
        average_food_rating = ProductFeedback.objects.filter(product_type='F').aggregate(Avg('rating'))
        return average_food_rating.get('rating__avg', None)

    def get_average_beverage_rating(self, obj):
        average_beverage_rating = ProductFeedback.objects.filter(product_type='B').aggregate(Avg('rating'))
        return average_beverage_rating.get('rating__avg', None)

    def get_average_rating(self, obj):
        average_ratings = ProductFeedback.objects.filter(product_type__in=['F', 'B'], business=obj).aggregate(
            avg_food_rating=Avg(Case(When(product_type='F', then='rating'))),
            avg_beverage_rating=Avg(Case(When(product_type='B', then='rating')))
        )
        avg_food_rating = average_ratings.get('avg_food_rating')
        avg_beverage_rating = average_ratings.get('avg_beverage_rating')

        return (avg_food_rating + avg_beverage_rating) / 2


class BusinessWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    address = serializers.CharField()
    nipt = serializers.CharField()

    def create(self, validated_data):
        return Business.objects.create(**validated_data)
