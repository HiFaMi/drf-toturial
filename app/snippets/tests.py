import json
import random
from django.utils.six import BytesIO


from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.parsers import JSONParser

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Snippet
from snippets.serializers import SnippetListSerializer

User = get_user_model()
DUMMY_USER_USERNAME = 'dummy_username'


def get_dummy_user():
    return User.objects.create_user(username=DUMMY_USER_USERNAME)


class SnippetListTest(APITestCase):
    """
    Snippet List요청에 대한 테스트
    """

    URL = '/snippets/generic_cbv/snippets/'
    DECENDING_URL = '/snippets/generic_cbv/snippets/?page='

    def test_status_code(self):
        """
        요청 결과의 HTTP상태코드가 200인지 확인
        :return:
        """
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_snippet_list_count(self):
        """
        Snippet List를 요청시 DB에 있는 자료수와 같은 갯수가 리턴되는지 테스트
        :return:
        """
        user = get_dummy_user()
        for i in range(random.randint(10, 100)):
            Snippet.objects.create(code='a={}'.format(i), owner=user)
        response = self.client.get(self.URL)
        data = json.loads(response.content)
        self.assertEqual(data['count'], Snippet.objects.count())

    def test_snippet_list_order_by_created_desending(self):
        """
        Snippet List의 결과가 생성일자 내림차순인지 확인
        :return:
        """
        user = get_dummy_user()
        for i in range(random.randint(5, 10)):
            Snippet.objects.create(code='a={}'.format(i), owner=user)
        response = self.client.get(self.DECENDING_URL+'1')
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

        # self.assertEqual(
        #     [item['pk'] for item in data],
        #     # flat default = False 각각의 튜플이 반환된 쿼리셋 리스트를 준다.
        #     # flat = True의 경우 반환하고자 하는 객체 그대로 반환된 쿼리셋 리스트를 준다.
        #     list(Snippet.objects.order_by('-created').values_list('pk', flat=True)),
        # )
        pk_list = []
        i = 0
        while True:
            if data['next']:
                response = self.client.get(self.DECENDING_URL + '{}'.format(i+1))
                data = json.loads(response.content)

                for item in data['results']:
                    pk_list.append(item['pk'])
                i += 1
            else:
                break

        self.assertEqual(
            pk_list,
            list(Snippet.objects.order_by('created').values_list('pk', flat=True)),
        )


class SnippetCreateTest(APITestCase):
    URL = '/snippets/generic_cbv/snippets/'

    def authenticate_user(self):

        user = get_dummy_user()
        self.client = APIClient()
        return self.client.force_authenticate(user=user)

    def test_snippet_create_status_code(self):
        """
        201이 돌아오는지
        :return:
        """

        # self.authenticate_user()
        user = get_dummy_user()
        self.client.force_authenticate(user=user)
        dummy = {
            "code": "asdf",
        }
        data = json.dumps(dummy)
        response = self.client.post(
            self.URL,
            data,
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_snippet_create_save_db(self):
        """
        요청 후 실제 DB에 저장되었는지 (모든 필드값이 정상적으로 저장되는지)
        :return:
        """
        # 하나 생성 하였을 경우 생성한 것과 데이터 베이스를 비교
        # dummy = {"code": "print('hello)"}
        # self.client.post(
        #     '/snippets/django_view/snippets/',
        #     json.dumps(dummy),
        #     content_type="application/json")
        # another_response = self.client.get('/snippets/django_view/snippets/')
        # data = json.loads(another_response.content)
        # self.assertEqual(
        #     data[0]['code'],
        #     Snippet.objects.last().code
        # )

        # 여러개 생성 한 다음 데이터 베이스와 비교
        # dummy = [{"code": "{}".format(i)} for i in range(random.randint(5, 10))]
        #
        # for dummy_index in range(len(dummy)):
        #     self.client.post(
        #         '/snippets/django_view/snippets/',
        #         json.dumps(dummy[dummy_index]),
        #         content_type="application/json"
        #     )
        #
        # response = self.client.get('/snippets/django_view/snippets/')
        # data = json.loads(response.content)
        #
        # self.assertEqual(
        #     [item['code'] for item in data],
        #     list(Snippet.objects.order_by('-created').values_list('code', flat=True))
        # )

        self.authenticate_user()

        snippet_data = {
            'title': 'SnippetTitle',
            'code': 'SnippetCode',
            'linenos': True,
            'language': 'c',
            'style': 'monokai',
        }

        response = self.client.post(
            self.URL,
            data=snippet_data,
            format='json'
        )
        data = json.loads(response.content)

        check_field = [
            'title',
            'linenos',
            'language',
            'style',
        ]

        for field in check_field:
            self.assertEqual(data[field], snippet_data[field])

    def test_snippet_create_missing_code_raise_exception(self):
        """
        'code' 데이터가 주어지지 않을 경우 적절한 Exception이 발생하는지
        :return:
        """
        self.authenticate_user()

        snippet_data = {
            'title': 'SnippetTitle',
            'linenos': True,
            'language': 'c',
            'style': 'monokai',
        }

        response = self.client.post(
            self.URL,
            json.dumps(snippet_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
