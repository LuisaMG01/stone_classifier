export interface MineralPredictionRequest {
  Element: string;
  Specific_Gravity: number;
  Calculated_Density: number;
  Refractive_Index?: number | undefined;
  Mohs_Hardness: number;
  Optical?: number | undefined;
}

export interface PredictionConfidence {
  probabilities: Array<[string, number]>;
  top_confidence: number;
}

export interface MineralPredictionResponse {
  id: number;
  element: string;
  specific_gravity: number;
  calculated_density: number;
  refractive_index: number | null;
  mohs_hardness: number;
  optical: number | null;
  predicted_group: string;
  created_at: string;
  prediction_confidence?: PredictionConfidence;
} 