from django_filters import FilterSet, NumberFilter
from django.db.models import Avg
from .models import Movie

class MovieFilter(FilterSet):
    average_rating_min = NumberFilter(method='filter_by_min_rating')
    average_rating_max = NumberFilter(method='filter_by_max_rating')

    class Meta:
        model = Movie
        fields = {
            'year': ['gt', 'lt'],
            'janre': ['exact'],
            'country': ['exact'],
        }

    def filter_by_min_rating(self, queryset, name, value):
        return queryset.annotate(average_rating=Avg('ratings__stars')).filter(average_rating__gte=value)

    def filter_by_max_rating(self, queryset, name, value):
        return queryset.annotate(average_rating=Avg('ratings__stars')).filter(average_rating__lte=value)
