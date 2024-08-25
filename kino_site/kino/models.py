from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True,blank=True)
    STATUS_CHOICES = (
        ('pro', 'pro'),
        ('simple', 'simple'),

    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple', null=True, blank=True)



class Country(models.Model):
    country_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.country_name}'


class Director(models.Model):
    director_name = models.CharField(max_length=32, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    director_image = models.ImageField(upload_to='director_img/', null=True, blank=True)

    def __str__(self):
        return f'{self.director_name}'


class Actor(models.Model):
    actor_name = models.CharField(max_length=32)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    actor_image = models.ImageField(upload_to='actor_img/', null=True, blank=True)

    def __str__(self):
        return f'{self.actor_name}'


class Janre(models.Model):
    janre_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f'{self.janre_name}'


class Movie(models.Model):
    movie_name = models.CharField(max_length=32)
    year = models.DateField(null=True, blank=True)
    country = models.ManyToManyField(Country,)
    director = models.ManyToManyField(Director)
    actor = models.ManyToManyField(Actor,)
    janre = models.ManyToManyField(Janre)
    Type_CHOICES = (
        ('144', '144'),
        ('360', '360'),
        ('480', '480'),
        ('720', '720'),
        ('1080', '1080'),
    )

    type = models.CharField(max_length=10, choices=Type_CHOICES, default='simple', null=True, blank=True)

    movie_time = models.TimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    movie_trailer = models.FileField(upload_to='movie_trailer/', null=True, blank=True)
    movie_image = models.ImageField(upload_to='movie_img/', null=True, blank=True)
    movie = models.FileField(upload_to='movie_film/', null=True, blank=True)
    STATUS_MOVIE = (
        ('pro', 'pro'),
        ('simple', 'simple'),
    )

    status_movie = models.CharField(max_length=10, choices=STATUS_MOVIE, default='simple', null=True, blank=True)
    def __str__(self):
        return f'{self.movie_name}'


    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,)
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1,11)], verbose_name='Рейтинг')


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,)
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='relies', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    created_data = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

