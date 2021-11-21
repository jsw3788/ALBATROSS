from rest_framework import serializers
from .models import Genre, Movie, Record, Comment, Movie, Review, Director, Actor
from accounts.serializers import UserProfileUpdateSerializer


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = (
            'id',
            'tmdb_id',
            'title',
            'release_date',
            'popularity',
            'tmdb_vote_sum',
            'tmdb_vote_cnt',
            'updated_vote_sum',
            'updated_vote_cnt',
            'poster_path',
        )


class MovieSerializer(serializers.ModelSerializer):
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ('id', 'name')

    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'genres',
            'tmdb_id',
            'title',
            'release_date',
            'popularity',
            'tmdb_vote_sum',
            'tmdb_vote_cnt',
            'updated_vote_sum',
            'updated_vote_cnt',
            'overview',
            'poster_path',
            'backdrop_path',
        )


class ReviewListSerializer(serializers.ModelSerializer):

    user = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'user',
            'movie',
            'like_users',
            'dislike_users',
            'content',
            'is_spoiled',
            'created_at',
            'updated_at',
        )


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = (
            'id',
            'user',
            'movie',
            'content',
            'is_spoiled',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('movie', 'user')


class CommentSerializer(serializers.ModelSerializer):

    user = UserProfileUpdateSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'review',
            'content',
            'created_at',
            'updated_at',
            'is_spoiled'
        )
        read_only_fields = ('user', 'review')


class DirectorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = (
            'id',
            'name',
            'profile_path',
            'popularity'
        )


class ActorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = (
            'id',
            'name',
            'profile_path',
            'popularity'
        )


# nested serializer로 변경해야함 : movies
class DirectorSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = (
                'title',
                'poster_path',
            )

    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Director
        fields = (
            'id',
            'movies',
            'name',
            'profile_path',
            'popularity'
        )


class ActorSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = (
                'title',
                'poster_path',
            )

    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = (
            'id',
            'movies',
            'name',
            'profile_path',
            'popularity'
        )
