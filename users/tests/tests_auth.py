from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):
    
    def test_01_user_registration(self):
        
        url = '/api/users/signup/'
        data = {
            'email': 'test@example.com',
            'username': 'newusertest',
            'password': 'testuserpassword',
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_02_user_login(self):
        
        User.objects.create_user(email='login@example.com',
                                username='loginusertest',
                                password='strongpassword')

        url = '/api/users/login/'
        data = {
            'email': 'login@example.com',
            'password': 'strongpassword',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
    
    def test_03_registration_with_invalid_email(self):
        url = '/api/users/signup/'
        data = {
            'email': 'invalid-email',
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_04_registration_with_existing_email(self):
        User.objects.create_user(email='duplicate@example.com',
                                 username='user1',
                                 password='testpass123')
        url = '/api/users/signup/'
        data = {
            'email': 'duplicate@example.com',
            'username': 'user2',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertTrue(len(response.data['email']) > 0)
        
    def test_05_login_with_wrong_password(self):
        User.objects.create_user(email='wrongpass@example.com',
                                 username='wronguser',
                                 password='correctpass')
        
        url = '/api/users/login/'
        data = {
            'email': 'wrongpass@example.com',
            'password': 'wrongpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_06_authenticated_access(self):
        User.objects.create_user(email='secure@example.com',
                        username='secureuser',
                        password='securepass')

        login_response = self.client.post('/api/users/login/', {
            'email': 'secure@example.com',
            'password': 'securepass'
        }, format='json')
        
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials()
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



