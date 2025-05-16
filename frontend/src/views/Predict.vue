<template>
  <div class="predict-page">
    <BContainer class="py-5">
      <h1 class="text-center mb-4 section-title">Clasificación de Minerales</h1>
      <p class="text-center lead mb-5">
        Ingresa las propiedades físicas del mineral para determinar su grupo químico
      </p>
      
      <BRow>
        <BCol cols="12" lg="6" class="mb-4">
          <!-- Formulario de clasificación -->
          <BCard class="shadow-sm">
            <BCardBody>
              <h2 class="h4 mb-4">Propiedades del Mineral</h2>
              
              <BForm @submit.prevent="submitPrediction" ref="form">
                <!-- Elemento -->
                <BFormGroup
                  label="Elemento Principal:"
                  label-for="element-input"
                  description="Ingresa el símbolo químico del elemento principal (Si, Ca, Fe, etc.)"
                >
                  <BFormInput
                    id="element-input"
                    v-model="formData.Element"
                    placeholder="Ej: Si"
                    required
                    :state="validationState('Element')"
                  ></BFormInput>
                  <BFormInvalidFeedback>
                    El elemento es requerido
                  </BFormInvalidFeedback>
                </BFormGroup>
                
                <!-- Gravedad específica -->
                <BFormGroup
                  label="Gravedad Específica:"
                  label-for="specific-gravity-input"
                >
                  <BFormInput
                    id="specific-gravity-input"
                    v-model.number="formData.Specific_Gravity"
                    type="number"
                    step="0.01"
                    placeholder="Ej: 2.65"
                    required
                    :state="validationState('Specific_Gravity')"
                  ></BFormInput>
                  <BFormInvalidFeedback>
                    Ingrese un valor numérico válido
                  </BFormInvalidFeedback>
                </BFormGroup>
                
                <!-- Densidad calculada -->
                <BFormGroup
                  label="Densidad Calculada (g/cm³):"
                  label-for="density-input"
                >
                  <BFormInput
                    id="density-input"
                    v-model.number="formData.Calculated_Density"
                    type="number"
                    step="0.01"
                    placeholder="Ej: 2.65"
                    required
                    :state="validationState('Calculated_Density')"
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
                >
                  <BFormInput
                    id="refractive-input"
                    v-model.number="formData.Refractive_Index"
                    type="number"
                    step="0.01"
                    placeholder="Ej: 1.54"
                  ></BFormInput>
                </BFormGroup>
                
                <!-- Dureza de Mohs -->
                <BFormGroup
                  label="Dureza de Mohs:"
                  label-for="hardness-input"
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
                >
                  <BFormInput
                    id="optical-input"
                    v-model.number="formData.Optical"
                    type="number"
                    placeholder="Ej: 1"
                  ></BFormInput>
                </BFormGroup>
                
                <div class="d-grid gap-2 mt-4">
                  <BButton 
                    type="submit" 
                    variant="primary" 
                    size="lg"
                    :disabled="isLoading"
                  >
                    <BSpinner v-if="isLoading" small></BSpinner>
                    {{ isLoading ? 'Procesando...' : 'Clasificar Mineral' }}
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
            class="shadow-sm h-100 result-card"
            border-variant="primary"
          >
            <BCardBody>
              <h2 class="h4 mb-4 text-center">Resultado de la Clasificación</h2>
              
              <div class="text-center mb-4">
                <div class="prediction-badge">
                  <BIcon icon="gem" scale="2"></BIcon>
                  <h3 class="mt-3">{{ prediction.predicted_group }}</h3>
                </div>
              </div>
              
              <BTable 
                striped 
                hover 
                responsive
                :items="predictionItems"
                :fields="predictionFields"
              ></BTable>
            </BCardBody>
          </BCard>
          
          <div v-else class="h-100 d-flex flex-column justify-content-center align-items-center text-center info-panel">
            <BIcon icon="info-circle" scale="3" variant="primary" class="mb-3"></BIcon>
            <h3 class="h4 mb-3">Información de Clasificación</h3>
            <p class="lead">
              Completa el formulario con las propiedades del mineral para obtener la clasificación de su grupo químico.
            </p>
            <div class="tips-box mt-2">
              <h4 class="h5 mb-2">Consejos útiles:</h4>
              <ul class="text-start">
                <li>La gravedad específica es la relación entre la densidad del mineral y la del agua.</li>
                <li>La dureza de Mohs va de 1 (talco) a 10 (diamante).</li>
                <li>El índice de refracción mide cómo la luz se dobla al pasar por el mineral.</li>
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
        class="mt-3"
      >
        <BIcon icon="exclamation-triangle-fill" aria-hidden="true"></BIcon>
        {{ errorMessage }}
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
  background-color: #f8f9fa;
  min-height: calc(100vh - 60px - 100px); /* Considerando altura de navbar y footer */
}

.section-title {
  color: #1a4b8c;
  font-weight: bold;
}

.result-card {
  background-color: #f8f9fa;
  transition: transform 0.3s ease;
}

.prediction-badge {
  background: linear-gradient(135deg, #1a4b8c 0%, #2980b9 100%);
  color: white;
  border-radius: 10px;
  padding: 20px;
  display: inline-block;
  margin-bottom: 15px;
}

.tips-box {
  background-color: rgba(26, 75, 140, 0.1);
  border-radius: 8px;
  padding: 15px;
  margin-top: 20px;
}

.info-panel {
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
}
</style> 