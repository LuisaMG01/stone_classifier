import axios from 'axios';
import { API_URL } from '../services/apiConfig';

class ModelMetricsService {
  /**
   * Obtiene la matriz de confusión del modelo
   */
  async getConfusionMatrix() {
    try {
      const response = await axios.get(`${API_URL}minerals/metrics/?type=confusion_matrix`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener la matriz de confusión:', error);
      throw error;
    }
  }

  /**
   * Obtiene la importancia de características del modelo
   */
  async getFeatureImportance() {
    try {
      const response = await axios.get(`${API_URL}minerals/metrics/?type=feature_importance`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener la importancia de características:', error);
      throw error;
    }
  }

  /**
   * Obtiene la distribución de clases del conjunto de datos
   */
  async getClassDistribution() {
    try {
      const response = await axios.get(`${API_URL}minerals/metrics/?type=class_distribution`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener la distribución de clases:', error);
      throw error;
    }
  }

  /**
   * Obtiene la visualización PCA del conjunto de datos
   */
  async getPCAVisualization() {
    try {
      const response = await axios.get(`${API_URL}minerals/metrics/?type=pca`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener la visualización PCA:', error);
      throw error;
    }
  }

  /**
   * Obtiene las estadísticas generales del modelo
   */
  async getModelStats() {
    try {
      const response = await axios.get(`${API_URL}minerals/metrics/?type=stats`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener las estadísticas del modelo:', error);
      throw error;
    }
  }

  /**
   * Obtiene todas las métricas del modelo en una sola petición
   */
  async getAllMetrics() {
    try {
      const response = await axios.get(`${API_URL}minerals/metrics/`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener todas las métricas:', error);
      throw error;
    }
  }
}

export default new ModelMetricsService(); 