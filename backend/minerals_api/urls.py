from django.urls import path
from .views import MineralPredictionView, MineralPredictionListView, ModelMetricsView

urlpatterns = [
    path('predict/', MineralPredictionView.as_view(), name='predict_mineral'),
    path('history/', MineralPredictionListView.as_view(), name='mineral_history'),
    path('metrics/', ModelMetricsView.as_view(), name='model_metrics'),
] 