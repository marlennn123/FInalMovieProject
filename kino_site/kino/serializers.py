from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'



class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class JanreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Janre
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Comment
        fields = '__all__'



class MovieSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    reviews = CommentSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    year = serializers.DateField(format=('%Y'))
    director = DirectorSerializer(many=True, read_only=True)
    janre = JanreSerializer(many=True, read_only=True)
    actor = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


    def get_average_rating(self, obj):
        return obj.get_average_rating()



class MovieListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    year = serializers.DateField(format=('%Y'))
    country = CountrySerializer(many=True, read_only=True)
    janre = JanreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id','movie_name', 'movie_image', 'average_rating', 'year', 'country', 'janre']

    def get_average_rating(self, obj):
        return obj.get_average_rating()



class CartItemSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(many=True, read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), write_only=True, source='movie')
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'