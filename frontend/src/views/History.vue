<template>
  <div class="history-page">
    <BContainer class="py-5">
      <h1 class="text-center mb-4 section-title">Historial de Predicciones</h1>
      <p class="text-center lead mb-5">
        Consulta todas las predicciones realizadas anteriormente
      </p>
      
      <!-- Panel de carga -->
      <div v-if="isLoading" class="text-center my-5">
        <BSpinner variant="primary" label="Cargando..."></BSpinner>
        <p class="mt-3">Cargando historial de predicciones...</p>
      </div>
      
      <!-- Error de carga -->
      <BAlert 
        v-if="showError" 
        variant="danger" 
        dismissible 
        class="my-3"
      >
        <BIcon icon="exclamation-triangle-fill" aria-hidden="true"></BIcon>
        {{ errorMessage }}
      </BAlert>
      
      <!-- Sin predicciones -->
      <div v-if="!isLoading && predictions.length === 0 && !showError" class="text-center my-5 empty-state">
        <BIcon icon="calendar-x" scale="3" variant="secondary" class="mb-3"></BIcon>
        <h3 class="h4">No hay predicciones registradas</h3>
        <p class="mb-4">Aún no se han realizado predicciones de minerales</p>
        <BButton to="/predict" variant="primary">Realizar una predicción</BButton>
      </div>
      
      <!-- Tabla de predicciones -->
      <div v-if="!isLoading && predictions.length > 0">
        <BCard class="shadow-sm">
          <BCardBody>
            <BTable
              striped
              hover
              responsive
              :items="predictions"
              :fields="fields"
              sort-by="created_at"
              :sort-desc="true"
            >
              <!-- Columna de Elemento -->
              <template #cell(element)="data">
                <span class="font-weight-bold">{{ data.value }}</span>
              </template>
              
              <!-- Columna de Grupo Químico -->
              <template #cell(predicted_group)="data">
                <BPill variant="primary" class="group-pill">
                  {{ data.value }}
                </BPill>
              </template>
              
              <!-- Columna de Fecha -->
              <template #cell(created_at)="data">
                {{ formatDate(data.value) }}
              </template>
              
              <!-- Columna de Acciones -->
              <template #cell(actions)="data">
                <BButton 
                  size="sm" 
                  variant="outline-info"
                  @click="showDetails(data.item)"
                  class="me-2"
                >
                  <BIcon icon="eye-fill" aria-hidden="true"></BIcon> Ver
                </BButton>
              </template>
            </BTable>
          </BCardBody>
        </BCard>
      </div>
    </BContainer>
    
    <!-- Modal de detalles -->
    <BModal 
      v-model="showModal" 
      title="Detalles de Predicción"
      size="lg"
      centered
      header-bg-variant="light"
      footer-bg-variant="light"
    >
      <div v-if="selectedPrediction" class="p-2">
        <div class="text-center mb-4">
          <div class="prediction-badge-modal">
            <h3>{{ selectedPrediction.predicted_group }}</h3>
          </div>
        </div>
        
        <BTable 
          striped 
          hover 
          responsive
          :items="detailItems"
          :fields="detailFields"
        ></BTable>
      </div>
      
      <template #footer>
        <BButton variant="secondary" @click="showModal = false">
          Cerrar
        </BButton>
      </template>
    </BModal>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import MineralService from '@/services/MineralService';
import type { MineralPredictionResponse } from '@/shared/interfaces/minerals/MineralResponseInterface';

export default defineComponent({
  name: 'HistoryView',
  
  setup() {
    const predictions = ref<MineralPredictionResponse[]>([]);
    const isLoading = ref(true);
    const errorMessage = ref('');
    const showError = ref(false);
    const showModal = ref(false);
    const selectedPrediction = ref<MineralPredictionResponse | null>(null);
    
    // Definición de columnas para la tabla
    const fields = [
      { key: 'element', label: 'Elemento', sortable: true },
      { key: 'predicted_group', label: 'Grupo Químico', sortable: true },
      { key: 'specific_gravity', label: 'Gravedad Específica', sortable: true },
      { key: 'mohs_hardness', label: 'Dureza de Mohs', sortable: true },
      { key: 'created_at', label: 'Fecha', sortable: true },
      { key: 'actions', label: 'Acciones' }
    ];
    
    // Definición de columnas para la tabla de detalles
    const detailFields = [
      { key: 'property', label: 'Propiedad' },
      { key: 'value', label: 'Valor' }
    ];
    
    // Datos para la tabla de detalles
    const detailItems = computed(() => {
      if (!selectedPrediction.value) return [];
      
      return [
        { property: 'ID', value: selectedPrediction.value.id },
        { property: 'Grupo Químico', value: selectedPrediction.value.predicted_group },
        { property: 'Elemento', value: selectedPrediction.value.element },
        { property: 'Gravedad Específica', value: selectedPrediction.value.specific_gravity },
        { property: 'Densidad Calculada', value: selectedPrediction.value.calculated_density + ' g/cm³' },
        { property: 'Dureza de Mohs', value: selectedPrediction.value.mohs_hardness },
        { property: 'Índice de Refracción', value: selectedPrediction.value.refractive_index || 'No disponible' },
        { property: 'Propiedad Óptica', value: selectedPrediction.value.optical !== null ? selectedPrediction.value.optical : 'No disponible' },
        { property: 'Fecha de Predicción', value: formatDate(selectedPrediction.value.created_at) }
      ];
    });
    
    // Formatear la fecha
    const formatDate = (dateString: string) => {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    };
    
    // Mostrar detalles de una predicción
    const showDetails = (prediction: MineralPredictionResponse) => {
      selectedPrediction.value = prediction;
      showModal.value = true;
    };
    
    // Cargar el historial de predicciones
    const loadPredictions = async () => {
      isLoading.value = true;
      errorMessage.value = '';
      showError.value = false;
      
      try {
        predictions.value = await MineralService.getPredictionHistory();
      } catch (error) {
        errorMessage.value = error instanceof Error 
          ? error.message 
          : 'Ha ocurrido un error al cargar el historial de predicciones';
        showError.value = true;
      } finally {
        isLoading.value = false;
      }
    };
    
    // Cargar predicciones al montar el componente
    onMounted(() => {
      loadPredictions();
    });
    
    return {
      predictions,
      isLoading,
      errorMessage,
      showError,
      showModal,
      selectedPrediction,
      fields,
      detailFields,
      detailItems,
      formatDate,
      showDetails
    };
  }
});
</script>

<style scoped>
.history-page {
  background-color: #f8f9fa;
  min-height: calc(100vh - 60px - 100px); /* Considerando altura de navbar y footer */
}

.section-title {
  color: #1a4b8c;
  font-weight: bold;
}

.empty-state {
  padding: 40px;
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
}

.group-pill {
  background: linear-gradient(135deg, #1a4b8c 0%, #2980b9 100%) !important;
  font-weight: 600;
  padding: 5px 10px;
}

.prediction-badge-modal {
  background: linear-gradient(135deg, #1a4b8c 0%, #2980b9 100%);
  color: white;
  border-radius: 10px;
  padding: 15px 30px;
  display: inline-block;
  margin-bottom: 15px;
}
</style> 