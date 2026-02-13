from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write('Creating teams...')
        
        # Create teams
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes'
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League Members'
        )
        
        self.stdout.write('Creating users...')
        
        # Create Marvel superhero users
        marvel_heroes = [
            {'name': 'Tony Stark', 'email': 'ironman@marvel.com', 'password': 'stark123'},
            {'name': 'Steve Rogers', 'email': 'captainamerica@marvel.com', 'password': 'rogers123'},
            {'name': 'Thor Odinson', 'email': 'thor@marvel.com', 'password': 'thor123'},
            {'name': 'Natasha Romanoff', 'email': 'blackwidow@marvel.com', 'password': 'natasha123'},
            {'name': 'Bruce Banner', 'email': 'hulk@marvel.com', 'password': 'banner123'},
            {'name': 'Peter Parker', 'email': 'spiderman@marvel.com', 'password': 'parker123'},
        ]
        
        # Create DC superhero users
        dc_heroes = [
            {'name': 'Clark Kent', 'email': 'superman@dc.com', 'password': 'kent123'},
            {'name': 'Bruce Wayne', 'email': 'batman@dc.com', 'password': 'wayne123'},
            {'name': 'Diana Prince', 'email': 'wonderwoman@dc.com', 'password': 'diana123'},
            {'name': 'Barry Allen', 'email': 'flash@dc.com', 'password': 'barry123'},
            {'name': 'Arthur Curry', 'email': 'aquaman@dc.com', 'password': 'arthur123'},
            {'name': 'Hal Jordan', 'email': 'greenlantern@dc.com', 'password': 'hal123'},
        ]
        
        marvel_users = []
        dc_users = []
        
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                password=hero['password'],
                team_id=str(team_marvel._id)
            )
            marvel_users.append(user)
        
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                password=hero['password'],
                team_id=str(team_dc._id)
            )
            dc_users.append(user)
        
        all_users = marvel_users + dc_users
        
        self.stdout.write('Creating activities...')
        
        # Create activities for each user
        activity_types = ['Running', 'Swimming', 'Cycling', 'Weight Training', 'Yoga', 'Boxing']
        
        for user in all_users:
            for i in range(random.randint(5, 15)):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                distance = round(random.uniform(1, 20), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                calories = duration * random.randint(5, 10)
                date = datetime.now() - timedelta(days=random.randint(1, 30))
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=calories,
                    date=date,
                    notes=f'{activity_type} session by {user.name}'
                )
        
        self.stdout.write('Creating leaderboard entries...')
        
        # Create leaderboard entries
        for user in all_users:
            activities = Activity.objects.filter(user_id=str(user._id))
            total_activities = activities.count()
            total_calories = sum(activity.calories for activity in activities)
            total_distance = sum(activity.distance for activity in activities if activity.distance)
            
            Leaderboard.objects.create(
                user_id=str(user._id),
                team_id=user.team_id,
                total_activities=total_activities,
                total_calories=total_calories,
                total_distance=round(total_distance, 2)
            )
        
        # Update ranks
        leaderboard_entries = Leaderboard.objects.all().order_by('-total_calories')
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()
        
        self.stdout.write('Creating workout suggestions...')
        
        # Create workout suggestions
        workouts = [
            {
                'name': 'Super Soldier Strength',
                'description': 'High-intensity strength training inspired by Captain America',
                'difficulty': 'Hard',
                'duration': 60,
                'calories_estimate': 600,
                'category': 'Strength'
            },
            {
                'name': 'Web-Slinger Cardio',
                'description': 'Fast-paced cardio workout like Spider-Man swinging through the city',
                'difficulty': 'Medium',
                'duration': 45,
                'calories_estimate': 450,
                'category': 'Cardio'
            },
            {
                'name': 'Amazon Warrior Training',
                'description': 'Combat-focused workout inspired by Wonder Woman',
                'difficulty': 'Hard',
                'duration': 75,
                'calories_estimate': 700,
                'category': 'Combat'
            },
            {
                'name': 'Flash Speed Circuit',
                'description': 'High-speed interval training for maximum calorie burn',
                'difficulty': 'Hard',
                'duration': 30,
                'calories_estimate': 500,
                'category': 'HIIT'
            },
            {
                'name': 'Zen Master Meditation',
                'description': 'Mindfulness and flexibility workout',
                'difficulty': 'Easy',
                'duration': 30,
                'calories_estimate': 150,
                'category': 'Yoga'
            },
            {
                'name': 'Dark Knight Endurance',
                'description': 'Batman-inspired endurance and stamina training',
                'difficulty': 'Medium',
                'duration': 60,
                'calories_estimate': 550,
                'category': 'Endurance'
            },
            {
                'name': 'Asgardian Power Lift',
                'description': 'Thor-inspired heavy lifting and power training',
                'difficulty': 'Hard',
                'duration': 50,
                'calories_estimate': 600,
                'category': 'Powerlifting'
            },
            {
                'name': 'Atlantean Swimming',
                'description': 'Aquaman-inspired swimming workout for full-body conditioning',
                'difficulty': 'Medium',
                'duration': 45,
                'calories_estimate': 400,
                'category': 'Swimming'
            },
        ]
        
        for workout in workouts:
            Workout.objects.create(**workout)
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
        self.stdout.write(f'Created {len(all_users)} users')
        self.stdout.write(f'Created 2 teams')
        self.stdout.write(f'Created {Activity.objects.count()} activities')
        self.stdout.write(f'Created {Leaderboard.objects.count()} leaderboard entries')
        self.stdout.write(f'Created {Workout.objects.count()} workout suggestions')
