from rest_framework.test import APITestCase
from posts.models import Post
from django.contrib.auth import get_user_model
from rest_framework import status


User = get_user_model()

class FeedTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1',
                                              email='user1@example.com',
                                              password='pass')
        
        self.user2 = User.objects.create_user(username='user2',
                                              email='user2@example.com',
                                              password='pass2')
        self.user1.following.add(self.user2)
        self.client.force_authenticate(user=self.user1)

    def test_01_feed_only_followed_users(self):
        Post.objects.create(author=self.user2, content='Followed user post')
        url = '/api/feed/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['content'], 'Followed user post')



    def test_02_feed_multiple_posts(self):
        user3 = User.objects.create_user(username='user3',
                                        email='user3@example.com',
                                        password='pass3')
        
        user4 = User.objects.create_user(username='user4',
                                        email='user4@example.com',
                                        password='pass4')

        self.user1.following.add(self.user2, user3, user4)

        post1 = Post.objects.create(author=self.user2, content='User2 Post')
        post2 = Post.objects.create(author=user3, content='User3 Post')
        post3 = Post.objects.create(author=user4, content='User4 Post')

        self.client.force_authenticate(user=self.user1)

        url = '/api/feed/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        contents = [post['content'] for post in response.data['results']]
        
        expected_posts = sorted([post1, post2, post3], key=lambda p: p.created_at, reverse=True)
        expected_contents = [p.content for p in expected_posts]

        self.assertEqual(contents, expected_contents)
        
        
    
    def test_03_feed_empty_for_user_with_no_posts(self):
        user_follower = User.objects.create_user(username='userfollower',
                                                 email='userfollower@example.com',
                                                 password='passuserfollower')
        
        user_followed = User.objects.create_user(username='userfollowed',
                                                 email='userfollowed@example.com',
                                                 password='passuserfollowed')
        
        user_follower.following.add(user_followed)
        self.client.force_authenticate(user=user_follower)
        
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)
        
        
        
    def test_04_feed_exclude_non_followed_users(self):
        user6 = User.objects.create_user(username='user6',
                                         email='user6@example.com',
                                         password='pass6')
        
        user7 = User.objects.create_user(username='user7',
                                         email='user7@example.com',
                                         password='pass7')

        self.user1.following.add(user6)

        post1 = Post.objects.create(author=user6, content='User6 Post')
        post2 = Post.objects.create(author=user7, content='User7 Post')

        self.client.force_authenticate(user=self.user1)

        url = '/api/feed/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['content'], 'User6 Post')
        
        
        
    def test_05_feed_pagination(self):
        
        for i in range(15):
            Post.objects.create(author=self.user2, content=f'Post {i}')
        
        self.client.force_authenticate(user=self.user1)
        url = '/api/feed/?page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertTrue('next' in response.data)

        url = response.data['next']
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        
        
        
    def test_06_feed_multiple_users_posts(self):
        user9 = User.objects.create_user(username='user9', email='user9@example.com', password='pass')
        user10 = User.objects.create_user(username='user10', email='user10@example.com', password='pass')

        self.user1.following.add(user9, user10)

        post1 = Post.objects.create(author=user9, content='User9 Post')
        post2 = Post.objects.create(author=user10, content='User10 Post')

        self.client.force_authenticate(user=self.user1)

        url = '/api/feed/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn('User9 Post', [post['content'] for post in response.data['results']])
        self.assertIn('User10 Post', [post['content'] for post in response.data['results']])
        
        


        
        
    