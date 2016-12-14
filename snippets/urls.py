# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.conf.urls import url, include
# from snippets import views
# from rest_framework.routers import DefaultRouter

# # Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
# router.register(r'users', views.UserViewSet)

# # The API URLs are now determined automatically by the router.
# # Additionally, we include the login URLs for the browseable API.
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(
#         r'^api-auth/',
#         include('rest_framework.urls', namespace='rest_framework')),
#     url(
#         r'^snippets2/$',
#         views.SnippetListView.as_view(),
#         name="snippet-list-2"
#     ),
# ]


from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
# from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^snippets/$',
        views.SnippetList.as_view(),
        name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$',
        views.SnippetDetail.as_view(),
        name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight'),
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail'),
    # url(r'^api-token-auth/',
    #     obtain_jwt_token),
    url(r'^sign_up/$', views.SignUp.as_view(), name="sign_up"),
    url(
        r'^snippets2/$',
        views.SnippetListView.as_view(),
        name="snippet-list-2"
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# Login and logout views for the browsable API
urlpatterns += [
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
        # Tip : namespace is optional since Django 1.9+
    ),
]
