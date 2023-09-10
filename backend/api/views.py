from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from sensors.models import (Garage, Manufacturer, Room, Sensor,
                            SensorType, Tag, User)

from .mixins import ListRetrieveViewSet
from .permissions import IsCurrentUserOrAdminOrReadOnly
from .serializers import SensorSerializer, TagSerializer, UserSerializer


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsCurrentUserOrAdminOrReadOnly]

    @action(['get'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(['post'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request})
        if serializer.is_valid(raise_exception=True):
            self.request.user.set_password(serializer.data["new_password"])
            self.request.user.save()
            return Response('Password successfully changed.',
                            status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['post', 'delete'],
    #         detail=True,
    #         permission_classes=[IsAuthenticated])
    # def subscribe(self, request, *args, **kwargs):
    #     author = get_object_or_404(User, id=self.kwargs.get('pk'))
    #     user = self.request.user

    #     if request.method == 'POST':
    #         if user.follower.filter(author=author).exists():
    #             return Response({'errors':
    #                              'You already follow this author.'
    #                              },
    #                             status=status.HTTP_400_BAD_REQUEST)
    #         serializer = FollowSerializer(
    #             data=request.data,
    #             context={'request': request, 'author': author})
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save(author=author, user=user)
    #             return Response(
    #                 serializer.data, status=status.HTTP_201_CREATED)
    #         return Response({'errors': 'Not found.'},
    #                         status=status.HTTP_404_NOT_FOUND)

    #     if request.method == 'DELETE':
    #         if user.follower.filter(author=author).delete()[0]:
    #             return Response(f'Unfollowed {author.get_username()}',
    #                             status=status.HTTP_204_NO_CONTENT)
    #         return Response({'errors': 'Object not found.'},
    #                         status=status.HTTP_404_NOT_FOUND)

    # @action(detail=False,
    #         methods=['get'],
    #         permission_classes=[IsAuthenticated])
    # def subscriptions(self, request):
    #     follows = self.request.user.follower.all()
    #     pages = self.paginate_queryset(follows)
    #     serializer = FollowSerializer(pages,
    #                                   many=True,
    #                                   context={'request': request})
    #     return self.get_paginated_response(serializer.data)
