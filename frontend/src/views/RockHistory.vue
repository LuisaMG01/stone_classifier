<template>
  <div class="history-page">
    <div class="page-background"></div>
    <BContainer class="py-5 px-md-4">
      <div class="header-section text-center mb-5">
        <h1 class="display-4 mb-3 section-title fw-bold">Historial de Clasificación de Rocas</h1>
        <p class="lead text-secondary col-md-8 mx-auto">
          Consulta todas las clasificaciones de rocas realizadas anteriormente
        </p>
        <div class="accent-line mx-auto mt-4"></div>
      </div>
      
      <!-- Panel de carga -->
      <div v-if="isLoading" class="text-center my-5 loading-container">
        <div class="spinner-container mb-3">
          <BSpinner variant="primary" label="Cargando..." class="spinner-lg"></BSpinner>
        </div>
        <p class="text-secondary">Cargando historial de clasificaciones...</p>
      </div>
      
      <!-- Error de carga -->
      <BAlert 
        v-if="showError" 
        variant="danger" 
        dismissible 
        class="my-3 error-alert"
      >
        <div class="d-flex align-items-center">
          <BIcon icon="exclamation-triangle-fill" aria-hidden="true" class="me-2 flex-shrink-0"></BIcon>
          <div>{{ errorMessage }}</div>
        </div>
      </BAlert>
      
      <!-- Sin predicciones -->
      <div v-if="!isLoading && predictions.length === 0 && !showError" class="glass-card empty-state text-center my-5 p-5">
        <div class="empty-icon-container mb-4">
          <BIcon icon="calendar-x" class="empty-icon"></BIcon>
        </div>
        <h3 class="h3 mb-3 card-title">No hay clasificaciones registradas</h3>
        <p class="text-secondary mb-4">Aún no se han realizado clasificaciones de rocas</p>
        <BButton to="/classify-rocks" class="modern-button">
          <div class="d-flex align-items-center">
            <BIcon icon="plus-circle" class="me-2"></BIcon>
            <span>Realizar una clasificación</span>
          </div>
        </BButton>
      </div>
      
      <!-- Tabla de predicciones -->
      <div v-if="!isLoading && predictions.length > 0">
        <BCard class="glass-card history-card">
          <BCardBody class="p-4">
            <h2 class="h3 mb-4 card-title">Registros de Clasificación</h2>
            <div class="table-responsive">
              <BTable
                striped
                hover
                responsive
                :items="predictions"
                :fields="fields"
                sort-by="created_at"
                :sort-desc="true"
                class="history-table"
              >
                <!-- Columna de Clase de Roca -->
                <template #cell(predicted_class)="data">
                  <div class="group-pill">
                    {{ data.value }}
                  </div>
                </template>
                
                <!-- Columna de Confianza -->
                <template #cell(confidence)="data">
                  <div v-if="data.value !== null" class="confidence-pill">
                    {{ (data.value * 100).toFixed(1) }}%
                  </div>
                  <div v-else class="text-muted">
                    No disponible
                  </div>
                </template>
                
                <!-- Columna de Fecha -->
                <template #cell(created_at)="data">
                  <div class="date-display">
                    <BIcon icon="calendar-date" class="me-1 date-icon"></BIcon>
                    {{ formatDate(data.value) }}
                  </div>
                </template>
                
                <!-- Columna de Acciones -->
                <template #cell(actions)="data">
                  <BButton 
                    size="sm" 
                    class="action-button"
                    @click="showDetails(data.item)"
                  >
                    <BIcon icon="eye-fill" aria-hidden="true" class="me-1"></BIcon> 
                    <span>Ver</span>
                  </BButton>
                </template>
              </BTable>
            </div>
          </BCardBody>
        </BCard>
      </div>
    </BContainer>
    
    <!-- Modal de detalles -->
    <BModal 
      v-model="showModal" 
      title="Detalles de Clasificación"
      size="lg"
      centered
      header-class="modern-modal-header"
      body-class="p-0"
      content-class="modern-modal-content"
      footer-class="modern-modal-footer"
      hide-header-close
    >
      <template #modal-title>
        <div class="modal-custom-title">
          <BIcon icon="layers" class="modal-title-icon me-2"></BIcon>
          <span>Detalles de Clasificación</span>
        </div>
      </template>
      
      <div v-if="selectedPrediction" class="p-4">
        <div class="text-center mb-4">
          <!-- Imagen de la roca -->
          <div class="rock-image-container mb-4">
            <img :src="getImageUrl(selectedPrediction.image)" alt="Roca analizada" class="rock-result-image" />
          </div>
          
          <div class="prediction-badge-modal">
            <div class="rock-icon-container mb-2">
              <BIcon icon="layers" class="rock-icon"></BIcon>
            </div>
            <h3 class="prediction-title">{{ selectedPrediction.predicted_class }}</h3>
            <div class="prediction-subtitle">Tipo de Roca</div>
            
            <!-- Añadir la confianza de la predicción si está disponible -->
            <div v-if="selectedPrediction.confidence" class="confidence-badge mt-2">
              {{ Math.round(selectedPrediction.confidence * 100) }}% confianza
            </div>
          </div>
        </div>
        
        <div class="detail-table-container">
          <BTable 
            striped 
            hover 
            responsive
            :items="detailItems"
            :fields="detailFields"
            class="detail-table"
          ></BTable>
        </div>
      </div>
      
      <template #modal-footer>
        <BButton variant="secondary" class="modal-close-button" @click="showModal = false">
          <BIcon icon="x-circle" class="me-1"></BIcon>
          Cerrar
        </BButton>
      </template>
    </BModal>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import RockService from '@/services/RockService';
