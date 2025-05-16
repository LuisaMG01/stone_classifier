<template>
  <div class="predict-page">
    <div class="page-background"></div>
    <BContainer class="py-5 px-md-4">
      <div class="header-section text-center mb-5">
        <h1 class="display-4 mb-3 section-title fw-bold">Clasificación de Minerales</h1>
        <p class="lead text-secondary col-md-8 mx-auto">
          Ingresa las propiedades físicas del mineral para determinar su grupo químico
        </p>
        <div class="accent-line mx-auto mt-4"></div>
      </div>
      
      <BRow>
        <BCol cols="12" lg="6" class="mb-4">
          <!-- Formulario de clasificación -->
          <BCard class="glass-card form-card h-100">
            <BCardBody class="p-4">
              <h2 class="h3 mb-4 card-title">Propiedades del Mineral</h2>
              
              <BForm @submit.prevent="submitPrediction" ref="form">
                <!-- Elemento -->
                <BFormGroup
                  label="Elemento Principal:"
                  label-for="element-input"
                  description="Ingresa el símbolo químico del elemento principal (Si, Ca, Fe, etc.)"
                  class="mb-4"
                >
                  <BFormInput
                    id="element-input"
                    v-model="formData.Element"
                    placeholder="Ej: Si"
                    required
                    :state="validationState('Element')"
                    class="modern-input"
                  ></BFormInput>
                  <BFormInvalidFeedback>
                    El elemento es requerido
                  </BFormInvalidFeedback>
                </BFormGroup>
                
                <!-- Gravedad específica -->
                <BFormGroup
                  label="Gravedad Específica:"
                  label-for="specific-gravity-input"
                  class="mb-4"
                >
                  <BFormInput
                    id="specific-gravity-input"
                    v-model.number="formData.Specific_Gravity"
                    type="number"
                    step="0.01"
                    placeholder="Ej: 2.65"
                    required
                    :state="validationState('Specific_Gravity')"
                    class="modern-input"
                  ></BFormInput>
                  <BFormInvalidFeedback>
                    Ingrese un valor numérico válido
                  </BFormInvalidFeedback>
                </BFormGroup>
                
                <!-- Densidad calculada -->
                <BFormGroup
                  label="Densidad Calculada (g/cm³):"
                  label-for="density-input"
                  class="mb-4"
                >
                  <BFormInput
                    id="density-input"
                    v-model.number="formData.Calculated_Density"
                    type="number"
                    step="0.01"
                    placeholder="Ej: 2.65"
                    required
                    :state="validationState('Calculated_Density')"
                    class="modern-input"
                  ></BFormInput>
                  <BFormInvalidFeedback>
                    Ingrese un valor numérico válido
                  </BFormInvalidFeedback>
                </BFormGroup>
                
                <!-- Índice de refracción -->
                <BFormGroup
                  label="Índice de Refracción:"
                  label-for="refractive-input"
                  description="Opcional"
                  class="mb-4"
                >
                  <BFormInput
                    id="refractive-input"
                    v-model.number="formData.Refractive_Index"
                    type="number"
                    step="0.01"
                    placeholder="Ej: 1.54"
                    class="modern-input"
                  ></BFormInput>
                </BFormGroup>
                
                <!-- Dureza de Mohs -->
                <BFormGroup
                  label="Dureza de Mohs:"
                  label-for="hardness-input"
                  class="mb-4"
                >
                  <BFormInput
                    id="hardness-input"
                    v-model.number="formData.Mohs_Hardness"
                    type="number"
                    step="0.1"
                    min="1"
                    max="10"
                    placeholder="Ej: 7"
                    required
                    :state="validationState('Mohs_Hardness')"
                    class="modern-input"
                  ></BFormInput>
                  <BFormInvalidFeedback>
                    Ingrese un valor entre 1 y 10
                  </BFormInvalidFeedback>
                </BFormGroup>
                
                <!-- Propiedad óptica -->
                <BFormGroup
                  label="Propiedad Óptica:"
                  label-for="optical-input"
                  description="Opcional"
                  class="mb-4"
                >
                  <BFormInput
                    id="optical-input"
                    v-model.number="formData.Optical"
                    type="number"
                    placeholder="Ej: 1"
                    class="modern-input"
                  ></BFormInput>
                </BFormGroup>
                
                <div class="d-grid gap-2 mt-5">
                  <BButton 
                    type="submit" 
                    class="modern-button"
                    size="lg"
                    :disabled="isLoading"
                  >
                    <div class="d-flex align-items-center justify-content-center">
                      <BSpinner v-if="isLoading" small class="me-2"></BSpinner>
                      <span>{{ isLoading ? 'Procesando...' : 'Clasificar Mineral' }}</span>
                    </div>
                  </BButton>
                </div>
              </BForm>
            </BCardBody>
          </BCard>
        </BCol>
        
        <BCol cols="12" lg="6" class="mb-4">
          <!-- Resultado de la clasificación -->
          <BCard 
            v-if="prediction" 
            class="glass-card result-card h-100"
          >
            <BCardBody class="p-4">
              <h2 class="h3 mb-4 text-center card-title">Resultado de la Clasificación</h2>
              
              <div class="text-center mb-4">
                <div class="prediction-badge">
                  <div class="gem-icon-container">
                    <BIcon icon="gem" class="gem-icon"></BIcon>
                  </div>
                  <h3 class="mt-3 prediction-title">{{ prediction.predicted_group }}</h3>
                  <div class="prediction-subtitle">Grupo Químico</div>
                </div>
              </div>
              
              <div class="result-table-container">
                <BTable 
                  striped 
                  hover 
                  responsive
                  :items="predictionItems"
                  :fields="predictionFields"
                  class="result-table"
                ></BTable>
              </div>
            </BCardBody>
          </BCard>
          
          <div v-else class="glass-card h-100 d-flex flex-column justify-content-center align-items-center text-center info-panel p-4">
            <div class="info-icon-container mb-4">
              <BIcon icon="info-circle" class="info-icon"></BIcon>
            </div>
            <h3 class="h3 mb-3 card-title">Instrucciones</h3>
            <p class="text-secondary mb-4">
              Completa el formulario con las propiedades del mineral para obtener la clasificación de su grupo químico.
            </p>
            <div class="tips-box mt-2">
              <h4 class="h5 mb-3">Consejos útiles:</h4>
              <ul class="text-start tip-list">
                <li>La <strong>gravedad específica</strong> es la relación entre la densidad del mineral y la del agua.</li>
                <li>La <strong>dureza de Mohs</strong> va de 1 (talco) a 10 (diamante).</li>
                <li>El <strong>índice de refracción</strong> mide cómo la luz se dobla al pasar por el mineral.</li>
              </ul>
            </div>
          </div>
        </BCol>
      </BRow>
      
      <!-- Error mensaje -->
      <BAlert 
        v-model="showError" 
        variant="danger" 
        dismissible 
        class="mt-3 error-alert"
      >
        <div class="d-flex align-items-center">
          <BIcon icon="exclamation-triangle-fill" aria-hidden="true" class="me-2 flex-shrink-0"></BIcon>
          <div>{{ errorMessage }}</div>
        </div>
      </BAlert>
    </BContainer>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import MineralService from '@/services/MineralService';
