from django.contrib import admin
from .models import Actor, Director, Genre, Movie, Recommend, Record, Review

# Register your models here.

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Review)
admin.site.register(Record)
admin.site.register(Recommend)
