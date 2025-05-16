<template>
  <div class="model-analysis-page">
    <div class="page-background"></div>
    
    <!-- Modal de carga -->
    <div v-if="isLoading" class="loading-modal">
      <div class="loading-modal-content">
        <div class="loading-animation">
          <BSpinner variant="primary" label="Cargando..." class="loading-spinner"></BSpinner>
          <svg class="loading-circle" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="40" />
          </svg>
        </div>
        <h3 class="mt-4 loading-title">Cargando datos del modelo</h3>
        <p class="text-secondary loading-subtitle">Preparando visualizaciones y métricas...</p>
      </div>
    </div>
    
    <BContainer fluid class="py-5 px-md-5">
      <div class="header-section text-center mb-5">
        <h1 class="display-4 mb-3 section-title fw-bold">Análisis del Modelo</h1>
        <p class="lead text-secondary col-md-8 mx-auto">
          Exploración visual del modelo de clasificación de minerales y sus métricas de rendimiento
        </p>
        <div class="accent-line mx-auto mt-4"></div>
      </div>
      
      <!-- Tabs de navegación -->
      <div class="tabs-container">
        <BTabs pills card vertical content-class="mt-0" class="mb-5 analysis-tabs">
          <!-- Tab de distribución de clases -->
          <BTab title="Distribución de Grupos" active>
            <BCard class="glass-card mb-4">
              <BCardBody class="p-4">
                <h2 class="h3 mb-4 card-title">Distribución de Grupos Químicos</h2>
                <p class="text-secondary mb-4">
                  Este gráfico muestra la distribución de minerales por grupo químico en el conjunto de datos.
                </p>
                <div class="chart-container" style="position: relative; height: 450px;">
                  <canvas ref="classDistributionChart"></canvas>
                </div>
              </BCardBody>
            </BCard>
          </BTab>
          
          <!-- Tab de matriz de confusión -->
          <BTab title="Matriz de Confusión">
            <BCard class="glass-card mb-4">
              <BCardBody class="p-4">
                <h2 class="h3 mb-4 card-title">Matriz de Confusión</h2>
                <p class="text-secondary mb-4">
                  Muestra la precisión de clasificación del modelo para cada grupo químico.
                  Cada celda representa el número de minerales clasificados en una categoría vs. su grupo real.
                </p>
                <div class="chart-container confusion-matrix-container">
                  <canvas ref="confusionMatrixChart"></canvas>
                </div>
                <div class="mt-4 insight-box">
                  <p><strong>Interpretación:</strong> Los valores diagonales representan clasificaciones correctas. Valores fuera de la diagonal son clasificaciones incorrectas.</p>
                </div>
              </BCardBody>
            </BCard>
          </BTab>
          
          <!-- Tab de importancia de características -->
          <BTab title="Importancia de Características">
            <BCard class="glass-card mb-4">
              <BCardBody class="p-4">
                <h2 class="h3 mb-4 card-title">Importancia de Características</h2>
                <p class="text-secondary mb-4">
                  Este gráfico muestra qué propiedades físicas tienen mayor influencia en la clasificación de minerales.
                </p>
                <div class="chart-container" style="position: relative; height: 450px;">
                  <canvas ref="featureImportanceChart"></canvas>
                </div>
                <div class="mt-4 insight-box">
                  <p><strong>Interpretación:</strong> Valores más altos indican características que el modelo considera más relevantes para la clasificación.</p>
                </div>
              </BCardBody>
            </BCard>
          </BTab>
          
          <!-- Tab de visualización PCA -->
          <BTab title="Visualización PCA">
            <BCard class="glass-card mb-4">
              <BCardBody class="p-4">
                <h2 class="h3 mb-4 card-title">Análisis de Componentes Principales (PCA)</h2>
                <p class="text-secondary mb-4">
                  Visualización de minerales en un espacio bidimensional, donde minerales similares aparecen cercanos entre sí.
                </p>
                <div class="chart-container" style="position: relative; height: 500px;">
                  <canvas ref="pcaChart"></canvas>
                </div>
                <div class="mt-4 insight-box">
                  <p><strong>Interpretación:</strong> PCA reduce las dimensiones del conjunto de datos, permitiendo visualizar cómo se agrupan los minerales basados en sus propiedades.</p>
                  <p class="mb-0 badge-variance">Varianza explicada: <span class="badge bg-primary">{{ pcaVarianceExplained }}%</span></p>
                </div>
              </BCardBody>
            </BCard>
          </BTab>
          
          <!-- Tab de curvas ROC -->
          <BTab title="Curvas ROC">
            <BCard class="glass-card mb-4">
              <BCardBody class="p-4">
                <h2 class="h3 mb-4 card-title">Curvas ROC por Grupo Químico</h2>
                <p class="text-secondary mb-4">
                  Visualización de la capacidad del modelo para distinguir entre diferentes grupos químicos.
                  Las curvas ROC muestran la relación entre tasa de verdaderos positivos (sensibilidad) y tasa de falsos positivos.
                </p>
                <div class="chart-container" style="position: relative; height: 450px;">
                  <canvas ref="rocCurvesChart"></canvas>
                </div>
                <div class="mt-4 insight-box">
                  <p><strong>Interpretación:</strong> Cuanto más cerca esté la curva ROC de la esquina superior izquierda, mejor es el rendimiento del modelo para esa clase. El valor AUC (Área Bajo la Curva) cuantifica este rendimiento, donde 1.0 representa una clasificación perfecta.</p>
                </div>
              </BCardBody>
            </BCard>
          </BTab>
          
          <!-- Tab de métricas del modelo -->
          <BTab title="Métricas de Rendimiento">
            <BCard class="glass-card mb-4">
              <BCardBody class="p-4">
                <h2 class="h3 mb-4 card-title">Métricas de Rendimiento del Modelo</h2>
                <p class="text-secondary mb-4">
                  Estadísticas detalladas sobre el rendimiento del modelo para cada grupo químico.
                </p>
                
                <div v-if="modelStats" class="metrics-container">
                  <h3 class="h5 mt-4 mb-3">Rendimiento Global</h3>
                  <BTable striped hover class="global-metrics-table" :items="globalMetricsItems" :fields="globalMetricsFields"></BTable>
                  
                  <h3 class="h5 mt-5 mb-3">Rendimiento por Grupo Químico</h3>
                  <div class="table-responsive">
                    <BTable striped hover responsive class="class-metrics-table" :items="classMetricsItems" :fields="classMetricsFields"></BTable>
                  </div>
                </div>
                
                <div v-else class="text-center py-5">
                  <div class="spinner-container">
                    <BSpinner variant="primary" class="spinner-lg"></BSpinner>
                  </div>
                  <p class="mt-3 text-secondary">Cargando métricas...</p>
                </div>
                
                <div class="mt-4 insight-box">
                  <p class="mb-2"><strong>Interpretación:</strong></p>
                  <div class="metrics-explanation">
                    <div class="metric-item">
                      <div class="metric-icon precision-icon">P</div>
                      <div class="metric-text">
                        <strong>Precisión (Precision):</strong> Porcentaje de minerales clasificados correctamente en un grupo específico.
                      </div>
                    </div>
                    <div class="metric-item">
                      <div class="metric-icon recall-icon">R</div>
                      <div class="metric-text">
                        <strong>Sensibilidad (Recall):</strong> Porcentaje de minerales de un grupo que fueron identificados correctamente.
                      </div>
                    </div>
                    <div class="metric-item">
                      <div class="metric-icon f1-icon">F1</div>
                      <div class="metric-text">
                        <strong>Puntuación F1:</strong> Media armónica entre precisión y sensibilidad.
                      </div>
                    </div>
                    <div class="metric-item">
                      <div class="metric-icon support-icon">S</div>
                      <div class="metric-text">
                        <strong>Soporte:</strong> Número de minerales en el conjunto de datos para cada grupo.
                      </div>
                    </div>
                  </div>
                </div>
              </BCardBody>
            </BCard>
          </BTab>
        </BTabs>
      </div>
      
      <!-- Mensaje de error -->
      <BAlert v-model="showError" variant="danger" dismissible class="mt-3 error-alert">
        <div class="d-flex align-items-center">
          <BIcon icon="exclamation-triangle-fill" aria-hidden="true" class="me-2 flex-shrink-0"></BIcon>
          <div>{{ errorMessage }}</div>
        </div>
      </BAlert>
    </BContainer>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import Chart from 'chart.js/auto';
