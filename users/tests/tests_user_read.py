from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()
        
class UserReadTests(APITestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1',
                                              email='user1@example.com',
                                              password='pass')
        
        self.user2 = User.objects.create_user(username='user2',
                                              email='user2@example.com',
                                              password='pass')
        self.client.login(email='user1@example.com', password='pass')
        
            
    def test_01_list_users(self):
        self.client.force_authenticate(user=self.user1)
        
        url = '/api/users/list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('results', response.data)
        users_data = response.data['results']
        
        self.assertGreaterEqual(len(users_data), 2)
        
        usernames = [user['username'] for user in users_data]
        self.assertIn(self.user1.username, usernames)
        
        self.assertIn('email', users_data[0])
        self.assertIn('followers', users_data[0])
        self.assertIn('following', users_data[0])


    def test_02_user_detail(self):
        self.client.force_authenticate(user=self.user1)
        
        url = f'/api/users/detail/{self.user2.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('id', response.data)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)
        self.assertIn('followers', response.data)
        self.assertIn('following', response.data)
        
        self.assertEqual(response.data['id'], self.user2.id)
        self.assertEqual(response.data['email'], self.user2.email)
        self.assertEqual(response.data['username'], self.user2.username)
        
        self.assertIsInstance(response.data['followers'], list)
        self.assertIsInstance(response.data['following'], list)


    def test_03_user_profile_followers_count(self):
        follower1 = User.objects.create_user(
                                        username='follower1',
                                        email='follower1@example.com',
                                        password='pass1')
        follower2 = User.objects.create_user(
                                        username='follower2',
                                        email='follower2@example.com',
                                        password='pass2')
        
        follower1.following.add(self.user2)
        follower2.following.add(self.user2)
        self.client.force_authenticate(user=self.user2)
        
        url = f'/api/users/detail/{self.user2.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('followers_count', response.data)
        self.assertEqual(response.data['followers_count'], 2)
        
        
