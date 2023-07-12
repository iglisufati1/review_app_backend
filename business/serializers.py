from common.global_serializers.serializers import UserSerializer
from django.db.models import Avg
from model.models import Category, Product, CategoryRating, ProductRating
from rest_framework import serializers
from waiter.serializers import WaiterReadSerializer


class ProductRatingReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())


class CategoryRatingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())


class ProductReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    product_ratings = serializers.SerializerMethodField()
    product_avg_rating = serializers.SerializerMethodField()

    def get_product_ratings(self, obj):
        product_ratings = ProductRating.objects.select_related('product').filter(product_id=obj.id)
        return ProductRatingReadSerializer(product_ratings, many=True).data

    def get_product_avg_rating(self, obj):
        product_avg_rating = ProductRating.objects.filter(product_id=obj.id).aggregate(Avg('rating'))
        return product_avg_rating.get('rating__avg', None)


class CategoryReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    products = serializers.SerializerMethodField()
    category_ratings = serializers.SerializerMethodField()
    category_avg_rating = serializers.SerializerMethodField()

    def get_products(self, obj):
        products = Product.objects.select_related('category').all()
        return ProductReadSerializer(products, many=True).data

    def get_category_ratings(self, obj):
        category_ratings = CategoryRating.objects.select_related('category').filter(category_id=obj.id)
        return CategoryRatingSerializer(category_ratings, many=True).data

    def get_category_avg_rating(self, obj):
        category_avg_rating = CategoryRating.objects.filter(category_id=obj.id).aggregate(Avg('rating'))
        return category_avg_rating.get('rating__avg', None)


class MenuReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        categories = Category.objects.select_related('menu').all()
        return CategoryReadSerializer(categories, many=True).data


class BusinessReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    address = serializers.CharField()
    nipt = serializers.CharField()
    admins = UserSerializer(many=True, read_only=True)
    waiters = WaiterReadSerializer(many=True, read_only=True)
    business_ratings = ProductRatingReadSerializer(many=True, read_only=True)
    menus = MenuReadSerializer()
    # average_food_rating = serializers.SerializerMethodField()
    # average_beverage_rating = serializers.SerializerMethodField()
    # average_rating = serializers.SerializerMethodField()
    #
    # def get_average_food_rating(self, obj):
    #     average_food_rating = ProductFeedback.objects.filter(product_type='F').aggregate(Avg('rating'))
    #     return average_food_rating.get('rating__avg', None)
    #
    # def get_average_beverage_rating(self, obj):
    #     average_beverage_rating = ProductFeedback.objects.filter(product_type='B').aggregate(Avg('rating'))
    #     return average_beverage_rating.get('rating__avg', None)
    #
    # def get_average_rating(self, obj):
    #     average_ratings = ProductFeedback.objects.filter(product_type__in=['F', 'B'], business=obj).aggregate(
    #         avg_food_rating=Avg(Case(When(product_type='F', then='rating'))),
    #         avg_beverage_rating=Avg(Case(When(product_type='B', then='rating')))
    #     )
    #     avg_food_rating = average_ratings.get('avg_food_rating')
    #     avg_beverage_rating = average_ratings.get('avg_beverage_rating')
    #
    #     return (avg_food_rating + avg_beverage_rating) / 2


class BusinessWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    address = serializers.CharField()
    nipt = serializers.CharField()

    def create(self, validated_data):
        return Business.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.nipt = validated_data.get('nipt', instance.nipt)
        instance.save()
        return instance
