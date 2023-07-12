from datetime import date

from model.models import WaiterRating, Waiter
from rest_framework import serializers


class WaiterRatingReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField()
    client_device = serializers.CharField(read_only=True)


class WaiterRatingWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    client_device = serializers.CharField(read_only=True)
    rating = serializers.IntegerField()
    waiter = serializers.PrimaryKeyRelatedField(queryset=Waiter.objects.all())

    def create(self, validated_data):
        request = self.context.get('request')
        client_device = request.META.get('HTTP_CLIENT_DEVICE')
        validated_data['client_device'] = client_device
        today = date.today()
        current_month = timezone.now().month
        today_ratings = WaiterRating.objects.filter(client_device=client_device, date_created__date=today)
        month_ratings = WaiterRating.objects.filter(client_device=client_device, date_created__month=current_month)
        if (len(today_ratings)) < 3:
            if (len(month_ratings)) < 7:
                return WaiterRating.objects.create(**validated_data)
            else:
                raise serializers.ValidationError('Ju keni arritur limitin e vleresimeve per kete muaj')
        else:
            raise serializers.ValidationError('Ju keni arritur limitin e vleresimeve per sot')
