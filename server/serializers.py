from rest_framework import serializers
from .models import User, Seller

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_seller', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'