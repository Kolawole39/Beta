from django.shortcuts import get_object_or_404

from rest_framework import mixins,status,viewsets,views

from rest_framework.exceptions import NotFound

from rest_framework.response import Response

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated

from .models import Event,Comment
from .serializers import EventSerializer,CommentSerializer
from .renderers import EventJSONRenderer,CommentJSONRenderer
# Create your views here.

class EventViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    lookup_field = 'slug'
    queryset = Event.objects.select_related('author','author__user')
    permissions_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (EventJSONRenderer,)
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        
        serializer_context = {'author':request.user.profile}
        serializer_data = request.data.get('event',{})

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def retrieve(self, request, slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Event.DoestNotExist:
            raise NotFound('An event with this slug does not exist.')
        
        serializer = self.serializer_class(serializer_instance)

        return Response(serializer.data,status=status.HTTP_200_OK)

    def update(self,request,slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Event.DoesNotExist:
            raise NotFound('An event with this slug does not exist.')
        
        serializer_data = request.data.get('event',{})

        serializer = self.serializer_class(
            serializer_instance,data=serializer_data,partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_200_OK)

class CommentListCreateAPIView(generics.ListCreateAPIView):

    lookup_field = 'event__slug'
    lookup_url_kwarg = 'event_slug'

    queryset = Comment.objects.select_related('author','author__user','event','event__author','event__author__user')
    permission_classes = (IsAuthenticated,)
    renderers_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer

    def create(self, request,event_slug=None):
        data = request.data.get('comment',{})

        context = {'author':request.user.profile}

        try:
            context['event'] = Event.objects.get(slug=event_slug)
        except Event.DoesNotExist:
            raise NotFound('An Event with this slug does not exist.')
        serializer = self.serializer_class(data=data,context=context)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ComementDestroyAPIView(generics.DestroyAPIView):
    lookup_url_kwarg = 'comment_id'
    permissions_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()

    def destroy(self, request, event_slug=None,comment_id=None):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')
        comment.delete()

        return Response(None,status=status.HTTP_204_NO_CONTENT)

class EventFavoriteAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (EventJSONRenderer,)
    serializer_class = EventSerializer

    def delete(self,request,event_slug=None):
        profile = self.request.user.profile

        try:
            event = Event.objects.get(slug=event_slug)
        except Event.DoesNotExist:
            raise NotFound('An event with this slug does not exist.')
        
        profile.unfavorite(event)

        serializer = self.serializer_class(event,context={
            'request':request
        })

        return Response(serializer.data,status=status.HTTP_200_OK)


    def post(self,request,event_slug=None):
        profile = self.request.user.profile

        try:
            event = Event.objects.get(slug=event_slug)
        except:
            raise NotFound('An article with this slug was not found.')
        
        profile.favorite(event)

        serializer = self.serializer_class(event,context={
            'request':request
        })

        return Response(serializer.data,status=status.HTTP_201_CREATED)
        