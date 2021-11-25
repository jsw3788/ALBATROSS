# from django.http.response import JsonResponse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from rest_framework.response import Response
import requests
from django.shortcuts import get_list_or_404, get_object_or_404
from decouple import config
from .serializers import AllMovieListSerializer, ActorListSerializer, ActorSerializer, CommentSerializer, DirectorListSerializer, DirectorSerializer, MovieListSerializer, ReviewListSerializer, ReviewSerializer, MovieSerializer
from .models import Genre, Movie, Actor, Director, Recommend, Review, Comment, Record
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model
from django.db.models import Count, F, Prefetch
from datetime import datetime
from random import choice
from django.core.paginator import Paginator



# 영화 상세 조회
@api_view(['GET'])
@permission_classes([AllowAny])
def read_movie_detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    return Response(MovieSerializer(movie).data)



# 영화리스트 데이터 조회

# 전체
@api_view(['GET'])
@permission_classes([AllowAny])
def read_all_movies(request):
    # 구버전
    # movies = Movie.objects.all()
    
    # 최적화
    movies = Movie.objects.prefetch_related('genres').prefetch_related('actors').prefetch_related('directors')
    return Response(AllMovieListSerializer(movies, many=True).data)



# 인기순
@api_view(['GET'])
@permission_classes([AllowAny])
def read_movies_by_popularity(request):
    movies = Movie.objects.order_by('-popularity')[:30]
    return Response(MovieListSerializer(movies, many=True).data)


# 평점순
@api_view(['GET'])
@permission_classes([AllowAny])
def read_movies_by_score(request):
    # 최적화
    # DB의 정보들을 바탕으로 F를 사용하여 DB 내에서 평균평점을 처리하여 annotate를 사용해 새로운 column을 추가한 후 정렬
    movies = Movie.objects.annotate(vote_average=(F('tmdb_vote_sum') + F('updated_vote_sum')) / (
        F('tmdb_vote_cnt') + F('updated_vote_cnt'))).order_by('-vote_average')[:30]
    return Response(MovieListSerializer(movies, many=True).data)


# 개봉순
@api_view(['GET'])
@permission_classes([AllowAny])
def read_movies_by_release(request):
    now = datetime.today().strftime("%Y-%m-%d")
    # release_date 데이터의 정확성에 문제가 있음
    movies = Movie.objects.filter(
        release_date__lte=now).order_by('-release_date')[:30]
    return Response(MovieListSerializer(movies, many=True).data)



# 추천 알고리즘
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def read_movies_by_recommend(request):
    # 구버전
    # my_genre = Recommend.objects.filter(user__pk=request.user.pk)

    # 최적화
    my_genre = Recommend.objects.select_related('genre').select_related('user').filter(user__pk=request.user.pk)
    most_prefer_point = 0
    most_prefer_genre = 0
    for genre in my_genre:
        if most_prefer_point < genre.score:
            most_prefer_point = genre.score
            most_prefer_genre = Genre.objects.get(pk=genre.genre_id).tmdb_id
    
    # 가장 좋아하는 장르를 못찾으면 랜덤 
    if most_prefer_genre == 0:
        most_prefer_genre = choice(
            [28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37])
    # 최적화
    movies = Movie.objects.prefetch_related('genres').filter(genres__tmdb_id=most_prefer_genre)
    
    # 해당하는 장르의 영화가 하나도 없으면 다시 뽑기
    while not movies:
        most_prefer_genre = choice(
            [28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37])
        # 최적화
        movies = Movie.objects.prefetch_related('genres').filter(genres__tmdb_id=most_prefer_genre)
    return Response(MovieListSerializer(movies[:30], many=True).data)


# 영화인 데이터 조회

# 인기순 상위 감독 리스트
@api_view(['GET'])
@permission_classes([AllowAny])
def director_list(request):
    directors = Director.objects.order_by('-popularity')[:18]
    return Response(DirectorListSerializer(directors, many=True).data)


# 인기순 상위 배우 리스트
@api_view(['GET'])
@permission_classes([AllowAny])
def actor_list(request):
    actors = Actor.objects.order_by('-popularity')[:18]
    return Response(ActorListSerializer(actors, many=True).data)


