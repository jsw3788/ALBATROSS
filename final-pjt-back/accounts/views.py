from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import UserSerializer, UserProfileUpdateSerializer



from django.contrib.auth import get_user_model


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    if get_user_model().objects.filter(username=request.data.get('username')).exists():
        return Response({'error':'이미 존재하는 계정 입니다.'},status=status.HTTP_400_BAD_REQUEST)

    if password != password_confirmation:
        return Response({'error' : '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()

        user.set_password(request.data.get('password'))
        user.save()
        print(user.profile_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def profile(request, username):
    # 회원 정보 조회 
    def profile_detail():
        person=get_object_or_404(get_user_model(), username=username)
        user=request.user
        
        if person != user:
            if user.followings.filter(pk=person.pk).exists():
                following = True
            else:
                following = False
        # 자기 자신은 팔로우 안함
        else:
            following = False
        
        context = {
            'username' : username,
            'profile_image': str(person.profile_image),
            'following': following,
            'movieCnt' : person.movies.count(),
            'followingCnt': person.followings.count(),
            'followerCnt': person.followers.count(),
        }
        return JsonResponse(context)

    # 회원 정보 수정 (프로필 이미지)
    def update_profile(request):
        username= request.data.get('username')
        profile_image=request.data.get('profileImg')
        password=request.data.get('password')
        passwordConfirm=request.data.get('passwordConfirmation')
        if password!=passwordConfirm:
            return Response({'error' : '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.username != request.data.get('username') and get_user_model().objects.filter(username=request.data.get('username')).exists():
            return Response({'error':'이미 존재하는 사용자 이름 입니다.'},status=status.HTTP_400_BAD_REQUEST)
        
        # 프로필 이미지 삭제
        if not profile_image:
            user=request.user
            user.profile_image.delete()
            user.username=username
            user.profile_image='default.png'
            user.save()
            profile_image = user.profile_image
        
        context={
            'following': False,
            'username': username,
            'profile_image': profile_image,
            'password': password,
        }
        serializer = UserProfileUpdateSerializer(request.user, data=context)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(profile_image=profile_image)
            
            user.set_password(password)
            user.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # 회원 탈퇴
    def delete_profile():
        user_pk = request.user.pk
        request.user.delete()
        return Response({'delete': f'{user_pk}번 회원이 탈퇴했습니다.'}, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return profile_detail()
    elif request.method == 'PUT':
        return update_profile(request)
    elif request.method == 'DELETE':
        return delete_profile()


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def follow(request, username):
    me = request.user
    you = get_object_or_404(get_user_model(), username=username)

    if me!=you:
        if me.followings.filter(pk=you.pk).exists():
            following = False
            me.followings.remove(you)
        else:
            following = True
            me.followings.add(you)
    else:
        return Response({'error':'자기자신을 팔로우 할 수 업습니다.'},status=status.HTTP_403_FORBIDDEN)
    context = {
        'following': following,
        'followingCnt' : you.followings.count(),
        'followerCnt' : you.followers.count()
    }
    return JsonResponse(context)