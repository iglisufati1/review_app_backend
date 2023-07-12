from io import BytesIO
from waiter_rating.serializers import WaiterRatingReadSerializer
import qrcode
from django.core.files import File
from django.db.models import Avg
from model.models import WaiterRating, Waiter
from rest_framework import serializers
class WaiterReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    waiter_ratings = WaiterRatingReadSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    qr_code = serializers.CharField()

    def get_average_rating(self, obj):
        average_rating = WaiterRating.objects.filter(waiter=obj.id).aggregate(Avg('rating'))
        return average_rating.get('rating__avg', None)


class WaiterWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def create(self, validated_data):
        waiter = Waiter.objects.create(**validated_data)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"Waiter ID: {waiter.id}")
        qr.make(fit=True)
        qr_image = qr.make_image(fill='black', back_color='white')
        qr_image_io = BytesIO()
        qr_image.save(qr_image_io, format='PNG')
        waiter.qr_code.save(f'qr_code_{waiter.first_name}_{waiter.last_name}_{waiter.id}.png', File(qr_image_io), save=False)
        return waiter

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


