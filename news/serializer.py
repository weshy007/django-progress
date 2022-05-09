from pyexpat import model
from rest_framework import serializers

from .models import WeshyMerch


class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeshyMerch
        fields = ('id', 'name', 'description', 'price')