import ModelMetricsService from '@/services/ModelMetricsService';

// Definir interfaces para los tipos de datos
interface MetricsData {
  [key: string]: any;
}

interface ModelStats {
  accuracy: number;
  macro_avg?: {
    precision?: number;
    recall?: number;
    f1_score?: number;
    support?: number;
  };
  weighted_avg?: {
    precision?: number;
    recall?: number;
    f1_score?: number;
    support?: number;
  };
  [key: string]: any;
}

export default defineComponent({
  name: 'ModelAnalysisView',
  
  setup() {
    // Referencias para los gráficos
    const classDistributionChart = ref<HTMLCanvasElement | null>(null);
    const confusionMatrixChart = ref<HTMLCanvasElement | null>(null);
    const featureImportanceChart = ref<HTMLCanvasElement | null>(null);
    const pcaChart = ref<HTMLCanvasElement | null>(null);
    const rocCurvesChart = ref<HTMLCanvasElement | null>(null);
    
    // Estado para los datos
    const classDistribution = ref<MetricsData | null>(null);
    const confusionMatrix = ref<MetricsData | null>(null);
    const featureImportance = ref<MetricsData | null>(null);
    const pcaData = ref<MetricsData | null>(null);
    const modelStats = ref<ModelStats | null>(null);
    const rocCurvesData = ref<MetricsData | null>(null);
    
    // Estado para errores y carga
    const errorMessage = ref('');
    const showError = ref(false);
    const isLoading = ref(true);
    
    // Gráficos instanciados
    const charts = ref<{[key: string]: Chart | null}>({
      classDistribution: null,
      confusionMatrix: null,
      featureImportance: null,
      pca: null,
      rocCurves: null
    });
    
    // Varianza explicada del PCA
    const pcaVarianceExplained = computed(() => {
      if (pcaData.value && pcaData.value.variance_explained) {
        const total = pcaData.value.variance_explained.reduce((a: number, b: number) => a + b, 0);
        return (total * 100).toFixed(2);
      }
      return 'N/A';
    });
    
    // Métricas globales para la tabla
    const globalMetricsFields = [
      { key: 'metric', label: 'Métrica' },
      { key: 'value', label: 'Valor' }
    ];
    
    const globalMetricsItems = computed(() => {
      if (!modelStats.value || !modelStats.value.accuracy) return [];
      
      // Para depuración, registrar el objeto completo
      console.log("ModelStats completo:", JSON.stringify(modelStats.value));
      
      // Acceder a macro avg y weighted avg usando notación de corchetes debido a los espacios
      const macroAvg = modelStats.value["macro avg"] || {};
      const weightedAvg = modelStats.value["weighted avg"] || {};
      
      console.log("MacroAvg accedido con corchetes:", macroAvg);
      console.log("WeightedAvg accedido con corchetes:", weightedAvg);
      
      // Mostrar todas las claves disponibles en macroAvg y weightedAvg
      console.log("Claves en macroAvg:", Object.keys(macroAvg));
      console.log("Claves en weightedAvg:", Object.keys(weightedAvg));
      
      // Acceder explícitamente a todos los posibles nombres de propiedades
      const macroF1 = macroAvg.f1_score || (macroAvg as any)["f1-score"];
      const weightedPrecision = weightedAvg.precision;
      const weightedRecall = weightedAvg.recall;
      
      console.log("Valores exactos:");
      console.log("- macroF1:", macroF1);
      console.log("- weightedPrecision:", weightedPrecision);
      console.log("- weightedRecall:", weightedRecall);
      
      // Forzar visualización de valores exactos
      return [
        { metric: 'Precisión Global', value: (modelStats.value.accuracy * 100).toFixed(2) + '%' },
        { metric: 'Macro F1-Score', value: macroF1 ? `${(macroF1 * 100).toFixed(2)}%` : `N/A` },
        { metric: 'Precisión Ponderada', value: weightedPrecision ? `${(weightedPrecision * 100).toFixed(2)}%` : `N/A` },
        { metric: 'Sensibilidad Ponderada', value: weightedRecall ? `${(weightedRecall * 100).toFixed(2)}%` : `N/A` }
      ];
    });
    
    // Métricas por clase para la tabla
    const classMetricsFields = [
      { key: 'class', label: 'Grupo Químico' },
      { key: 'precision', label: 'Precisión' },
      { key: 'recall', label: 'Sensibilidad' },
      { key: 'f1_score', label: 'F1-Score' },
      { key: 'support', label: 'Soporte' }
    ];
    
    const classMetricsItems = computed(() => {
      if (!modelStats.value) return [];
      
      const items = [];
      
      for (const [className, metrics] of Object.entries(modelStats.value)) {
        if (['accuracy', 'macro_avg', 'weighted_avg'].includes(className)) continue;
        if (!metrics || typeof metrics !== 'object') continue;
        
        // Validar que las métricas tengan las propiedades necesarias
        items.push({
          class: className,
          precision: (metrics.precision !== undefined ? (metrics.precision * 100).toFixed(2) : 'N/A') + '%',
          recall: (metrics.recall !== undefined ? (metrics.recall * 100).toFixed(2) : 'N/A') + '%',
          f1_score: (metrics.f1_score !== undefined ? (metrics.f1_score * 100).toFixed(2) : 'N/A') + '%',
          support: metrics.support || 'N/A'
        });
      }
      
      return items;
    });
    
    // Cargar datos y crear gráficos
    const loadData = async () => {
      isLoading.value = true;
      
      try {
        // Obtener todos los datos en paralelo
        const [
          classDistributionData,
          confusionMatrixData,
          featureImportanceData,
          pcaVisualizationData,
          modelStatsData,
          rocCurvesResponse
        ] = await Promise.all([
          ModelMetricsService.getClassDistribution(),
          ModelMetricsService.getConfusionMatrix(),
          ModelMetricsService.getFeatureImportance(),
          ModelMetricsService.getPCAVisualization(),
          ModelMetricsService.getModelStats(),
          ModelMetricsService.getROCCurves()
        ]);
        
        // Guardar los datos
        classDistribution.value = classDistributionData;
        confusionMatrix.value = confusionMatrixData;
        featureImportance.value = featureImportanceData;
        pcaData.value = pcaVisualizationData;
        modelStats.value = modelStatsData;
        rocCurvesData.value = rocCurvesResponse;
        
        // Crear los gráficos una vez que tenemos los datos
        createCharts();
        
      } catch (error) {
        errorMessage.value = error instanceof Error 
          ? error.message 
          : 'Ha ocurrido un error al cargar los datos del modelo';
        showError.value = true;
      } finally {
        // Pequeño retraso para asegurar que las gráficas se hayan renderizado
        setTimeout(() => {
          isLoading.value = false;
        }, 800);
      }
    };
    
    // Crear los gráficos
    const createCharts = () => {
      // Limpiar gráficos existentes
      Object.values(charts.value).forEach(chart => {
        if (chart) chart.destroy();
      });
      
      // 1. Gráfico de distribución de clases
      if (classDistributionChart.value && classDistribution.value) {
        const ctx = classDistributionChart.value.getContext('2d');
        if (ctx) {
          charts.value.classDistribution = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: classDistribution.value.classes,
              datasets: [{
                label: 'Número de Minerales',
                data: classDistribution.value.counts,
                backgroundColor: generateColors(classDistribution.value.classes.length),
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: false
                },
                tooltip: {
                  callbacks: {
                    label: (context: any) => {
                      return `Minerales: ${context.raw}`;
                    }
                  }
                }
              },
              scales: {
                y: {
                  beginAtZero: true,
                  title: {
                    display: true,
                    text: 'Número de Minerales'
                  }
                },
                x: {
                  title: {
                    display: true,
                    text: 'Grupo Químico'
                  }
                }
              }
            }
          });
        }
      }
      
      // 2. Gráfico de matriz de confusión (usando scatter en lugar de bubble/matrix)
      if (confusionMatrixChart.value && confusionMatrix.value) {
        const ctx = confusionMatrixChart.value.getContext('2d');
        if (ctx) {
          const classes = confusionMatrix.value.classes;
          const matrix = confusionMatrix.value.normalized_matrix;
          
          console.log("Matrix de confusión:", matrix);
          
          // Preparar múltiples datasets, uno por fila de la matriz
          const datasets = [];
          
          for (let i = 0; i < classes.length; i++) {
            const rowData = [];
            for (let j = 0; j < classes.length; j++) {
              // Verificar si el valor es casi 1 (100%)
              let value = matrix[i][j];
              // Si es un número muy cercano a 1 (por error de redondeo), lo ajustamos
              if (value > 0.99 && value < 1.00001) {
                value = 1.0;
              }
              
              // Usar posiciones numéricas para evitar problemas con las categorías
              rowData.push({
                x: j,
                y: i,
                r: Math.max(5, value * 30), // Radio proporcional al valor
                v: value,  // Valor real para el tooltip
                raw: confusionMatrix.value.matrix[i][j] // Valor absoluto para el tooltip
              });
            }
            
            datasets.push({
              label: classes[i],
              data: rowData,
              backgroundColor: (context: any) => {
                // Color más intenso para valores más altos
                const value = context.raw.v || 0;
                // Escala de azules con intensidad según el valor
                if (value > 0.75) {
                  return `rgba(26, 75, 140, ${0.7 + value * 0.3})`;  // Azul oscuro para valores altos
                } else if (value > 0.5) {
                  return `rgba(41, 128, 185, ${0.5 + value * 0.5})`;  // Azul medio
                } else if (value > 0.25) {
                  return `rgba(52, 152, 219, ${0.4 + value * 0.6})`;  // Azul claro
                } else if (value > 0) {
                  return `rgba(133, 193, 233, ${0.3 + value * 0.7})`;  // Azul muy claro
                } else {
                  return `rgba(214, 234, 248, 0.3)`;  // Casi blanco para cero
                }
              },
              pointRadius: (context: any) => {
                // Tamaño de punto proporcional al valor
                const value = context.raw.v || 0;
                return Math.max(5, value * 25);
              },
              pointStyle: 'circle',
              hoverBackgroundColor: (context: any) => {
                // Color de hover más saturado
                const value = context.raw.v || 0;
                return `rgba(41, 128, 185, ${0.8 + value * 0.2})`;
              },
              hoverRadius: (context: any) => {
                // Tamaño de hover ligeramente mayor
                const value = context.raw.v || 0;
                return Math.max(7, value * 28);
              }
            });
          }
          
          charts.value.confusionMatrix = new Chart(ctx, {
            type: 'scatter',
            data: {
              datasets
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                tooltip: {
                  callbacks: {
                    title: (context: any) => {
                      return `Predicho: ${classes[context[0].raw.x]}, Real: ${classes[context[0].raw.y]}`;
                    },
                    label: (context: any) => {
                      const value = context.raw.v;
                      const rawValue = context.raw.raw || 0;
                      return [
                        `Precisión: ${(value * 100).toFixed(1)}%`,
                        `Cantidad: ${rawValue} muestras`
                      ];
                    }
                  }
                },
                legend: {
                  display: false
                }
              },
              scales: {
                x: {
                  type: 'linear',
                  position: 'bottom',
                  min: -0.5,
                  max: classes.length - 0.5,
                  ticks: {
                    callback: function(value: any) {
                      // Truncar nombres largos
                      const label = classes[value];
                      return label ? (label.length > 12 ? label.slice(0, 10) + '...' : label) : '';
                    },
                    stepSize: 1,
                    font: {
                      weight: 'bold'
                    },
                    color: '#1a4b8c'
                  },
                  title: {
                    display: true,
                    text: 'Grupo Predicho',
                    font: {
                      weight: 'bold',
                      size: 14
                    },
                    color: '#1a4b8c'
                  },
                  grid: {
                    display: true,
                    drawOnChartArea: true,
                    color: 'rgba(200, 200, 200, 0.3)'
                  }
                },
                y: {
                  type: 'linear',
                  min: -0.5,
                  max: classes.length - 0.5,
                  ticks: {
                    callback: function(value: any) {
                      // Truncar nombres largos
                      const label = classes[value];
                      return label ? (label.length > 12 ? label.slice(0, 10) + '...' : label) : '';
                    },
                    stepSize: 1,
                    font: {
                      weight: 'bold'
                    },
                    color: '#1a4b8c'
                  },
                  title: {
                    display: true,
                    text: 'Grupo Real',
                    font: {
                      weight: 'bold',
                      size: 14
                    },
                    color: '#1a4b8c'
                  },
                  grid: {
                    display: true,
                    drawOnChartArea: true,
                    color: 'rgba(200, 200, 200, 0.3)'
                  }
                }
              }
            }
          });
        }
      }
      
      // 3. Gráfico de importancia de características
      if (featureImportanceChart.value && featureImportance.value) {
        const ctx = featureImportanceChart.value.getContext('2d');
        if (ctx) {
          // Ordenar datos por importancia
          const features = [...featureImportance.value.features];
          const importances = [...featureImportance.value.importance_values];
          
          const combinedData = features.map((feature, index) => ({
            feature,
            importance: importances[index]
          }));
          
          combinedData.sort((a, b) => b.importance - a.importance);
          
          const sortedFeatures = combinedData.map(item => item.feature);
          const sortedImportances = combinedData.map(item => item.importance);
          
          charts.value.featureImportance = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: sortedFeatures,
              datasets: [{
                label: 'Importancia',
                data: sortedImportances,
                backgroundColor: 'rgba(41, 128, 185, 0.8)',
                borderColor: 'rgba(41, 128, 185, 1)',
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
                      return `Importancia: ${(context.raw as number * 100).toFixed(2)}%`;
                    }
                  }
                }
              },
              scales: {
                x: {
                  beginAtZero: true,
                  title: {
                    display: true,
                    text: 'Importancia Relativa'
                  }
                }
              }
            }
          });
        }
      }
      
      // 4. Gráfico PCA
      if (pcaChart.value && pcaData.value) {
        const ctx = pcaChart.value.getContext('2d');
        if (ctx) {
          const uniqueLabels = pcaData.value.unique_labels;
          const colors = generateColors(uniqueLabels.length);
          
          // Crear datasets para cada clase
          const datasets = uniqueLabels.map((label: string, labelIndex: number) => {
            const points = pcaData.value ? pcaData.value.points : [];
            const labels = pcaData.value ? pcaData.value.labels : [];
            
            // Filtrar puntos de esta clase
            const classPoints = points.filter((_: any, i: number) => labels[i] === label);
            
            return {
              label,
              data: classPoints.map((p: number[]) => ({ x: p[0], y: p[1] })),
              backgroundColor: colors[labelIndex],
              pointRadius: 5
            };
          });
          
          charts.value.pca = new Chart(ctx, {
            type: 'scatter',
            data: {
              datasets
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                tooltip: {
                  callbacks: {
                    label: (context: any) => {
                      return `${context?.dataset?.label || ''}`;
                    }
                  }
                }
              },
              scales: {
                x: {
                  title: {
                    display: true,
                    text: 'Componente Principal 1'
                  }
                },
                y: {
                  title: {
                    display: true,
                    text: 'Componente Principal 2'
                  }
                }
              }
            }
          });
        }
      }
      
      // 5. Gráfico de curvas ROC
      if (rocCurvesChart.value && rocCurvesData.value) {
        const ctx = rocCurvesChart.value.getContext('2d');
        if (ctx) {
          // Preparar datasets para el gráfico de líneas
          const datasets = [];
          
          // Línea de referencia (diagonal)
          datasets.push({
            label: 'Referencia',
            data: [
              { x: 0, y: 0 },
              { x: 1, y: 1 }
            ],
            borderColor: 'rgba(200, 200, 200, 0.7)',
            borderDash: [5, 5],
            borderWidth: 2,
            pointRadius: 0,
            fill: false
          });
          
          // Líneas para cada clase
          const colors = generateColors(rocCurvesData.value.roc_curves.length);
          
          rocCurvesData.value.roc_curves.forEach((curve: any, i: number) => {
            const points = curve.fpr.map((fpr: number, j: number) => ({
              x: fpr,
              y: curve.tpr[j]
            }));
            
            datasets.push({
              label: `${curve.class} (AUC = ${curve.auc.toFixed(2)})`,
              data: points,
              borderColor: colors[i],
              backgroundColor: colors[i].replace('0.8', '0.1'),
              borderWidth: 2,
              pointRadius: 0,
              pointHoverRadius: 5,
              fill: false,
              tension: 0.1
            });
          });
          
          charts.value.rocCurves = new Chart(ctx, {
            type: 'line',
            data: {
              datasets
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                tooltip: {
                  callbacks: {
                    label: (context: any) => {
                      const dataIndex = context.datasetIndex;
                      
                      if (dataIndex === 0) {
                        return 'Referencia';
                      }
                      
                      const label = context.dataset.label || '';
                      const x = context.raw.x.toFixed(2);
                      const y = context.raw.y.toFixed(2);
                      
                      return [
                        label,
                        `FPR: ${x}`,
                        `TPR: ${y}`
                      ];
                    }
                  }
                },
                legend: {
                  position: 'top'
                }
              },
              scales: {
                x: {
                  type: 'linear',
                  title: {
                    display: true,
                    text: 'Tasa de Falsos Positivos (1 - Especificidad)',
                    font: {
                      weight: 'bold',
                      size: 13
                    }
                  },
                  min: 0,
                  max: 1
                },
                y: {
                  type: 'linear',
                  title: {
                    display: true,
                    text: 'Tasa de Verdaderos Positivos (Sensibilidad)',
                    font: {
                      weight: 'bold',
                      size: 13
                    }
                  },
                  min: 0,
                  max: 1
                }
              }
            }
          });
        }
      }
    };
    
    // Generar colores para los gráficos
    const generateColors = (count: number) => {
      const baseColors = [
        'rgba(26, 75, 140, 0.8)',
        'rgba(41, 128, 185, 0.8)',
        'rgba(155, 89, 182, 0.8)',
        'rgba(52, 152, 219, 0.8)',
        'rgba(22, 160, 133, 0.8)',
        'rgba(39, 174, 96, 0.8)',
        'rgba(241, 196, 15, 0.8)',
        'rgba(230, 126, 34, 0.8)',
        'rgba(231, 76, 60, 0.8)',
        'rgba(149, 165, 166, 0.8)'
      ];
      
      // Si necesitamos más colores, generamos tonos intermedios
      if (count <= baseColors.length) {
        return baseColors.slice(0, count);
      } else {
        const colors = [...baseColors];
        while (colors.length < count) {
          const r = Math.floor(Math.random() * 255);
          const g = Math.floor(Math.random() * 255);
          const b = Math.floor(Math.random() * 255);
          colors.push(`rgba(${r}, ${g}, ${b}, 0.8)`);
        }
        return colors;
      }
    };
    
    // Cargar datos al montar el componente
    onMounted(() => {
      // Cargar datos
      loadData();
    });
    
    return {
      classDistributionChart,
      confusionMatrixChart,
      featureImportanceChart,
      pcaChart,
      rocCurvesChart,
      errorMessage,
      showError,
      isLoading,
      pcaVarianceExplained,
      modelStats,
      globalMetricsFields,
      globalMetricsItems,
      classMetricsFields,
      classMetricsItems
    };
  }
});
</script>

