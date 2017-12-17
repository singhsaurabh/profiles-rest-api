from django.shortcuts import render

#viewsets import
from rest_framework import viewsets
#APIView import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated


from . import serializers
from . import models
from . import permissions

# Create your views here.

#class for APIView
class HelloApiView(APIView):
    """Test API view."""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features."""
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'It is similar to a traditional Django View',
            'Gives you the most contol over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name."""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handling update on object."""

        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""

        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """Delete a Object."""

        return Response({'method': 'delete'})

#class for viewsets
class HelloViewSet(viewsets.ViewSet):
    """ Test API ViewSet."""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """List the API viewset. Return the hello message."""

        a_viewset = [
            'Uses actions (list, ctreate, retrieve, update, partial_update)',
            'Automatically maps to URLs using routers',
            'Provides more funtionality with less code.'
        ]

        return Response({'message': 'Hello!', 'a_viewset':a_viewset})

    def create(self, request):
        """Create a new Hello Message."""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Getting the object by its ID."""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Updating an object."""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Updating part of the Object."""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Removing an Object."""

        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Creating and Updating user profile."""

    serializer_class = serializers.UserProfileSerialzer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
    """Check emails and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Creating, Reading and Updating profile feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    #permission_classes = (permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""

        serializer.save(user_profile=self.request.user)
