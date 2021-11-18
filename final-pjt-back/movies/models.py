from django.db import models
from django.conf import settings

# 장르


class Genre(models.Model):
    tmdb_id = models.IntegerField()
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

# 영화


class Movie(models.Model):
    genres = models.ManyToManyField(Genre, related_name='movies')
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    tmdb_vote_sum = models.FloatField()
    tmdb_vote_cnt = models.IntegerField()
    updated_vote_sum = models.FloatField()
    updated_vote_cnt = models.IntegerField()
    overview = models.TextField()
    poster_path = models.TextField()
    backdrop_path = models.TextField()

    def __str__(self) -> str:
        return self.title


# 감독
class Director(models.Model):
    director_id = models.IntegerField()
    movies = models.ManyToManyField(Movie, related_name='directors')
    name = models.CharField(max_length=100)
    profile_path = models.TextField()
    popularity = models.FloatField()

    def __str__(self) -> str:
        return self.name


# 배우
class Actor(models.Model):
    actor_id = models.IntegerField()
    movies = models.ManyToManyField(Movie, related_name='actors')
    name = models.CharField(max_length=100)
    profile_path = models.TextField()
    popularity = models.FloatField()

    def __str__(self) -> str:
        return self.name


# 리뷰
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="reviews")
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_reviews')
    dislike_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='dislike_reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_spoiled = models.BooleanField(default=False)



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_spoiled = models.BooleanField(default=False)


# 내 영화
class Record(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='movies')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='users')
    title = models.CharField(max_length=100)
    poster_path = models.TextField()
    score = models.FloatField(blank=True, null=True)
    wanted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


# 내 장르
class Recommend(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='genre_recommend')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='user_recommend')
    score = models.FloatField(default=0)
    count = models.IntegerField(default=0)
