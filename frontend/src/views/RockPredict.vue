<template>
  <div class="predict-page">
    <div class="page-background"></div>
    <BContainer class="py-5 px-md-4">
      <div class="header-section text-center mb-5">
        <h1 class="display-4 mb-3 section-title fw-bold">Clasificación de Rocas</h1>
        <p class="lead text-secondary col-md-8 mx-auto">
          Sube una imagen clara de la roca para determinar su tipo
        </p>
        <div class="accent-line mx-auto mt-4"></div>
      </div>
      
      <BRow>
        <BCol cols="12" lg="6" class="mb-4">
          <!-- Formulario de clasificación de rocas -->
          <BCard class="glass-card form-card h-100">
            <BCardBody class="p-4">
              <h2 class="h3 mb-4 card-title">Subir Imagen de Roca</h2>
              
              <BForm @submit.prevent="submitPrediction" ref="form" enctype="multipart/form-data">
                <!-- Campo para subir imagen -->
                <div class="upload-container mb-4">
                  <div 
                    class="drop-zone p-3" 
                    :class="{ 'has-image': imageUrl, 'is-dragover': isDragover }"
                    @dragover.prevent="isDragover = true"
                    @dragleave="isDragover = false"
                    @drop.prevent="onDrop"
                    @click="triggerFileInput"
                  >
                    <div v-if="!imageUrl" class="text-center py-5">
                      <BIcon icon="cloud-arrow-up" class="upload-icon mb-3"></BIcon>
                      <h4 class="h5">Arrastra una imagen o haz clic aquí</h4>
                      <p class="text-secondary small">Formatos aceptados: JPG, PNG, JPEG (Máx: 5MB)</p>
                    </div>
                    <div v-else class="preview-container">
                      <img :src="imageUrl" alt="Preview" class="img-preview" />
                      <button type="button" class="remove-btn" @click.stop="removeImage">
                        <BIcon icon="x-circle-fill"></BIcon>
                      </button>
                    </div>
                  </div>
                  <input 
                    type="file" 
                    ref="fileInput" 
                    class="d-none" 
                    accept=".jpg,.jpeg,.png"
                    @change="onFileSelected"
                  />
                </div>
                
                <div v-if="fileError" class="invalid-feedback d-block mb-3">
                  {{ fileError }}
                </div>
                
                <div class="d-grid gap-2 mt-5">
                  <BButton 
                    type="submit" 
                    class="modern-button"
                    size="lg"
                    :disabled="isLoading || !imageFile"
                  >
                    <div class="d-flex align-items-center justify-content-center">
                      <BSpinner v-if="isLoading" small class="me-2"></BSpinner>
                      <span>{{ isLoading ? 'Procesando...' : 'Clasificar Roca' }}</span>
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
                  <div class="rock-icon-container">
                    <BIcon icon="layers" class="rock-icon"></BIcon>
                  </div>
                  <h3 class="mt-3 prediction-title">{{ prediction.predicted_class }}</h3>
                  <div class="prediction-subtitle">Tipo de Roca</div>
                  
                  <!-- Añadir la confianza de la predicción si está disponible -->
                  <div v-if="prediction.confidence" class="confidence-badge mt-2">
                    {{ Math.round(prediction.confidence * 100) }}% confianza
                  </div>
                </div>
              </div>
              
              <!-- Gráfico de probabilidades -->
              <div v-if="prediction.prediction_probabilities" class="confidence-chart-container mb-4">
                <h4 class="h5 mb-3 text-center">Probabilidades por Tipo</h4>
                <div class="chart-container" style="position: relative; height: 200px;">
                  <canvas ref="confidenceChart"></canvas>
                </div>
              </div>
              
              <div class="result-details mt-4">
                <h4 class="h5 mb-3">Detalles de la predicción:</h4>
                <p class="text-secondary">
                  La imagen se clasificó como <strong>{{ prediction.predicted_class }}</strong> 
                  {{ prediction.confidence ? `con una confianza del ${Math.round(prediction.confidence * 100)}%` : '' }}.
                </p>
                <p class="text-secondary small">Fecha: {{ formatDate(prediction.created_at) }}</p>
              </div>
            </BCardBody>
          </BCard>
          
          <div v-else class="glass-card h-100 d-flex flex-column justify-content-center align-items-center text-center info-panel p-4">
            <div class="info-icon-container mb-4">
              <BIcon icon="info-circle" class="info-icon"></BIcon>
            </div>
            <h3 class="h3 mb-3 card-title">Instrucciones</h3>
            <p class="text-secondary mb-4">
              Sube una imagen clara de la roca para que nuestro modelo de clasificación pueda identificar su tipo.
            </p>
            <div class="tips-box mt-2">
              <h4 class="h5 mb-3">Consejos útiles:</h4>
              <ul class="text-start tip-list">
                <li>Toma la foto con <strong>buena iluminación</strong> (preferiblemente luz natural).</li>
                <li>Asegúrate que la roca esté <strong>centrada</strong> en la imagen.</li>
                <li>Evita fondos con muchos detalles o distracciones.</li>
                <li>Incluye una referencia de escala si es posible.</li>
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
import { defineComponent, ref, nextTick } from 'vue';
import RockService from '@/services/RockService';
import type { RockPredictionResponse } from '@/shared/interfaces/rocks/RockResponseInterface';
import Chart from 'chart.js/auto';

