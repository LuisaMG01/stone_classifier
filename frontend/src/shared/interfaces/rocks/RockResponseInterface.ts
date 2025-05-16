export interface RockPredictionResponse {
  id: number;
  image: string;
  predicted_class: string;
  confidence: number | null;
  created_at: string;
  prediction_probabilities?: {
    probabilities: [string, number][];
    top_confidence: number;
  };
} 