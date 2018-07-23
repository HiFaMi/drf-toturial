from django.urls import path

from ..views import mixins

app_name = 'mixins'
urlpatterns = [
    path('snippets/', mixins.SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', mixins.SnippetDetail.as_view(), name='snippet-detail'),
]
