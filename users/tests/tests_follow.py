from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class FollowTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1',
                                              email='user1@example.com',
                                              password='pass')
        
        self.user2 = User.objects.create_user(username='user2',
                                              email='user2@example.com',
                                              password='pass')
        self.client.login(email='user1@example.com', password='pass')


    def test_01_follow_user(self):
        self.client.force_authenticate(user=self.user1)
        
        url = f'/api/users/follow/{self.user2.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user2, self.user1.following.all())


    def test_02_unfollow_user(self):
        self.user1.following.add(self.user2)
        self.client.force_authenticate(user=self.user1)
        
        url = f'/api/users/unfollow/{self.user2.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user2, self.user1.following.all())
        self.assertEqual(response.data['detail'], f'You have unfollowed {self.user2.username}')
        
        
    def test_03_follow_self(self):
        self.client.force_authenticate(user=self.user1)
        
        url = f'/api/users/follow/{self.user1.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(self.user1, self.user1.following.all())
        self.assertEqual(response.data['detail'], "You can't follow yourself")
        
        
    def test_04_unfollow_self(self):
        self.client.force_authenticate(user=self.user1)
        
        url = f'/api/users/unfollow/{self.user1.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(self.user1, self.user1.following.all())
        self.assertEqual(response.data['detail'], "You can't unfollow yourself")
        
    
    def test_05_follow_nonexistent_user(self):
        self.client.force_authenticate(user=self.user1)
        id_not_exist = 7777777
        url = f'/api/users/follow/{id_not_exist}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_06_unfollow_nonexistent_user(self):
        self.client.force_authenticate(user=self.user1)
        id_not_exist = 8888888
        url = f'/api/users/unfollow/{id_not_exist}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        
    def test_07_no_followers(self):
        self.client.force_authenticate(user=self.user1)
        
        url = f'/api/users/followers/{self.user1.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])
    
    
    def test_08_no_following(self):
        self.client.force_authenticate(user=self.user1)
            
        url = f'/api/users/following/{self.user1.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])
        
    
    def test_09_authentication_required_followers(self):
        self.client.logout()
        
        url = f'/api/users/followers/{self.user1.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        
