from rest_framework import serializers
from .models import MineralPrediction

class MineralInputSerializer(serializers.Serializer):
    """
    Serializador para la entrada de datos para predecir un mineral.
    """
    Element = serializers.CharField(max_length=50)
    Specific_Gravity = serializers.FloatField()
    Calculated_Density = serializers.FloatField()
    Refractive_Index = serializers.FloatField(required=False, allow_null=True)
    Mohs_Hardness = serializers.FloatField()
    Optical = serializers.FloatField(required=False, allow_null=True)

class MineralOutputSerializer(serializers.ModelSerializer):
    """
    Serializador para el resultado de la predicción de minerales.
    """
    class Meta:
        model = MineralPrediction
        fields = '__all__' 