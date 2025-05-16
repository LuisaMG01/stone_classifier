from django.urls import path
from .views import MineralPredictionView, MineralPredictionListView, ModelMetricsView, RockPredictionView, RockPredictionListView

urlpatterns = [
    path('predict/', MineralPredictionView.as_view(), name='predict_mineral'),
    path('history/', MineralPredictionListView.as_view(), name='mineral_history'),
    path('metrics/', ModelMetricsView.as_view(), name='model_metrics'),
    
    # Rutas para clasificación de rocas
    path('rocks/predict/', RockPredictionView.as_view(), name='predict_rock'),
    path('rocks/history/', RockPredictionListView.as_view(), name='rock_history'),
] 