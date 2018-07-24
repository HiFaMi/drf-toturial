from django.urls import path

from ..views import generic_cbv

urlpatterns = [
    path('snippets/', generic_cbv.SnippetList.as_view(), name='snippets-list'),
    path('snippets/<int:pk>/', generic_cbv.SnippetDetail.as_view(), name='snippets-detail'),
    path('users/', generic_cbv.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', generic_cbv.UserDetail.as_view(), name='user-detail'),
]