<style scoped>
.model-analysis-page {
  background-color: #f8fafc;
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
  color: #1a4b8c;
  letter-spacing: -0.5px;
}

.accent-line {
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #1a4b8c, #52a5e0);
  border-radius: 2px;
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

.card-title {
  color: #1a4b8c;
  font-weight: 600;
  position: relative;
}

.chart-container {
  margin: 20px 0;
  border-radius: 8px;
  padding: 16px;
  background: #ffffff;
  box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.05);
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.confusion-matrix-container {
  min-height: 550px;
  padding: 24px;
}

.insight-box {
  background-color: rgba(243, 244, 246, 0.7);
  border-left: 4px solid #1a4b8c;
  padding: 15px;
  border-radius: 0 8px 8px 0;
  font-size: 0.9rem;
}

.badge-variance {
  display: flex;
  align-items: center;
  gap: 8px;
}

.badge-variance .badge {
  font-size: 0.85rem;
  padding: 6px 10px;
  border-radius: 20px;
  background: linear-gradient(to right, #1a4b8c, #3498db);
  font-weight: 500;
}

/* Estilos para las tabs */
:deep(.analysis-tabs) {
  gap: 20px;
}

:deep(.card-header) {
  border-radius: 10px !important;
  background-color: transparent !important;
  border-bottom: none !important;
}

:deep(.tab-content) {
  padding-left: 20px;
  flex: 1;
}

:deep(.nav-pills) {
  border-radius: 10px;
  background: #fff;
  padding: 15px 10px;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
  border: 1px solid rgba(226, 232, 240, 0.7);
}

:deep(.nav-pills .nav-link) {
  color: #64748b;
  border-radius: 8px;
  margin: 5px 0;
  transition: all 0.2s ease;
  font-weight: 500;
  padding: 12px 15px;
}

:deep(.nav-pills .nav-link:hover:not(.active)) {
  background-color: rgba(226, 232, 240, 0.5);
  color: #1a4b8c;
}

:deep(.nav-pills .nav-link.active) {
  background: linear-gradient(to right, #1a4b8c, #3498db);
  box-shadow: 0 4px 12px rgba(26, 75, 140, 0.2);
  color: white;
  font-weight: 600;
}

/* Estilos para las tablas */
:deep(.table) {
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
  border: 1px solid rgba(226, 232, 240, 0.7);
}

:deep(.table thead th) {
  background-color: rgba(26, 75, 140, 0.05);
  color: #1a4b8c;
  font-weight: 600;
  border-bottom: 2px solid rgba(26, 75, 140, 0.1);
  padding: 12px 16px;
}

:deep(.table tbody td) {
  padding: 12px 16px;
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
  color: #374151;
}

:deep(.table tbody tr:last-child td) {
  border-bottom: none;
}

/* Estilos para los indicadores de métricas */
.metrics-explanation {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  margin-top: 10px;
}

.metric-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.metric-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  color: white;
  flex-shrink: 0;
}

.precision-icon {
  background: linear-gradient(to right, #1a4b8c, #3498db);
}

.recall-icon {
  background: linear-gradient(to right, #2980b9, #3498db);
}

.f1-icon {
  background: linear-gradient(to right, #3498db, #52a5e0);
}

.support-icon {
  background: linear-gradient(to right, #52a5e0, #85c1e9);
}

.metric-text {
  font-size: 0.9rem;
  color: #4b5563;
}

/* Estilos para el spinner */
.spinner-container {
  margin: 30px 0;
}

.spinner-lg {
  width: 3rem;
  height: 3rem;
}

/* Estilos para alerta de error */
.error-alert {
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);
}

/* Media queries para responsividad */
@media (max-width: 992px) {
  :deep(.tab-content) {
    padding-left: 0;
    margin-top: 20px;
  }
  
  .metrics-explanation {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-section {
    margin-bottom: 2rem;
  }
  
  .header-section h1 {
    font-size: 2rem;
  }
  
  .chart-container {
    padding: 10px;
  }
  
  .confusion-matrix-container {
    min-height: 450px;
    padding: 12px;
  }
}

/* Estilos para el modal de carga */
.loading-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-modal-content {
  text-align: center;
  padding: 2rem;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(15, 23, 42, 0.1);
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.loading-animation {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto;
}

.loading-spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 3rem;
  height: 3rem;
}

.loading-circle {
  width: 100%;
  height: 100%;
  animation: rotate 2s linear infinite;
}

.loading-circle circle {
  fill: none;
  stroke: #1a4b8c;
  stroke-width: 3;
  stroke-dasharray: 150, 200;
  stroke-dashoffset: 0;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
  opacity: 0.7;
}

.loading-title {
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.loading-subtitle {
  font-size: 0.95rem;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 200;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 200;
    stroke-dashoffset: -125;
  }
}
</style> 