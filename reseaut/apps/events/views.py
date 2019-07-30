from django.shortcuts import get_object_or_404

from rest_framework import mixins,status,viewsets

from rest_framework.exceptions import NotFound

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Event
from .serializers import EventSerializer

# Create your views here.

class EventViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    lookup_field = 'slug'
    queryset = Event.objects.select_related('author','author__user')
    permissions_classes = (IsAuthenticatedOrReadOnly,)
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