import type { MineralPredictionRequest, MineralPredictionResponse } from '@/shared/interfaces/minerals/MineralResponseInterface';

export default defineComponent({
  name: 'ClassifyView',
  
  setup() {
    // Estado del formulario
    const formData = ref<MineralPredictionRequest>({
      Element: '',
      Specific_Gravity: null as unknown as number,
      Calculated_Density: null as unknown as number,
      Refractive_Index: undefined,
      Mohs_Hardness: null as unknown as number,
      Optical: undefined
    });
    
    // Estado para los validadores
    const validationErrors = ref<Record<string, boolean>>({});
    
    // Estado para la respuesta
    const prediction = ref<MineralPredictionResponse | null>(null);
    const isLoading = ref(false);
    const errorMessage = ref('');
    const showError = ref(false);
    
    // Validación
    const validateForm = (): boolean => {
      validationErrors.value = {};
      let isValid = true;
      
      if (!formData.value.Element || formData.value.Element.trim() === '') {
        validationErrors.value.Element = true;
        isValid = false;
      }
      
      if (!formData.value.Specific_Gravity || isNaN(formData.value.Specific_Gravity)) {
        validationErrors.value.Specific_Gravity = true;
        isValid = false;
      }
      
      if (!formData.value.Calculated_Density || isNaN(formData.value.Calculated_Density)) {
        validationErrors.value.Calculated_Density = true;
        isValid = false;
      }
      
      if (!formData.value.Mohs_Hardness || isNaN(formData.value.Mohs_Hardness) || 
          formData.value.Mohs_Hardness < 1 || formData.value.Mohs_Hardness > 10) {
        validationErrors.value.Mohs_Hardness = true;
        isValid = false;
      }
      
      return isValid;
    };
    
    const validationState = (field: string) => {
      return validationErrors.value[field] === undefined ? null : !validationErrors.value[field];
    };
    
    // Envío del formulario
    const submitPrediction = async () => {
      if (!validateForm()) return;
      
      isLoading.value = true;
      errorMessage.value = '';
      showError.value = false;
      
      try {
        prediction.value = await MineralService.predictMineral(formData.value);
      } catch (error) {
        errorMessage.value = error instanceof Error 
          ? error.message 
          : 'Ha ocurrido un error al procesar la solicitud';
        showError.value = true;
        prediction.value = null;
      } finally {
        isLoading.value = false;
      }
    };
    
    // Campos para la tabla de resultados
    const predictionFields = [
      { key: 'property', label: 'Propiedad' },
      { key: 'value', label: 'Valor' }
    ];
    
    // Datos para la tabla de resultados
    const predictionItems = computed(() => {
      if (!prediction.value) return [];
      
      return [
        { property: 'Grupo Químico', value: prediction.value.predicted_group },
        { property: 'Elemento', value: prediction.value.element },
        { property: 'Gravedad Específica', value: prediction.value.specific_gravity },
        { property: 'Densidad Calculada', value: prediction.value.calculated_density + ' g/cm³' },
        { property: 'Dureza de Mohs', value: prediction.value.mohs_hardness },
        { property: 'Índice de Refracción', value: prediction.value.refractive_index || 'No disponible' },
        { property: 'Propiedad Óptica', value: prediction.value.optical !== null ? prediction.value.optical : 'No disponible' },
        { property: 'Fecha de Clasificación', value: new Date(prediction.value.created_at).toLocaleDateString() }
      ];
    });
    
    return {
      formData,
      prediction,
      isLoading,
      errorMessage,
      showError,
      validationState,
      submitPrediction,
      predictionFields,
      predictionItems
    };
  }
});
</script>

