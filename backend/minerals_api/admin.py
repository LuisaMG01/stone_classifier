from django.contrib import admin
from .models import MineralPrediction, RockPrediction

@admin.register(MineralPrediction)
class MineralPredictionAdmin(admin.ModelAdmin):
    list_display = ['element', 'predicted_group', 'created_at']
    list_filter = ['predicted_group']
    search_fields = ['element', 'predicted_group']

@admin.register(RockPrediction)
class RockPredictionAdmin(admin.ModelAdmin):
    list_display = ['predicted_class', 'confidence', 'created_at']
    list_filter = ['predicted_class']
    search_fields = ['predicted_class']