# 감독 상세
@api_view(['GET'])
@permission_classes([AllowAny])
def director_detail(request, director_pk):
    director = get_object_or_404(Director, id=director_pk)
    return Response(DirectorSerializer(director).data)


# 배우 상세
@api_view(['GET'])
@permission_classes([AllowAny])
def actor_detail(request, actor_pk):
    actor = get_object_or_404(Actor, id=actor_pk)
    return Response(ActorSerializer(actor).data)


# 영화의 평점을 매기면 scroe를 작성하고, wanted를 false로 뒤집기
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def read_update_score(request, movie_pk):
    # 평점을 매기면, 사용자의 Recommend 테이블과 Record 테이블을 갱신해야함
    # POST 요청은 사용자가 평점을 매긴적이 없는 경우
    # PUT 요청은 사용자가 매긴 평점을 수정할 경우
    # DELETE 요청은 사용자가 평점을 0으로 바꿀 경우
    if request.method == "GET":
        if Record.objects.filter(user=request.user.pk, movie=movie_pk).exists():
            my_movie = Record.objects.get(user=request.user.pk, movie=movie_pk)
            score = my_movie.score
        else:
            score = 0
        context = {
            'score': score,
        }
        # return JsonResponse(context)
        return Response(context,status=status.HTTP_200_OK)
    else:
        # 선택한 영화
        movie = get_object_or_404(Movie, pk=movie_pk)
        
        after_score = request.data.get('score')
        if request.method == "PUT":
            # 원래 평점이 있잔아
            my_movie = Record.objects.get(user=request.user.pk, movie=movie.pk)
            before_score = my_movie.score
            movie.updated_vote_sum += (after_score - before_score)
            movie.save()
            my_movie.score = after_score
            my_movie.save()
            # 이거는 내가 담아놓은 모든 장르 가져오는 필터
            my_recommends = Recommend.objects.filter(user=request.user.pk)
            # 이거는 고른 영화의 모든 장르 가져오는 것
            movie_genres = movie.genres.all()
            # movie_genres = Movie.objects.prefetch_related('genres')
            # movie_genres = Genre.objects.prefetch_related('movies')
            for movie_genre in movie_genres:
                for recommend in my_recommends:
                    if movie_genre.pk == recommend.genre_id:  # 이거 값들은 나중에 찍어보면서 확인
                        recommend.score += (after_score - before_score)
                        recommend.save()
            context={
                'wanted': my_movie.wanted
            }
            # return JsonResponse(context)
            return Response(context)

        elif request.method == "POST":
            movie.updated_vote_cnt += 1
            movie.updated_vote_sum += after_score
            movie.save()
            # 보고싶어요가 체크되어 있는 상태라면
            if Record.objects.filter(user=request.user.pk, movie=movie_pk).exists():
                my_movie = Record.objects.get(
                    user=request.user.pk, movie=movie.pk)
                my_movie.wanted = False
                my_movie.score = after_score
                my_movie.save()
                for genre in movie.genres.all():
                    is_recommend = Recommend.objects.filter(genre=genre).exists()
                    if is_recommend:
                        my_recommends = Recommend.objects.filter(user=request.user.pk)
                        for recommend in my_recommends:
                            if genre.pk == recommend.genre_id:
                                recommend.score += after_score
                                recommend.count += 1
                                recommend.save()
                    else:
                        Recommend.objects.create(
                            user=request.user,
                            genre=genre,
                            score = after_score,
                            count = 1
                        )
            else:  # 보고싶어요 체크 안된 상태라면
                my_movie = Record.objects.create(
                    title=movie.title,
                    poster_path=movie.poster_path,
                    score=after_score,
                    wanted=False,
                    user=request.user,
                    movie=movie
                )
                # 영화의 장르를 돌면서, Recommend에 장르가 있는지 확인하자
                for genre in movie.genres.all():
                    is_recommend = Recommend.objects.filter(genre=genre).exists()
                    # 이미 좋아하는 장르에 있는 데이터면, 수정해줘야하고
                    if is_recommend:
                        # 새로 만들고나면 
                        my_recommends = Recommend.objects.filter(user=request.user.pk)
                        for recommend in my_recommends:
                            if genre.pk == recommend.genre_id:
                                recommend.score += after_score
                                recommend.count += 1
                                recommend.save()
                    # 아니면 새로 만들어야함
                    else:
                        Recommend.objects.create(
                            user=request.user,
                            genre=genre,
                            score = after_score,
                            count = 1
                        )
            context={
                'wanted': my_movie.wanted
            }
            # return JsonResponse(context)
            return Response(context)


        elif request.method == "DELETE":  # 0점을 줬어! 삭제할거야!
            movie.updated_vote_sum -= request.data.get('delScore')
            movie.updated_vote_cnt -= 1
            movie.save()
            my_movie = Record.objects.get(user=request.user.pk, movie=movie.pk)
            before_score = my_movie.score
            my_recommends = Recommend.objects.filter(user=request.user.pk)
            movie_genres = movie.genres.all()
            for movie_genre in movie_genres:
                for recommend in my_recommends:
                    if movie_genre.pk == recommend.genre_id:
                        recommend.score -= before_score
                        recommend.count -= 1
                        if recommend.count:
                            recommend.save()
                        else:
                            recommend.delete()
            my_movie.delete()

            context={
                'deleted': '평점데이터가 삭제되었습니다.'
            }
            # return JsonResponse(context)
            return Response(context)



