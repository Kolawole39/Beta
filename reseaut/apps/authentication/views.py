from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer

from .backends import JWTAuthentication

from rest_framework.generics import RetrieveUpdateAPIView

from .renderers import UserJSONRenderer

# Create your views here.
from .serializers import RegistrationSerializer,LoginSerializer,UserSerializer

class RegistrationAPIView(APIView):
    #Allow any user to hit this endpoint
    permissions_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self,request):
        user = request.data.get('user',{})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    serializer_class = LoginSerializer

    def post(self,request):
        user = request.data.get('user',{})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    authentication_classes = (JWTAuthentication,)

    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        user = request.data.get('user',{})

        serializer = self.serializer_class(
            request.user, data=serializer.data,partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)