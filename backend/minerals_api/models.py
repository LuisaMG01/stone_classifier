from django.db import models

# Create your models here.

class MineralPrediction(models.Model):
    """
    Modelo para almacenar las predicciones de minerales.
    """
    element = models.CharField(max_length=50)
    specific_gravity = models.FloatField()
    calculated_density = models.FloatField()
    refractive_index = models.FloatField(null=True, blank=True)
    mohs_hardness = models.FloatField()
    optical = models.FloatField(null=True, blank=True)
    predicted_group = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.element} - {self.predicted_group}"
