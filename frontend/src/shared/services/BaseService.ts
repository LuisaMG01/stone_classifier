import axios, { AxiosError } from 'axios';
import type { Method } from 'axios';
import JsonParserUtil from '@/shared/utils/JsonParserUtil';

export abstract class BaseService {
  protected async makeRequest(url: string, useJsonParser: boolean = false, method: Method = 'get', body?: unknown,
    headers?: Record<string, string>
  ): Promise<any> {
    try {
      const response = await axios({ url, method, data: body, headers });

      if (useJsonParser) {
        return JsonParserUtil.parse(response.data);
      }

      return response.data;
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
          throw new Error('El servidor no está disponible en este momento. Por favor, intenta más tarde.');
        }

        const backendMessage = error.response?.data?.message || error.message;
        throw new Error(backendMessage);
      } else {
        throw error;
      }
    }
  }
} 