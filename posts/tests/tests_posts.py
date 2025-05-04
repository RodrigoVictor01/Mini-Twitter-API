from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post
from users.models import User

User = get_user_model()

class PostTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com',
                                                         password='passwordtest',
                                                         username='testuser')
        self.client.force_authenticate(user=self.user)

    def test_01_create_post(self):
        data = {
        'title': 'Test Title',
        'content': 'This is a test post.'
        }
        
        url = '/api/posts/create/'
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().content, 'This is a test post.')
        
    def test_02_create_post_unauthenticated(self):
        self.client.logout()
        data = {
            'title': 'Test Title',
            'content': 'This is a test post.'
        }
        url = '/api/posts/create/'
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)
        
    
    def test_03_list_posts(self):
        Post.objects.create(content='Post 1', author=self.user)
        Post.objects.create(content='Post 2', author=self.user)
        
        url = '/api/posts/list/'
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        sorted_posts = sorted(response.data, key=lambda post: post['content'])
        self.assertEqual(sorted_posts[0]['content'], 'Post 1')
        self.assertEqual(sorted_posts[1]['content'], 'Post 2')
        
    
    def test_04_update_post(self):
        post = Post.objects.create(content='Old content', author=self.user)
        data = {'content': 'Updated content'}
        url = f'/api/posts/edit/{post.id}/'
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.content, 'Updated content')
    
    
    def test_05_like_post(self):
        post = Post.objects.create(content='Post to like', author=self.user)
        
        url = f'/api/posts/like/{post.id}/'
        response = self.client.post(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertIn(self.user, post.likes.all())
        
    
    def test_06_unlike_post(self):
        post = Post.objects.create(content='Post to unlike', author=self.user)
        post.likes.add(self.user)
        
        url = f'/api/posts/like/{post.id}/'
        response = self.client.post(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertNotIn(self.user, post.likes.all())
        self.assertEqual(post.likes.count(), 0)
        
        
    def test_07_like_post_nonexistent(self):
        id_not_exist = 7777777
        url = f'/api/posts/like/{id_not_exist}/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    
    def test_08_unlike_post_nonexistent(self):
        post = Post.objects.create(content='Post to unlike', author=self.user)
        
        id_not_exist = 8888888
        url = f'/api/posts/like/{id_not_exist}/'
        
        response = self.client.post(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        
    def test_09_create_post_invalid_data(self):
        data = {
            'title': '',
            'content': ''
        }
        url = '/api/posts/create/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_10_delete_post(self):
        post = Post.objects.create(content='Post to delete', author=self.user)
        url = f'/api/posts/delete/{post.id}/'
        response = self.client.delete(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
        
    def test_11_count_likes(self):
        post = Post.objects.create(content='Post to count likes',
                                   author=self.user)
        
        user2 = User.objects.create_user(email='user2@example.com',
                                        password='password2',
                                        username='user2')
        post.likes.add(self.user)
        post.likes.add(user2)
        
        url = f'/api/posts/list/like/{post.id}/'
        response = self.client.post(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes'], 2)

        post.refresh_from_db()
        self.assertIn(self.user, post.likes.all())
        self.assertIn(user2, post.likes.all())
        self.assertEqual(post.likes.count(), 2)
