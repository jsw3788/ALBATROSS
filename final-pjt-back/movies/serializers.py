from rest_framework import serializers
from .models import Movie, Record, Comment, Movie, Review


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
