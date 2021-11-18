from rest_framework import serializers, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import UserSerializer, UserProfileSerializer

# from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth import get_user_model


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    if password != password_confirmation:
        return Response({'error' : '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()

        user.set_password(request.data.get('password'))
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):

    # 회원 정보 조회
    def profile_detail():
        serializer = UserProfileSerializer(request.data)
        return Response(serializer.data)

    # 회원 정보 수정 (프로필 이미지)
    def update_profile():
        profile_image = request.data.get('profile_image')
        if request.user.username != request.data.get('username') and get_user_model().objects.filter(username=request.data.get('username')).exists():
            return Response({'error':'이미 존재하는 사용자 이름 입니다.'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(profile_image=profile_image)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # 회원 탈퇴
    def delete_profile():
        user_pk = request.user.pk
        request.user.delete()
        return Response({'delete': f'{user_pk}번 회원이 탈퇴했습니다.'}, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return profile_detail()
    elif request.method == 'PUT':
        return update_profile()
    elif request.method == 'DELETE':
        return delete_profile()