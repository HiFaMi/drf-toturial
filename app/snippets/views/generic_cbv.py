from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination

from utils.pageinaction import SnippetListPagination
from ..permissions import IsOwnerOrReadOnly
from ..models import Snippet
from ..serializers import SnippetListSerializer, UserListSerializer, SnippetDetailSerializer
from rest_framework import generics, permissions


User = get_user_model()

__all__ = (
    'SnippetList',
    'SnippetDetail',
    'UserList',
    'UserDetail',
)


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = SnippetListPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SnippetListSerializer
        else:
            return SnippetDetailSerializer

    def perform_create(self, serializer):
        # SnippetListSerializer로 전달받은 데이터
        # 'owner'항목에 self.request.user데이터를 추가한 후
        # save() 호출, DB에 저장 및 인스턴스 반환
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetDetailSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly,
    )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