<style scoped>
.predict-page {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

.page-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at top right, rgba(26, 75, 140, 0.05), transparent 70%),
              radial-gradient(circle at bottom left, rgba(52, 152, 219, 0.05), transparent 70%);
  z-index: -1;
}

.header-section {
  margin-bottom: 3rem;
}

.section-title {
  color: var(--primary-color);
  letter-spacing: -0.5px;
}

.accent-line {
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #1a4b8c, #52a5e0);
  border-radius: 2px;
}

.card-title {
  color: var(--primary-color);
  font-weight: 600;
}

.glass-card {
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 8px 32px rgba(15, 23, 42, 0.08);
  border-radius: 12px;
  border: 1px solid rgba(226, 232, 240, 0.7);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 40px rgba(15, 23, 42, 0.12);
}

.form-card {
  border-top: 5px solid var(--primary-color);
}

.modern-input {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  background-color: rgba(255, 255, 255, 0.8);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.modern-input:focus {
  border-color: var(--primary-light);
  box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.15);
}

.modern-button {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(26, 75, 140, 0.2);
}

.modern-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(26, 75, 140, 0.3);
}

.modern-button:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(26, 75, 140, 0.3);
}

.modern-button:disabled {
  background: linear-gradient(135deg, #6c757d 0%, #adb5bd 100%);
  cursor: not-allowed;
}

.result-card {
  border-top: 5px solid var(--primary-light);
}

.prediction-badge {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  border-radius: 16px;
  padding: 30px 20px;
  display: inline-block;
  box-shadow: 0 10px 25px rgba(26, 75, 140, 0.2);
  color: white;
  width: 80%;
  max-width: 320px;
}

.gem-icon-container {
  background: rgba(255, 255, 255, 0.2);
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  backdrop-filter: blur(5px);
}

.gem-icon {
  font-size: 2rem;
  color: white;
}

.prediction-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 5px;
}

.prediction-subtitle {
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 500;
}

.result-table-container {
  margin-top: 2rem;
}

.result-table {
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
  border: 1px solid rgba(226, 232, 240, 0.7);
}

.result-table th {
  background-color: rgba(26, 75, 140, 0.05);
  color: var(--primary-color);
  font-weight: 600;
  border-bottom: 2px solid rgba(26, 75, 140, 0.1);
  padding: 12px 16px;
}

.result-table td {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
  color: #374151;
}

.info-panel {
  padding: 40px 20px;
}

.info-icon-container {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  box-shadow: 0 6px 16px rgba(26, 75, 140, 0.2);
}

.info-icon {
  font-size: 2rem;
  color: white;
}

.tips-box {
  background-color: rgba(26, 75, 140, 0.05);
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid var(--primary-color);
  text-align: left;
  margin: 0 auto;
  max-width: 90%;
}

.tip-list {
  list-style-type: none;
  padding-left: 0;
}

.tip-list li {
  position: relative;
  padding-left: 25px;
  margin-bottom: 12px;
  line-height: 1.5;
}

.tip-list li:before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
}

.error-alert {
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);
}

@media (max-width: 992px) {
  .prediction-badge {
    width: 90%;
  }
  
  .tips-box {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .header-section h1 {
    font-size: 2rem;
  }
  
  .glass-card {
    padding: 10px;
  }
  
  .prediction-badge {
    padding: 20px 15px;
  }
  
  .gem-icon-container, .info-icon-container {
    width: 60px;
    height: 60px;
  }
  
  .gem-icon, .info-icon {
    font-size: 1.5rem;
  }
}
</style> 