import json
import random

from django.test import TestCase
from rest_framework.parsers import JSONParser

from rest_framework.test import APITestCase
from rest_framework import status

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetListTest(APITestCase):
    """
    Snippet List요청에 대한 테스트
    """

    def test_status_code(self):
        """
        요청 결과의 HTTP상태코드가 200인지 확인
        :return:
        """
        response = self.client.get('/snippets/django_view/snippets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_snippet_list_count(self):
        """
        Snippet List를 요청시 DB에 있는 자료수와 같은 갯수가 리턴되는지 테스트
        :return:
        """
        for i in range(random.randint(10, 100)):
            Snippet.objects.create(code='a={}'.format(i))
        response = self.client.get('/snippets/django_view/snippets/')
        data = json.loads(response.content)
        self.assertEqual(len(data), Snippet.objects.count())



    def test_snippet_list_order_by_created_desending(self):
        """
        Snippet List의 결과가 생성일자 내림차순인지 확인
        :return:
        """
        for i in range(random.randint(5, 10)):
            Snippet.objects.create(code='a={}'.format(i))
        response = self.client.get('/snippets/django_view/snippets/')
        data = json.loads(response.content)
        # snippets = Snippet.objects.order_by('-created')
        #
        # data_pk_list = []
        # for item in data:
        #     data_pk_list.append(item['pk'])
        #
        # snippets_pk_list = []
        # for snippet in snippets:
        #     snippets_pk_list.append(snippet.pk)

        self.assertEqual(
            [item['pk'] for item in data],
            list(Snippet.objects.order_by('-created').values_list('pk', flat=True)),
        )
