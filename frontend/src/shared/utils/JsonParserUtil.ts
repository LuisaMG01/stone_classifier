/**
 * Utilidad para el parseo seguro de JSON
 */
export default class JsonParserUtil {
  /**
   * Analiza los datos JSON con manejo seguro
   * @param data Datos a analizar
   * @returns Objeto parseado
   */
  static parse(data: any): any {
    if (typeof data === 'string') {
      try {
        return JSON.parse(data);
      } catch (e) {
        console.error('Error al parsear JSON:', e);
        return data;
      }
    }
    return data;
  }
} 