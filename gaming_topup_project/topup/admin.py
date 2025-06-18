from django.contrib import admin
from .models import Game, TopUpProduct, TopUpOrder

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_id', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'game_id')
    list_editable = ('is_active',)

@admin.register(TopUpProduct)
class TopUpProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'price', 'in_game_currency', 'is_active', 'created_at')
    list_filter = ('game', 'is_active', 'created_at')
    search_fields = ('name', 'game__name', 'in_game_currency')
    list_editable = ('price', 'is_active')
    list_select_related = ('game',)

@admin.register(TopUpOrder)
class TopUpOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_email', 'product', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'product__game')
    search_fields = ('user_email', 'product__name', 'product__game__name')
    list_select_related = ('product', 'product__game')
    readonly_fields = ('created_at', 'updated_at')