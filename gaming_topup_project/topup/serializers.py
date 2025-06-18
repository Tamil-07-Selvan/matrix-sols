from rest_framework import serializers
from .models import Game, TopUpProduct, TopUpOrder

class TopUpOrderSerializer(serializers.Serializer):
    gamename = serializers.CharField(max_length=100)
    game_id = serializers.CharField(max_length=50)
    product_name = serializers.CharField(max_length=100)
    product_id = serializers.IntegerField()
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    user_email = serializers.EmailField()
    payment_status = serializers.ChoiceField(
        choices=['pending', 'success', 'failed'],
        default='pending'
    )
    
    def validate(self, data):
        # Check if game exists and is active
        try:
            game = Game.objects.get(
                name=data['gamename'],
                game_id=data['game_id'],
                is_active=True
            )
        except Game.DoesNotExist:
            raise serializers.ValidationError(
                "Game not found or inactive. Please check game name and game_id."
            )
        
        # Check if product exists and belongs to the game
        try:
            product = TopUpProduct.objects.get(
                id=data['product_id'],
                game=game,
                is_active=True
            )
        except TopUpProduct.DoesNotExist:
            raise serializers.ValidationError(
                "Product not found or not associated with the specified game."
            )
        
        # Validate product name matches
        if product.name != data['product_name']:
            raise serializers.ValidationError(
                "Product name doesn't match the product ID."
            )
        
        # Validate product price matches
        if product.price != data['product_price']:
            raise serializers.ValidationError(
                f"Product price mismatch. Expected: {product.price}, Got: {data['product_price']}"
            )
        
        # Store validated objects for use in create method
        data['_game'] = game
        data['_product'] = product
        
        return data
    
    def create(self, validated_data):
        # Create the order using validated product
        order = TopUpOrder.objects.create(
            user_email=validated_data['user_email'],
            product=validated_data['_product'],
            status=validated_data['payment_status']
        )
        return order

class TopUpOrderResponseSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(source='product.game.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = TopUpOrder
        fields = [
            'id', 'user_email', 'game_name', 'product_name', 
            'product_price', 'status', 'created_at'
        ]
