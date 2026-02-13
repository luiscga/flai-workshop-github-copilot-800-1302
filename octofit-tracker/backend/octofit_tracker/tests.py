from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertIsNotNone(self.user._id)


class TeamModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(
            name="Test Team",
            description="A test team"
        )
    
    def test_team_creation(self):
        self.assertEqual(self.team.name, "Test Team")
        self.assertEqual(self.team.description, "A test team")
        self.assertIsNotNone(self.team._id)


class ActivityModelTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id="user123",
            activity_type="Running",
            duration=30,
            distance=5.0,
            calories=300,
            date=datetime.now()
        )
    
    def test_activity_creation(self):
        self.assertEqual(self.activity.activity_type, "Running")
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories, 300)
        self.assertIsNotNone(self.activity._id)


class LeaderboardModelTest(TestCase):
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            user_id="user123",
            team_id="team456",
            total_activities=10,
            total_calories=3000,
            total_distance=50.0,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        self.assertEqual(self.leaderboard.user_id, "user123")
        self.assertEqual(self.leaderboard.total_activities, 10)
        self.assertEqual(self.leaderboard.rank, 1)
        self.assertIsNotNone(self.leaderboard._id)


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.workout = Workout.objects.create(
            name="Morning Run",
            description="A refreshing morning run",
            difficulty="Medium",
            duration=45,
            calories_estimate=400,
            category="Cardio"
        )
    
    def test_workout_creation(self):
        self.assertEqual(self.workout.name, "Morning Run")
        self.assertEqual(self.workout.difficulty, "Medium")
        self.assertEqual(self.workout.category, "Cardio")
        self.assertIsNotNone(self.workout._id)


class APIRootTest(APITestCase):
    def test_api_root(self):
        url = reverse('api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)


class UserAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_create_user(self):
        url = reverse('user-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'Test User')
    
    def test_get_users(self):
        User.objects.create(**self.user_data)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TeamAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            'name': 'Test Team',
            'description': 'A test team'
        }
    
    def test_create_team(self):
        url = reverse('team-list')
        response = self.client.post(url, self.team_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get().name, 'Test Team')
    
    def test_get_teams(self):
        Team.objects.create(**self.team_data)
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ActivityAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.activity_data = {
            'user_id': 'user123',
            'activity_type': 'Running',
            'duration': 30,
            'distance': 5.0,
            'calories': 300,
            'date': datetime.now().isoformat()
        }
    
    def test_create_activity(self):
        url = reverse('activity-list')
        response = self.client.post(url, self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
    
    def test_get_activities(self):
        Activity.objects.create(
            user_id='user123',
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            date=datetime.now()
        )
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class LeaderboardAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.leaderboard_data = {
            'user_id': 'user123',
            'team_id': 'team456',
            'total_activities': 10,
            'total_calories': 3000,
            'total_distance': 50.0,
            'rank': 1
        }
    
    def test_create_leaderboard_entry(self):
        url = reverse('leaderboard-list')
        response = self.client.post(url, self.leaderboard_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Leaderboard.objects.count(), 1)
    
    def test_get_leaderboard(self):
        Leaderboard.objects.create(**self.leaderboard_data)
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class WorkoutAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.workout_data = {
            'name': 'Morning Run',
            'description': 'A refreshing morning run',
            'difficulty': 'Medium',
            'duration': 45,
            'calories_estimate': 400,
            'category': 'Cardio'
        }
    
    def test_create_workout(self):
        url = reverse('workout-list')
        response = self.client.post(url, self.workout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)
    
    def test_get_workouts(self):
        Workout.objects.create(**self.workout_data)
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
