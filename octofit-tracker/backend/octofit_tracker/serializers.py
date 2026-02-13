from rest_framework import serializers
from bson import ObjectId
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.CharField(source='name', read_only=True)
    team_name = serializers.SerializerMethodField()
    fitness_level = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'password', 'team_id', 'team_name', 'fitness_level', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_id(self, obj):
        return str(obj._id)
    
    def get_team_name(self, obj):
        if obj.team_id:
            try:
                team = Team.objects.get(_id=ObjectId(obj.team_id))
                return team.name
            except (Team.DoesNotExist, Exception):
                return None
        return None
    
    def get_fitness_level(self, obj):
        # Calculate fitness level based on activity data
        try:
            leaderboard = Leaderboard.objects.get(user_id=str(obj._id))
            if leaderboard.total_calories >= 7000:
                return 'Advanced'
            elif leaderboard.total_calories >= 5000:
                return 'Intermediate'
            else:
                return 'Beginner'
        except Leaderboard.DoesNotExist:
            return 'Beginner'


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'member_count', 'created_at']
    
    def get_id(self, obj):
        return str(obj._id)
    
    def get_member_count(self, obj):
        return User.objects.filter(team_id=str(obj._id)).count()


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    duration_minutes = serializers.IntegerField(source='duration', read_only=True)
    calories_burned = serializers.IntegerField(source='calories', read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'user_name', 'activity_type', 'duration', 'duration_minutes', 
                  'distance', 'calories', 'calories_burned', 'date', 'notes']
    
    def get_id(self, obj):
        return str(obj._id)
    
    def get_user_name(self, obj):
        try:
            user = User.objects.get(_id=ObjectId(obj.user_id))
            return user.name
        except (User.DoesNotExist, Exception):
            return 'Unknown User'


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    total_points = serializers.IntegerField(source='total_calories', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'user_name', 'team_id', 'team_name', 'total_activities', 
                  'total_calories', 'total_points', 'total_distance', 'rank']
    
    def get_id(self, obj):
        return str(obj._id)
    
    def get_user_name(self, obj):
        try:
            user = User.objects.get(_id=ObjectId(obj.user_id))
            return user.name
        except (User.DoesNotExist, Exception):
            return 'Unknown User'
    
    def get_team_name(self, obj):
        try:
            team = Team.objects.get(_id=ObjectId(obj.team_id))
            return team.name
        except (Team.DoesNotExist, Exception):
            return None


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    difficulty_level = serializers.CharField(source='difficulty', read_only=True)
    duration_minutes = serializers.IntegerField(source='duration', read_only=True)
    calories_burned = serializers.IntegerField(source='calories_estimate', read_only=True)
    workout_type = serializers.CharField(source='category', read_only=True)
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty', 'difficulty_level', 'duration', 
                  'duration_minutes', 'calories_estimate', 'calories_burned', 'category', 'workout_type']
    
    def get_id(self, obj):
        return str(obj._id)