import type { RockPredictionResponse } from '@/shared/interfaces/rocks/RockResponseInterface';

export default defineComponent({
  name: 'RockHistoryView',
  
  setup() {
    const predictions = ref<RockPredictionResponse[]>([]);
    const isLoading = ref(true);
    const errorMessage = ref('');
    const showError = ref(false);
    const showModal = ref(false);
    const selectedPrediction = ref<RockPredictionResponse | null>(null);
    
    // URL base para las imágenes
    const API_BASE_URL = 'http://localhost:8000';
    
    // Función para construir URLs completas para imágenes
    const getImageUrl = (imagePath: string): string => {
      if (imagePath && (imagePath.startsWith('http://') || imagePath.startsWith('https://'))) {
        return imagePath;
      }
      
      if (imagePath && imagePath.startsWith('/')) {
        return `${API_BASE_URL}${imagePath}`;
      }
      
      return `${API_BASE_URL}/${imagePath}`;
    };
    
    // Definición de columnas para la tabla
    const fields = [
      { key: 'predicted_class', label: 'Tipo de Roca', sortable: true },
      { key: 'confidence', label: 'Confianza', sortable: true },
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
        { property: 'Tipo de Roca', value: selectedPrediction.value.predicted_class },
        { property: 'Confianza', value: selectedPrediction.value.confidence !== null ? `${(selectedPrediction.value.confidence * 100).toFixed(1)}%` : 'No disponible' },
        { property: 'Fecha de Clasificación', value: formatDate(selectedPrediction.value.created_at) }
      ];
    });
    
    // Formatear la fecha
    const formatDate = (dateString: string) => {
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    };
    
    // Mostrar detalles de una predicción
    const showDetails = (prediction: RockPredictionResponse) => {
      selectedPrediction.value = prediction;
      showModal.value = true;
    };
    
    // Cargar el historial de predicciones
    const loadPredictions = async () => {
      isLoading.value = true;
      errorMessage.value = '';
      showError.value = false;
      
      try {
        predictions.value = await RockService.getPredictionHistory();
      } catch (error) {
        errorMessage.value = error instanceof Error 
          ? error.message 
          : 'Ha ocurrido un error al cargar el historial de clasificaciones';
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
      showDetails,
      getImageUrl
    };
  }
});
</script>

<style scoped>
.history-page {
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
  background: radial-gradient(circle at top right, rgba(92, 48, 125, 0.05), transparent 70%),
              radial-gradient(circle at bottom left, rgba(149, 97, 226, 0.05), transparent 70%);
  z-index: -1;
}

.header-section {
  margin-bottom: 3rem;
}

.section-title {
  color: #5c307d; /* Morado para rocas */
  letter-spacing: -0.5px;
}

.accent-line {
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #5c307d, #9561e2);
  border-radius: 2px;
}

.card-title {
  color: #5c307d;
  font-weight: 600;
}

.loading-container {
  padding: 3rem;
}

.spinner-container {
  margin: 1.5rem 0;
}

.spinner-lg {
  width: 3rem;
  height: 3rem;
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

.history-card {
  border-top: 5px solid #5c307d;
}

.empty-state {
  max-width: 600px;
  margin: 3rem auto;
  padding: 3rem 2rem !important;
}

.empty-icon-container {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #5c307d 0%, #9561e2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  box-shadow: 0 8px 20px rgba(92, 48, 125, 0.2);
}

.empty-icon {
  font-size: 2.5rem;
  color: white;
}

.modern-button {
  background: linear-gradient(135deg, #5c307d 0%, #9561e2 100%);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(92, 48, 125, 0.2);
}

.modern-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(92, 48, 125, 0.3);
}

.modern-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(92, 48, 125, 0.3);
}

