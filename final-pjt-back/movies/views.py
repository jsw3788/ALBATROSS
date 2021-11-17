from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests
from django.shortcuts import get_list_or_404
from decouple import config
from .models import Genre, Movie, Actor, Director

# Create your views here.


@api_view(['POST'])
def get_genre(request):
    API_KEY = config('API_KEY')
    URL = f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=ko-KR'
    request = requests.get(URL).json()
    for tmdb_data in request.get('genres'):
        if Genre.objects.filter(tmdb_id=tmdb_data.get('id')).exists():
            continue
        Genre.objects.create(
            tmdb_id=tmdb_data.get('id'),
            name=tmdb_data.get('name'),
        )
    return Response({'database': '성공'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def get_movies(request):
    API_KEY = config('API_KEY')
    for page in range(1, 2):
        URL = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=ko-KR&page={page}&region=KR'
        request = requests.get(URL).json()
        # print(request)
        for tmdb_data in request.get('results'):
            tmdb_movie_id = tmdb_data.get('id')
            if Movie.objects.filter(tmdb_id=tmdb_movie_id).exists():
                movie = Movie.objects.get(tmdb_id=tmdb_movie_id)
                movie.popularity = tmdb_data.get('popularity')
                movie.tmdb_vote_sum = tmdb_data.get(
                    'vote_average') * tmdb_data.get('vote_count')
                movie.tmdb_vote_cnt = tmdb_data.get('vote_count')
                movie.save()
            else:
                detail_URL = f'https://api.themoviedb.org/3/movie/{tmdb_movie_id}?api_key={API_KEY}&language=ko-KR'
                detail_status = requests.get(detail_URL).json().get('status')

                movie = Movie.objects.create(
                    tmdb_id=tmdb_movie_id,
                    title=tmdb_data.get('title'),
                    release_date=tmdb_data.get('release_date'),
                    popularity=tmdb_data.get('popularity'),
                    tmdb_vote_sum=tmdb_data.get(
                        'vote_average') * tmdb_data.get('vote_count'),
                    tmdb_vote_cnt=tmdb_data.get('vote_count'),
                    updated_vote_sum=0,
                    updated_vote_cnt=0,
                    overview=tmdb_data.get('overview'),
                    poster_path=f'https://image.tmdb.org/t/p/w500{tmdb_data.get("poster_path")}',
                    backdrop_path=f'https://image.tmdb.org/t/p/w500{tmdb_data.get("backdrop_path")}',
                    release_status=detail_status
                )
                for genre_id in tmdb_data.get('genre_ids'):
                    genre = Genre.objects.get(tmdb_id=genre_id)
                    movie.genres.add(genre)
    return Response({'database': '성공'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def get_credits(request):
    API_KEY = config('API_KEY')
    movie_data = get_list_or_404(Movie)
    for movie in movie_data:
        URL = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}/credits?api_key={API_KEY}&language=ko-KR'
        actors = requests.get(URL).json().get('cast')
        for actor in actors:
            tmdb_id = actor.get("id")
            if not actor.get("profile_path"):
                continue
            if Actor.objects.filter(actor_id=tmdb_id).exists():
                continue
            ppl_URL = f'https://api.themoviedb.org/3/person/{tmdb_id}?api_key={API_KEY}&language=ko-KR'
            actor_popularity = requests.get(ppl_URL).json().get('popularity')
            new_actor = Actor.objects.create(
                actor_id=tmdb_id,
                name=actor.get("name"),
                profile_path=f'https://image.tmdb.org/t/p/w500{actor.get("profile_path")}',
                popularity=actor_popularity,
            )
            new_actor.movies.add(movie)

        crews = requests.get(URL).json().get('crew')
        for crew in crews:
            tmdb_id = crew.get("id")
            if crew.get("job") != "Director" or not crew.get("profile_path"):
                continue
            if Director.objects.filter(director_id=tmdb_id).exists():
                continue
            ppl_URL = f'https://api.themoviedb.org/3/person/{tmdb_id}?api_key={API_KEY}&language=ko-KR'
            director_popularity = requests.get(
                ppl_URL).json().get('popularity')
            new_director = Director.objects.create(
                director_id=tmdb_id,
                name=crew.get("name"),
                profile_path=f'https://image.tmdb.org/t/p/w500{crew.get("profile_path")}',
                popularity=director_popularity,
            )
            new_director.movies.add(movie)
    return Response({'database': '성공!'}, status=status.HTTP_201_CREATED)
