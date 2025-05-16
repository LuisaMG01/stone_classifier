import { BaseService } from '@/shared/services/BaseService';
import type { RockPredictionResponse } from '@/shared/interfaces/rocks/RockResponseInterface';

// En un entorno de producción, esto vendría de las variables de entorno
const API_URL = 'http://localhost:8000/api/minerals/';

class RockService extends BaseService {
  /**
   * Realiza una predicción de la clase de roca basado en una imagen
   * @param formData FormData con la imagen de la roca
   * @returns Respuesta con la predicción de la clase de roca
   */
  async predictRock(formData: FormData): Promise<RockPredictionResponse> {
    const url = `${API_URL}rocks/predict/`;
    return this.makeRequest(url, true, 'post', formData, {
      'Content-Type': 'multipart/form-data'
    });
  }

  /**
   * Obtiene el historial de predicciones de rocas realizadas
   * @returns Lista de predicciones anteriores
   */
  async getPredictionHistory(): Promise<RockPredictionResponse[]> {
    const url = `${API_URL}rocks/history/`;
    return this.makeRequest(url, true);
  }
}

export default new RockService(); 