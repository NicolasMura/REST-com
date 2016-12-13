from snippets.models import Snippet
from snippets.serializers import (
    SnippetSerializer,
    UserSerializer,
    SignUpSerializer
)
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from snippets.permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from django.views.generic.list import ListView

# Imports for endpoint for the root of our ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

# Imports for creating an endpoint for the highlighted snippets
from rest_framework import renderers

# Imports for oauth2_provider
from oauth2_provider.ext.rest_framework import OAuth2Authentication

# Test
from rest_framework.parsers import MultiPartParser, FileUploadParser, JSONParser, FormParser


# Endpoint for the root of our ListAPIView
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # authentication_classes = [OAuth2Authentication]
    # permission_classes = [TokenHasScope]
    # parser_classes = (MultiPartParser, FileUploadParser, JSONParser, FormParser)
    parser_classes = (MultiPartParser, JSONParser)

    # # Overriding .perform_create() method to associate Snippets with Users
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # permission_classes = (
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsOwnerOrReadOnly,
    # )


# Creating an endpoint for the highlighted snippets
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# # Refactoring SnippetList, SnippetDetail & SnippetHighlight
# class SnippetViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.

#     Additionally we also provide an extra `highlight` action.
#     """
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly,)
#     authentication_classes = [OAuth2Authentication]

#     @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
#     def highlight(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)

#     def pre_save(self, obj):
#         obj.owner = self.request.user


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# # Refactoring UserList & UserDetail
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# Test oauth
class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)


class SnippetListView(ListView):
    model = Snippet
    template_name = 'snippets/page.html'