# 영화를 보고싶어하면 wanted를 true로 Record에 넣기
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def read_update_wanted(request, movie_pk):
    # 선택한 영화
    if request.method == "GET":
        if Record.objects.filter(user=request.user.pk, movie=movie_pk).exists():
            my_movie = Record.objects.get(user=request.user.pk, movie=movie_pk)
            wanted = my_movie.wanted
        else:
            wanted = False
        context = {
            'wanted': wanted,
        }
        # return JsonResponse(context)
        return Response(context)


    elif request.method == "POST":
        movie = Movie.objects.get(pk=movie_pk)
        # 그 영화가 Record에 이미 담겨있을까? 그럴수도 있고~ 아닐수도 있고
        if not Record.objects.filter(user=request.user.pk, movie=movie_pk).exists():
            my_movie = Record.objects.create(
                title=movie.title,
                poster_path=movie.poster_path,
                wanted=True,
                user=request.user,
                movie=movie
            )
            wanted = True
        else:
            my_movie = Record.objects.get(user=request.user.pk, movie=movie_pk)
            if my_movie.wanted:  # 보고싶어요를 취소하고있음
                my_movie.delete()
                wanted = False
            else:
                return Response({'error': '이미 본 영화입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        context = {
            'wanted': wanted,
        }
        # return JsonResponse(context)
        return Response(context)


# 유저의 최신순 리뷰
@api_view(['GET'])
@permission_classes([AllowAny])
def read_recent_reviews_by_user(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    recent_reviews = person.reviews.order_by('-updated_at')[:3]
    
    return Response(ReviewSerializer(recent_reviews, many=True).data)


# 유저의 인기순 리뷰
@api_view(['GET'])
@permission_classes([AllowAny])
def read_popular_reviews_by_user(request, username):
    # person=get_object_or_404(get_user_model(), username=username)
    person = get_user_model().objects.get(username=username)
    if person:
        reviews = []
        # my_reviews = person.reviews.all()
        my_reviews = Review.objects.annotate(like_count=Count('like_users')).select_related('user').prefetch_related('like_users').prefetch_related('dislike_users').filter(user=person)
        for review in my_reviews:
            # reviews.append((review.like_users.count(), review))
            reviews.append((review.like_count, review))
        # 좋아요 순 정렬
        sorted_reviews = sorted(reviews, key=lambda x: x[0])[:3]
        popular_reviews = []
        for cnt, review in sorted_reviews:
            popular_reviews.append(review)
        return Response(ReviewListSerializer(popular_reviews, many=True).data)
    else:
        return Response({'error': '본 영화가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


# 유저가 최근 평점을 매긴 영화
@api_view(['GET'])
@permission_classes([AllowAny])
def read_recent_movies_by_user(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    # 최적화
    records = Record.objects.select_related('user').filter(user=person).prefetch_related('movie').order_by('-pk')
    
    recent_movies = []
    for record in records:
        if 4 <= len(recent_movies):
            break
        if record.score:
            recent_movies.append(record.movie)

    

    return Response(MovieListSerializer(recent_movies, many=True).data)

# 유저의 가장 좋아하는(최고 평점) 영화
@api_view(['GET'])
@permission_classes([AllowAny])
def read_favorite_movies_by_user(request, username):
    
    person = get_object_or_404(get_user_model(), username=username)
    # 구버전
    # favorite_movies = person.movies.order_by('-score').distinct()[:4]
    
    # 최적화
    favorite_movies = Record.objects.select_related('user').prefetch_related('movie').filter(user=person).order_by('-score').distinct()[:4]
    ret = []
    for favorite_movie in favorite_movies:
        ret.append(favorite_movie.movie)
    return Response(MovieListSerializer(ret, many=True).data)


# 리뷰 전체 조회, 생성
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def review_list(request, movie_pk):
    if request.method == 'GET':
        # 구버전
        # reviews = Review.objects.filter(movie__pk=movie_pk)
        
        # 최적화
        reviews = Review.objects.select_related('user').prefetch_related('like_users').prefetch_related('dislike_users').filter(movie__pk=movie_pk)
        # paginator
        paginator = Paginator(reviews, 5)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        serializer = ReviewListSerializer(page_obj, many=True)
        data = serializer.data
        data.append({'last_page': paginator.num_pages})
        return Response(data)
        # serializer = ReviewListSerializer(reviews, many=True)

    elif request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 리뷰 상세 조회, 삭제, 수정
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def review_detail(request, review_pk):
    # 구버전
    # review = get_object_or_404(Review, pk=review_pk)

    # 최적화
    review = Review.objects.annotate(like_count=Count('like_users'), dislike_count=Count('dislike_users')).select_related('user').get(pk=review_pk)
    
    # 리뷰에 대한 좋아요, 싫어요 정보 조회
    if request.method == 'GET':
        if review.like_users.filter(pk=request.user.pk).exists():
            isLiked = True
        else:
            isLiked = False
        
        if review.dislike_users.filter(pk=request.user.pk).exists():
            isDisiked = True
        else:
            isDisiked = False

        context={
            'isLiked': isLiked,
            'isDisliked': isDisiked,
            # 'likeCnt' : review.like_users.count(),
            'likeCnt' : review.like_count,
            # 'dislikeCnt' : review.dislike_users.count(),
            'dislikeCnt' : review.dislike_count,
            'commentCnt' : review.comments.count(),
        }
        # return JsonResponse(context)
        return Response(context)


    elif request.user == review.user:
        # 리뷰 수정
        if request.method == 'PUT':
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

        # 리뷰 제거
        elif request.method == 'DELETE':
            review.delete()
            return Response({'delete': f'{review_pk}번 리뷰가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'Unauthorized': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


# 리뷰 좋아요
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def likes(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    # 싫어요를 눌렀으면 좋아요를 누를 수 없음
    if review.dislike_users.filter(pk=request.user.pk).exists():
        return Response({'error': '이미 싫어요를 눌렀습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    if review.like_users.filter(pk=request.user.pk).exists():
        isLiked = False
        review.like_users.remove(request.user)
    else:
        isLiked = True
        review.like_users.add(request.user)

    context = {
        'isLiked': isLiked,
        'likeCnt': review.like_users.count()
    }
    # return JsonResponse(context)
    return Response(context)


# 리뷰 싫어요
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def dislikes(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    # 좋아요를 눌렀으면 싫어요를 누를 수 없음
    if review.like_users.filter(pk=request.user.pk).exists():
        return Response({'error': '이미 좋아요를 눌렀습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    if review.dislike_users.filter(pk=request.user.pk).exists():
        isDisliked = False
        review.dislike_users.remove(request.user)
    else:
        isDisliked = True
        review.dislike_users.add(request.user)

    context = {
        'isDisliked': isDisliked,
        'dislikeCnt': review.dislike_users.count()
    }
    # return JsonResponse(context)
    return Response(context)



# 전체 댓글 조회, 생성
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def comment_list(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':

        # 구버전
        # comments = Comment.objects.filter(review__pk=review_pk)

        # 최적화
        comments = Comment.objects.select_related('user').filter(review__pk=review_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 댓글 삭제, 수정
@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:

        if request.method == 'PUT':
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

        # 댓글 제거
        elif request.method == 'DELETE':
            comment.delete()
            return Response({'delete': f'{comment_pk}번 댓글이 삭제되었습니다.'})

    return Response({'Unauthorized': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


# db 장르 데이터 불러오기
@api_view(['POST'])
@permission_classes([AllowAny])
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
    # if request.data.get('username') == 'admin':
    # return Response({'Unauthorized':'권한이 없습니다.'},status=status.HTTP_401_UNAUTHORIZED)


# db 영화 데이터 불러오기
@api_view(['POST'])
@permission_classes([AllowAny])
def get_movies(request):
    API_KEY = config('API_KEY')
    for page in range(4, 7):
        URL = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=ko-KR&page={page}&region=KR'
        request = requests.get(URL).json()
        for tmdb_data in request.get('results'):
            tmdb_movie_id = tmdb_data.get('id')
            if Movie.objects.filter(tmdb_id=tmdb_movie_id).exists():
                movie = Movie.objects.get(tmdb_id=tmdb_movie_id)
                movie.popularity = tmdb_data.get('popularity')
                movie.tmdb_vote_sum = tmdb_data.get(
                    'vote_average') * tmdb_data.get('vote_count')
                movie.tmdb_vote_cnt = tmdb_data.get('vote_count')
                # movie.release_status = tmdb_data.get('release_status')
                movie.save()
            else:
            
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
                    backdrop_path=f'https://image.tmdb.org/t/p/original{tmdb_data.get("backdrop_path")}',
                    # release_status=detail_status
                )
                for genre_id in tmdb_data.get('genre_ids'):
                    genre = Genre.objects.get(tmdb_id=genre_id)
                    movie.genres.add(genre)
    return Response({'database': '성공'}, status=status.HTTP_201_CREATED)
    # if request.data.get('username') == 'admin':
    # return Response({'Unauthorized':'권한이 없습니다.'},status=status.HTTP_401_UNAUTHORIZED)


# db 영화인 데이터 불러오기

# db 영화인 데이터 불러오기

@api_view(['POST'])
@permission_classes([AllowAny])
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
                actor = get_object_or_404(Actor, actor_id=tmdb_id)
                actor.movies.add(movie)
                continue
            # ppl_URL = f'https://api.themoviedb.org/3/person/{tmdb_id}?api_key={API_KEY}&language=ko-KR'
            # actor_popularity = requests.get(ppl_URL).json().get('popularity')
            new_actor = Actor.objects.create(
                actor_id=tmdb_id,
                name=actor.get("name"),
                profile_path=f'https://image.tmdb.org/t/p/w500{actor.get("profile_path")}',
                popularity=actor.get("popularity"),
            )
            new_actor.movies.add(movie)

        crews = requests.get(URL).json().get('crew')
        for crew in crews:
            tmdb_id = crew.get("id")
            if crew.get("job") != "Director" or not crew.get("profile_path"):
                continue
            if Director.objects.filter(director_id=tmdb_id).exists():
                director = get_object_or_404(Director, director_id=tmdb_id)
                director.movies.add(movie)
                continue
            # ppl_URL = f'https://api.themoviedb.org/3/person/{tmdb_id}?api_key={API_KEY}&language=ko-KR'
            # director_popularity = requests.get(ppl_URL).json().get('popularity')
            new_director = Director.objects.create(
                director_id=tmdb_id,
                name=crew.get("name"),
                profile_path=f'https://image.tmdb.org/t/p/w500{crew.get("profile_path")}',
                popularity=director.get("popularity"),
            )
            new_director.movies.add(movie)
    return Response({'database': '성공!'}, status=status.HTTP_201_CREATED)
    # if request.data.get('username') == 'admin':
    # return Response({'Unauthorized':'권한이 없습니다.'},status=status.HTTP_401_UNAUTHORIZED)
