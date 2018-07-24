from django.contrib.auth import get_user_model

from ..models import Snippet
from ..serializers import SnippetSerializer, UserSerializer
from rest_framework import generics

User = get_user_model()

__all__ = (
    'SnippetList',
    'SnippetDetail',
    'UserList',
    'UserDetail',
)


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        # SnippetSerializer로 전달받은 데이터
        # 'owner'항목에 self.request.user데이터를 추가한 후
        # save() 호출, DB에 저장 및 인스턴스 반환
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer