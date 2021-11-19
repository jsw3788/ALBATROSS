from rest_framework import serializers
from .models import Movie, Record, Comment, Movie, Review, Director, Actor


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = (
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

    class Meta:
        model = Movie
        fields = (
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


class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record
        fields = ('id', 'user', 'movie', 'title', 'poster_path', 'score', 'wanted')


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = (
            'user',
            'movie',
            'like_users',
            'dislike_users',
            'content',
            'is_spoiled',
            'created_at',
            'updated_at',
        )

        
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'user',
            'review',
            'content',
            'created_at',
            'updated_at',
            'is_spoiled'
        )


class DirectorListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Director
        fields = (
            'director_id',
            'name',
            'profile_path',
            'popularity'
        )

class ActorListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Actor
        fields = (
            'actor_id',
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
            'director_id',
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
            'actor_id',
            'movies',
            'name',
            'profile_path',
            'popularity'
        )