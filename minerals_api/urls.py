from django.urls import path
from .views import MineralPredictionView, MineralPredictionListView

urlpatterns = [
    path('predict/', MineralPredictionView.as_view(), name='predict_mineral'),
    path('predictions/', MineralPredictionListView.as_view(), name='list_predictions'),
] 