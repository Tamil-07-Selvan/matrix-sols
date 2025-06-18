from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    game_id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.game_id})"
    
    class Meta:
        ordering = ['name']

class TopUpProduct(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    in_game_currency = models.CharField(max_length=50)  # e.g., "500 UC", "1000 Diamonds"
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.game.name} (${self.price})"
    
    class Meta:
        ordering = ['game__name', 'price']
        unique_together = ['game', 'name']

class TopUpOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'), 
        ('failed', 'Failed'),
    ]
    
    user_email = models.EmailField()
    product = models.ForeignKey(TopUpProduct, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user_email} - {self.product.name}"
    
    class Meta:
        ordering = ['-created_at']