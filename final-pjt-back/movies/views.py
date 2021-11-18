from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests
from django.shortcuts import get_list_or_404
from decouple import config
from .serializers import MovieListSerializer
from .models import Genre, Movie, Actor, Director, Recommend
from django.contrib.auth import get_user_model
from django.db.models import Max, F
from datetime import datetime
from random import choice

# Create your views here.
# 인기순
@api_view(['GET'])
def read_movies_by_popularity(request):
    movies = Movie.objects.order_by('-popularity')
    return Response(MovieListSerializer(movies, many=True).data)

# 평점순
@api_view(['GET'])
def read_movies_by_score(request):
    # DB의 정보들을 바탕으로 F를 사용하여 DB 내에서 평균평점을 처리하여 annotate를 사용해 새로운 column을 추가한 후 정렬
    movies = Movie.objects.annotate(vote_average=(F('tmdb_vote_sum') + F('updated_vote_sum')) / (F('tmdb_vote_cnt') + F('updated_vote_cnt'))).order_by('-vote_average')
    return Response(MovieListSerializer(movies, many=True).data)
    

# 개봉순
@api_view(['GET'])
def read_movies_by_release(request):
    now = datetime.today().strftime("%Y-%m-%d")
    # release_date 데이터의 정확성에 문제가 있음
    # movies = Movie.objects.order_by('-release_date').filter(release_status="Released")
    movies = Movie.objects.filter(release_date__lte=now).order_by('-release_date')
    return Response(MovieListSerializer(movies, many=True).data)

# 추천 알고리즘
@api_view(['GET'])
def read_movies_by_recommend(request):
    my_genre = Recommend.objects.filter(user__pk=request.user.pk)
    most_prefer_point = 0
    most_prefer_genre = 0
    for genre in my_genre:
        if most_prefer_point < genre.score:
            most_prefer_point = genre.score
            most_prefer_genre = genre.genre
    if most_prefer_genre == 0:
        most_prefer_genre = choice([28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37])
    movies = Movie.objects.filter(genres__tmdb_id=most_prefer_genre)
    while not movies:
        most_prefer_genre = choice([28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37])
        movies = Movie.objects.filter(genres__tmdb_id=most_prefer_genre)
    return Response(MovieListSerializer(movies, many=True).data)


    # 아래는 구버전
    """
    # 사용자가 담아둔 영화가 있다면
    preference = {
        # 장르번호 : [매긴 평점, 매긴 개수]
        28: [0, 0],
        12: [0, 0],
        16: [0, 0],
        35: [0, 0],
        80: [0, 0],
        99: [0, 0],
        18: [0, 0],
        10751: [0, 0],
        14: [0, 0],
        36: [0, 0],
        27: [0, 0],
        10402: [0, 0],
        9648: [0, 0],
        10749: [0, 0],
        878: [0, 0],
        10770: [0, 0],
        53: [0, 0],
        10752: [0, 0],
        37: [0, 0],
    }

    my_genre = Recommend.objects.filter(user__pk=request.user.pk)
    for genre in my_genre:
        preference[genre.genre.tmdb_id][0] += genre.score
        preference[genre.genre.tmdb_id][1] += 1
    most_prefer_genre = most_prefer_point = 0
    for key, value in preference.items():
        if value[1] == 0:
            continue
        if most_prefer_point < value[0]/value[1]:
            most_prefer_point = value[0]/value[1]
            most_prefer_genre = key
    if most_prefer_genre == 0:
        most_prefer_genre = choice([28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37])
    
    movies = Movie.objects.filter(genres__tmdb_id=most_prefer_genre)
    while not movies:
        most_prefer_genre = choice([28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37])
        movies = Movie.objects.filter(genres__tmdb_id=most_prefer_genre)
    return Response(MovieListSerializer(movies, many=True).data)
    """



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
                movie.tmdb_vote_sum = tmdb_data.get('vote_average') * tmdb_data.get('vote_count')
                movie.tmdb_vote_cnt = tmdb_data.get('vote_count')
                # movie.release_status = tmdb_data.get('release_status')
                movie.save()
            else:
                # detail_URL = f'https://api.themoviedb.org/3/movie/{tmdb_movie_id}?api_key={API_KEY}&language=ko-KR'
                # detail_status = requests.get(detail_URL).json().get('status')

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
                    # release_status=detail_status
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