export default defineComponent({
  name: 'RockClassifyView',
  
  setup() {
    // Estado para la imagen
    const fileInput = ref<HTMLInputElement | null>(null);
    const imageFile = ref<File | null>(null);
    const imageUrl = ref<string | null>(null);
    const isDragover = ref(false);
    const fileError = ref('');
    
    // Estado para la respuesta
    const prediction = ref<RockPredictionResponse | null>(null);
    const isLoading = ref(false);
    const errorMessage = ref('');
    const showError = ref(false);
    
    // Referencia al canvas para el gráfico
    const confidenceChart = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;
    
    // Añadir esto en la sección de script, dentro del método setup()
    const API_BASE_URL = 'http://localhost:8000';

    const getImageUrl = (imagePath: string): string => {
      // Si ya es una URL completa, la devolvemos tal cual
      if (imagePath && (imagePath.startsWith('http://') || imagePath.startsWith('https://'))) {
        return imagePath;
      }
      
      // Si es una ruta relativa, construimos la URL completa
      if (imagePath && imagePath.startsWith('/')) {
        return `${API_BASE_URL}${imagePath}`;
      }
      
      // Si no tiene un slash inicial, asumimos que necesita uno
      return `${API_BASE_URL}/${imagePath}`;
    };
    
    // Métodos para manejar la subida de archivos
    const triggerFileInput = () => {
      if (fileInput.value) {
        fileInput.value.click();
      }
    };
    
    const validateFile = (file: File): boolean => {
      // Validar tipo de archivo
      const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
      if (!validTypes.includes(file.type)) {
        fileError.value = 'Formato no válido. Por favor, sube una imagen JPG o PNG.';
        return false;
      }
      
      // Validar tamaño (max 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        fileError.value = 'La imagen es demasiado grande. El tamaño máximo es 5MB.';
        return false;
      }
      
      fileError.value = '';
      return true;
    };
    
    const onFileSelected = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files && input.files.length > 0) {
        const file = input.files[0];
        
        if (validateFile(file)) {
          imageFile.value = file;
          imageUrl.value = URL.createObjectURL(file);
        } else {
          removeImage();
        }
      }
    };
    
    const onDrop = (event: DragEvent) => {
      isDragover.value = false;
      
      if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
        const file = event.dataTransfer.files[0];
        
        if (validateFile(file)) {
          imageFile.value = file;
          imageUrl.value = URL.createObjectURL(file);
        }
      }
    };
    
    const removeImage = () => {
      if (imageUrl.value) {
        URL.revokeObjectURL(imageUrl.value);
      }
      imageFile.value = null;
      imageUrl.value = null;
      if (fileInput.value) {
        fileInput.value.value = '';
      }
    };
    
    // Envío del formulario
    const submitPrediction = async () => {
      if (!imageFile.value) {
        fileError.value = 'Por favor, selecciona una imagen antes de continuar.';
        return;
      }
      
      isLoading.value = true;
      errorMessage.value = '';
      showError.value = false;
      
      // Destruir el gráfico existente si hay uno
      if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
      }
      
      try {
        const formData = new FormData();
        formData.append('image', imageFile.value);
        
        prediction.value = await RockService.predictRock(formData);
        
        // Crear el gráfico de confianza si hay datos disponibles
        nextTick(() => {
          createConfidenceChart();
        });
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
    
    // Crear el gráfico de confianza
    const createConfidenceChart = () => {
      if (!confidenceChart.value || !prediction.value?.prediction_probabilities) return;
      
      const ctx = confidenceChart.value.getContext('2d');
      if (!ctx) return;
      
      // Destruir el gráfico existente si hay uno
      if (chartInstance) {
        chartInstance.destroy();
      }
      
      // Ordenar las probabilidades de mayor a menor
      const probabilities = prediction.value.prediction_probabilities.probabilities;
      
      // Extraer etiquetas y valores
      const labels = probabilities.map((item: [string, number]) => item[0]);
      const values = probabilities.map((item: [string, number]) => item[1] * 100); // Convertir a porcentaje
      
      // Generar colores para las barras
      const colors = generateClassColors(labels);
      
      // Crear el gráfico
      chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Confianza (%)',
            data: values,
            backgroundColor: colors,
            borderColor: colors.map(c => c.replace('0.7', '1')),
            borderWidth: 1
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: (context: any) => {
                  return `Confianza: ${context.raw.toFixed(1)}%`;
                }
              }
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              max: 100,
              title: {
                display: true,
                text: 'Confianza (%)'
              }
            },
            y: {
              ticks: {
                font: {
                  weight: (context: any) => {
                    // Destacar la clase predicha
                    return labels[context.index] === prediction.value?.predicted_class ? 'bold' : 'normal';
                  }
                }
              }
            }
          }
        }
      });
    };
    
    // Generar colores para cada tipo de roca
    const generateClassColors = (classes: string[]) => {
      // Usar un color destacado para la clase predicha
      return classes.map(rockClass => {
        if (rockClass === prediction.value?.predicted_class) {
          return 'rgba(92, 48, 125, 0.7)';  // Color primario para la clase predicha (tono morado)
        } else {
          return 'rgba(149, 97, 226, 0.7)';  // Color secundario para otras clases (morado más claro)
        }
      });
    };
    
    // Formatear fecha
    const formatDate = (dateString: string): string => {
      return new Date(dateString).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    return {
      fileInput,
      imageFile,
      imageUrl,
      isDragover,
      fileError,
      prediction,
      isLoading,
      errorMessage,
      showError,
      confidenceChart,
      triggerFileInput,
      onFileSelected,
      onDrop,
      removeImage,
      submitPrediction,
      formatDate,
      getImageUrl
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
  background: radial-gradient(circle at top right, rgba(92, 48, 125, 0.05), transparent 70%),
              radial-gradient(circle at bottom left, rgba(149, 97, 226, 0.05), transparent 70%);
  z-index: -1;
}

.header-section {
  margin-bottom: 3rem;
}

.section-title {
  color: #5c307d; /* Morado más oscuro para el título */
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
  border-top: 5px solid #5c307d;
}

.drop-zone {
  border: 2px dashed #d1d5db;
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  transition: border-color 0.3s ease, background-color 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.drop-zone:hover {
  border-color: #9561e2;
  background-color: rgba(149, 97, 226, 0.05);
}

.drop-zone.is-dragover {
  border-color: #5c307d;
  background-color: rgba(149, 97, 226, 0.1);
}

.drop-zone.has-image {
  border-style: solid;
  border-color: #9561e2;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 0 !important;
}

.upload-icon {
  font-size: 2.5rem;
  color: #9561e2;
}

.preview-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.img-preview {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: contain;
  border-radius: 8px;
  display: block;
}

.remove-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  border: none;
  padding: 5px;
  font-size: 1.2rem;
  color: #ef4444;
  cursor: pointer;
  transition: transform 0.2s ease, background-color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.remove-btn:hover {
  transform: scale(1.1);
  background-color: rgba(255, 255, 255, 1);
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

.modern-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(92, 48, 125, 0.3);
}

.modern-button:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(92, 48, 125, 0.3);
}

.modern-button:disabled {
  background: linear-gradient(135deg, #6c757d 0%, #adb5bd 100%);
  cursor: not-allowed;
}

.result-card {
  border-top: 5px solid #9561e2;
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

.prediction-badge {
  background: linear-gradient(135deg, #5c307d 0%, #9561e2 100%);
  border-radius: 16px;
  padding: 30px 20px;
  display: inline-block;
  box-shadow: 0 10px 25px rgba(92, 48, 125, 0.2);
  color: white;
  width: 80%;
  max-width: 320px;
}

.rock-icon-container {
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

.rock-icon {
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

.info-panel {
  padding: 40px 20px;
}

.info-icon-container {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #5c307d 0%, #9561e2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  box-shadow: 0 6px 16px rgba(92, 48, 125, 0.2);
}

.info-icon {
  font-size: 2rem;
  color: white;
}

.tips-box {
  background-color: rgba(92, 48, 125, 0.05);
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid #5c307d;
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
  background: linear-gradient(135deg, #5c307d 0%, #9561e2 100%);
}

.error-alert {
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);
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

.confidence-chart-container {
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  padding: 16px;
  box-shadow: 0 3px 10px rgba(15, 23, 42, 0.06);
  border: 1px solid rgba(226, 232, 240, 0.7);
}

.chart-container {
  margin: 10px 0;
}

.result-details {
  background-color: rgba(92, 48, 125, 0.05);
  border-radius: 10px;
  padding: 20px;
  border-left: 4px solid #9561e2;
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
  
  .rock-icon-container, .info-icon-container {
    width: 60px;
    height: 60px;
  }
  
  .rock-icon, .info-icon {
    font-size: 1.5rem;
  }
}
</style> 