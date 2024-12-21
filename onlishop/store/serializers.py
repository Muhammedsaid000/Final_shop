from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username', 'email', 'password')
        extra_kwargs={'password':{'write_only':True}}

    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user


    def to_representation(self, instance):
        refresh=RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LoginSerializers(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        user=authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh=RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields=['first_name','last_name']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    date_registered=serializers.DateTimeField(format('%d-%m-%Y-%H-%M'))
    class Meta:
        model = UserProfile
        fields=['first_name','last_name','age','status','date_registered',]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=['category_name']


class ProductPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields=['image']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields='__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author=UserProfileSerializer()

    class Meta:
        model = Review
        fields=['author', 'text', 'parent_review','created_date']


class ProductSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model = Product
        fields=['product_name','category','price','active']


class ProductDetailSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    owner=UserProfileSerializer()
    date=serializers.DateField(format('%d-%m-%Y'))
    product=ProductPhotosSerializers(read_only=True, many=True)
    review=ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields=['product_name','description','category',
                'price','product_video','product','active','date','owner','review']