from rest_framework import serializers
from .models import CustomUser, Product, Plan, Order, Contact


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True, source='user')

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        # `user` is already in `validated_data` due to `source='user'`
        return Product.objects.create(**validated_data)


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'plan', 'strip_id']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
