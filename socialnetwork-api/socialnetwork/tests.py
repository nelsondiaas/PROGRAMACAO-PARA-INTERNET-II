from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

User = get_user_model()

'''
Quando executa esses tests, terá que commentar o
'DEFAULT_THROTTLE_RATES', que está em config/settings.py,
pois o mesmo permite apenas 1 token gerado a cada hora por user.

'''

class APITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def get_token(self):
        user = User.objects.create_user(username="nelson", password="admin@123")
        token = Token.objects.get_or_create(user=user)
        return str(token[0])
    
    def test_user_list(self):
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, 200)

    def test_profile_list(self):
        response = self.client.get(reverse('profiles-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list(self):
        response = self.client.get(reverse('posts-list'))
        self.assertEqual(response.status_code, 200)

    def test_comment_list(self):
        response = self.client.get(reverse('comments-list'))
        self.assertEqual(response.status_code, 200)