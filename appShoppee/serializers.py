from rest_framework import serializers
from .models import Product

class GetAllProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name','price','digital','image','category','detail')

# class GetProductWithSearchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('name','price','digital','image','category','detail')