.history-table {
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
  border: 1px solid rgba(226, 232, 240, 0.7);
}

.history-table th {
  background-color: rgba(92, 48, 125, 0.05);
  color: #5c307d;
  font-weight: 600;
  border-bottom: 2px solid rgba(92, 48, 125, 0.1);
  padding: 12px 16px;
}

.history-table td {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
  color: #374151;
}

.group-pill {
  background: linear-gradient(135deg, #5c307d 0%, #9561e2 100%);
  color: white;
  border-radius: 20px;
  font-weight: 600;
  padding: 5px 12px;
  display: inline-block;
  box-shadow: 0 2px 6px rgba(92, 48, 125, 0.2);
  font-size: 0.85rem;
}

.confidence-pill {
  background-color: rgba(92, 48, 125, 0.1);
  color: #5c307d;
  border-radius: 20px;
  font-weight: 600;
  padding: 5px 12px;
  display: inline-block;
  font-size: 0.85rem;
}

.date-display {
  display: flex;
  align-items: center;
  color: #4b5563;
  font-size: 0.9rem;
}

.date-icon {
  color: #5c307d;
  opacity: 0.8;
}

.action-button {
  background-color: rgba(92, 48, 125, 0.1);
  color: #5c307d;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.action-button:hover {
  background-color: rgba(92, 48, 125, 0.15);
  transform: translateY(-1px);
}

.action-button:active {
  transform: translateY(0);
}

/* Modal de detalles */
.modern-modal-content {
  border-radius: 12px;
  overflow: hidden;
  border: none;
  box-shadow: 0 25px 50px rgba(15, 23, 42, 0.15);
}

.modern-modal-header {
  background-color: #5c307d;
  color: white;
  border-bottom: none;
  padding: 1.25rem 1.5rem;
}

.modal-custom-title {
  display: flex;
  align-items: center;
  font-weight: 600;
  font-size: 1.25rem;
}

.modal-title-icon {
  font-size: 1.2rem;
}

.modern-modal-footer {
  border-top: none;
  background-color: #f8fafc;
  padding: 1rem 1.5rem;
}

.modal-close-button {
  background-color: #e5e7eb;
  color: #4b5563;
  border: none;
  font-weight: 500;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.modal-close-button:hover {
  background-color: #d1d5db;
  color: #1f2937;
}

.prediction-badge-modal {
  background: linear-gradient(135deg, #5c307d 0%, #9561e2 100%);
  border-radius: 16px;
  padding: 25px 30px;
  display: inline-block;
  box-shadow: 0 10px 25px rgba(92, 48, 125, 0.2);
  color: white;
  width: 80%;
  max-width: 320px;
}

.rock-icon-container {
  background: rgba(255, 255, 255, 0.2);
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  backdrop-filter: blur(5px);
}

.rock-icon {
  font-size: 1.8rem;
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

.confidence-badge {
  background-color: rgba(255, 255, 255, 0.3);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  display: inline-block;
  backdrop-filter: blur(2px);
}

.detail-table-container {
  margin-top: 2rem;
}

.detail-table {
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
  border: 1px solid rgba(226, 232, 240, 0.7);
}

.detail-table th {
  background-color: rgba(92, 48, 125, 0.05);
  color: #5c307d;
  font-weight: 600;
  border-bottom: 2px solid rgba(92, 48, 125, 0.1);
  padding: 12px 16px;
}

.detail-table td {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
  color: #374151;
}

.error-alert {
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);
}

.rock-image-container {
  max-width: 100%;
  max-height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  overflow: hidden;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.1);
}

.rock-result-image {
  max-width: 100%;
  max-height: 200px;
  object-fit: contain;
}

/* Media queries */
@media (max-width: 768px) {
  .header-section h1 {
    font-size: 2rem;
  }
  
  .prediction-badge-modal {
    width: 90%;
    padding: 20px 15px;
  }
  
  .rock-icon-container {
    width: 50px;
    height: 50px;
  }
  
  .rock-icon {
    font-size: 1.5rem;
  }
  
  .group-pill {
    padding: 4px 8px;
    font-size: 0.8rem;
  }
  
  .action-button {
    padding: 0.4rem 0.8rem;
  }
}
</style> 