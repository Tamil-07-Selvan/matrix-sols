from django.core.management.base import BaseCommand
from topup.models import Game, TopUpProduct, TopUpOrder
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate the database with sample gaming data'

    def handle(self, *args, **options):
        # Create sample games
        games_data = [
            {'name': 'PUBG Mobile', 'game_id': 'pubg123'},
            {'name': 'Mobile Legends', 'game_id': 'ml456'},
            {'name': 'Free Fire', 'game_id': 'ff789'},
            {'name': 'Call of Duty Mobile', 'game_id': 'cod101'},
        ]
        
        games = []
        for game_data in games_data:
            game, created = Game.objects.get_or_create(**game_data)
            games.append(game)
            if created:
                self.stdout.write(f'Created game: {game.name}')

        # Create sample products
        products_data = [
            # PUBG Mobile
            {'game': games[0], 'name': 'UC Pack 60', 'price': Decimal('0.99'), 'in_game_currency': '60 UC'},
            {'game': games[0], 'name': 'UC Pack 325', 'price': Decimal('4.99'), 'in_game_currency': '325 UC'},
            {'game': games[0], 'name': 'UC Pack 660', 'price': Decimal('9.99'), 'in_game_currency': '660 UC'},
            
            # Mobile Legends
            {'game': games[1], 'name': 'Diamond 86', 'price': Decimal('2.99'), 'in_game_currency': '86 Diamonds'},
            {'game': games[1], 'name': 'Diamond 172', 'price': Decimal('4.99'), 'in_game_currency': '172 Diamonds'},
            
            # Free Fire
            {'game': games[2], 'name': 'Diamond 100', 'price': Decimal('1.99'), 'in_game_currency': '100 Diamonds'},
            {'game': games[2], 'name': 'Diamond 520', 'price': Decimal('9.99'), 'in_game_currency': '520 Diamonds'},
        ]
        
        products = []
        for product_data in products_data:
            product, created = TopUpProduct.objects.get_or_create(**product_data)
            products.append(product)
            if created:
                self.stdout.write(f'Created product: {product.name}')

        # Create sample orders
        sample_emails = [
            'player1@example.com', 'gamer2@test.com', 'user3@sample.com',
            'player4@example.com', 'gamer5@test.com'
        ]
        
        statuses = ['success', 'pending', 'failed']
        
        for i in range(50):  # Create 50 sample orders
            order = TopUpOrder.objects.create(
                user_email=random.choice(sample_emails),
                product=random.choice(products),
                status=random.choices(statuses, weights=[70, 20, 10])[0]  # 70% success, 20% pending, 10% failed
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))
