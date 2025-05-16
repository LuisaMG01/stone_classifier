from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MineralInputSerializer, MineralOutputSerializer
from .models import MineralPrediction
import sys
import os
import pandas as pd
from .model_metrics import (
    generate_confusion_matrix,
    get_feature_importance,
    get_class_distribution,
    generate_pca_visualization,
    get_model_stats
)

# Agregar la ruta del proyecto al path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Importar las funciones de predicción desde el módulo minerals
from src.minerals.predict import predict
from src.minerals.preprocess import load_chemical_group_mapping

class MineralPredictionView(APIView):
    """
    Vista para realizar predicciones de minerales.
    
    Para usar esta API, envíe una solicitud POST con un objeto JSON que tenga la siguiente estructura:
    
    ```json
    {
        "Element": "Silicon",
        "Specific_Gravity": 2.33,
        "Calculated_Density": 2.33,
        "Refractive_Index": 3.42,
        "Mohs_Hardness": 7,
        "Optical": 1
    }
    ```
    
    Todos los campos son requeridos excepto `Refractive_Index` y `Optical` que pueden ser omitidos o nulos.
    
    La respuesta contendrá todos los datos ingresados más el grupo químico predicho para el mineral.
    """
    def post(self, request, format=None):
        serializer = MineralInputSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Preparar los datos para la predicción
                input_data = serializer.validated_data
                
                # Convertir el input a un DataFrame para la predicción
                # Asegurarse de que los nombres de las columnas coincidan con lo que espera el modelo
                transformed_data = {
                    "Element": input_data["Element"],
                    "Specific Gravity": input_data["Specific_Gravity"],
                    "Calculated Density": input_data["Calculated_Density"],
                    "Refractive Index": input_data.get("Refractive_Index"),
                    "Mohs Hardness": input_data["Mohs_Hardness"],
                    "Optical": input_data.get("Optical", 0)
                }
                
                input_df = pd.DataFrame([transformed_data])
                
                # Realizar la predicción utilizando el modelo
                model_path = os.path.join(BASE_DIR, 'model/crystal_model.pkl')
                reference_data_path = os.path.join(BASE_DIR, 'data/minerals/minerals.csv')
                
                predicted_group = predict(
                    input_df,
                    model_path=model_path,
                    reference_data_path=reference_data_path
                )[0]  # Obtenemos el primer resultado
                
                # Guardar la predicción en la base de datos
                prediction = MineralPrediction(
                    element=input_data['Element'],
                    specific_gravity=input_data['Specific_Gravity'],
                    calculated_density=input_data['Calculated_Density'],
                    refractive_index=input_data.get('Refractive_Index'),
                    mohs_hardness=input_data['Mohs_Hardness'],
                    optical=input_data.get('Optical'),
                    predicted_group=predicted_group
                )
                prediction.save()
                
                # Serializar la respuesta
                output_serializer = MineralOutputSerializer(prediction)
                return Response(output_serializer.data, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MineralPredictionListView(APIView):
    """
    Vista para listar todas las predicciones de minerales realizadas.
    
    Esta API devuelve una lista de todas las predicciones de minerales realizadas,
    ordenadas por fecha de creación (las más recientes primero).
    """
    def get(self, request, format=None):
        predictions = MineralPrediction.objects.all().order_by('-created_at')
        serializer = MineralOutputSerializer(predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ModelMetricsView(APIView):
    """
    Vista para obtener métricas y visualizaciones del modelo de clasificación.
    
    Esta API devuelve datos sobre el modelo de clasificación, como matriz de confusión,
    importancia de características, distribución de clases, etc.
    """
    def get(self, request, format=None):
        try:
            metrics_type = request.query_params.get('type', 'all')
            
            if metrics_type == 'confusion_matrix':
                data = generate_confusion_matrix()
            elif metrics_type == 'feature_importance':
                data = get_feature_importance()
            elif metrics_type == 'class_distribution':
                data = get_class_distribution()
            elif metrics_type == 'pca':
                data = generate_pca_visualization()
            elif metrics_type == 'stats':
                data = get_model_stats()
            else:
                # Devolver todas las métricas
                data = {
                    'confusion_matrix': generate_confusion_matrix(),
                    'feature_importance': get_feature_importance(),
                    'class_distribution': get_class_distribution(),
                    'pca': generate_pca_visualization(),
                    'stats': get_model_stats()
                }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
