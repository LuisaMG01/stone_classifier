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

class RockPrediction(models.Model):
    image = models.ImageField(upload_to='rock_images/')
    predicted_class = models.CharField(max_length=100)
    confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.predicted_class} ({self.created_at})"
