import { BaseService } from '@/shared/services/BaseService';
import type { MineralPredictionRequest, MineralPredictionResponse } from '@/shared/interfaces/minerals/MineralResponseInterface';

// En un entorno de producción, esto vendría de las variables de entorno
const API_URL = 'http://localhost:8000/api/minerals/';

class MineralService extends BaseService {
  /**
   * Realiza una predicción del grupo químico de un mineral basado en sus propiedades
   * @param mineralData Datos del mineral a predecir
   * @returns Respuesta con la predicción del grupo químico
   */
  async predictMineral(mineralData: MineralPredictionRequest): Promise<MineralPredictionResponse> {
    const url = `${API_URL}predict/`;
    return this.makeRequest(url, true, 'post', mineralData);
  }

  /**
   * Obtiene el historial de predicciones realizadas
   * @returns Lista de predicciones anteriores
   */
  async getPredictionHistory(): Promise<MineralPredictionResponse[]> {
    const url = `${API_URL}history/`;
    return this.makeRequest(url, true);
  }
}

export default new MineralService(); 