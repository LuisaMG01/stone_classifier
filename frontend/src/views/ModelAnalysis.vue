<template>
  <div class="model-analysis-page">
    <BContainer class="py-5">
      <h1 class="text-center mb-4 section-title">Análisis del Modelo</h1>
      <p class="text-center lead mb-5">
        Exploración visual del modelo de clasificación de minerales y sus métricas de rendimiento
      </p>
      
      <!-- Tabs de navegación -->
      <BTabs pills card vertical content-class="mt-3" class="mb-5">
        <!-- Tab de distribución de clases -->
        <BTab title="Distribución de Grupos" active>
          <BCard class="shadow-sm mb-4">
            <BCardBody>
              <h2 class="h4 mb-4">Distribución de Grupos Químicos</h2>
              <p class="text-muted">
                Este gráfico muestra la distribución de minerales por grupo químico en el conjunto de datos.
              </p>
              <div class="chart-container" style="position: relative; height: 400px;">
                <canvas ref="classDistributionChart"></canvas>
              </div>
            </BCardBody>
          </BCard>
        </BTab>
        
        <!-- Tab de matriz de confusión -->
        <BTab title="Matriz de Confusión">
          <BCard class="shadow-sm mb-4">
            <BCardBody>
              <h2 class="h4 mb-4">Matriz de Confusión</h2>
              <p class="text-muted">
                Muestra la precisión de clasificación del modelo para cada grupo químico.
                Cada celda representa el número de minerales clasificados en una categoría vs. su grupo real.
              </p>
              <div class="chart-container" style="position: relative; min-height: 500px;">
                <canvas ref="confusionMatrixChart"></canvas>
              </div>
              <div class="mt-4 small">
                <p><strong>Interpretación:</strong> Los valores diagonales representan clasificaciones correctas. Valores fuera de la diagonal son clasificaciones incorrectas.</p>
              </div>
            </BCardBody>
          </BCard>
        </BTab>
        
        <!-- Tab de importancia de características -->
        <BTab title="Importancia de Características">
          <BCard class="shadow-sm mb-4">
            <BCardBody>
              <h2 class="h4 mb-4">Importancia de Características</h2>
              <p class="text-muted">
                Este gráfico muestra qué propiedades físicas tienen mayor influencia en la clasificación de minerales.
              </p>
              <div class="chart-container" style="position: relative; height: 400px;">
                <canvas ref="featureImportanceChart"></canvas>
              </div>
              <div class="mt-4 small">
                <p><strong>Interpretación:</strong> Valores más altos indican características que el modelo considera más relevantes para la clasificación.</p>
              </div>
            </BCardBody>
          </BCard>
        </BTab>
        
        <!-- Tab de visualización PCA -->
        <BTab title="Visualización PCA">
          <BCard class="shadow-sm mb-4">
            <BCardBody>
              <h2 class="h4 mb-4">Análisis de Componentes Principales (PCA)</h2>
              <p class="text-muted">
                Visualización de minerales en un espacio bidimensional, donde minerales similares aparecen cercanos entre sí.
              </p>
              <div class="chart-container" style="position: relative; height: 500px;">
                <canvas ref="pcaChart"></canvas>
              </div>
              <div class="mt-4 small">
                <p><strong>Interpretación:</strong> PCA reduce las dimensiones del conjunto de datos, permitiendo visualizar cómo se agrupan los minerales basados en sus propiedades.</p>
                <p>Varianza explicada: {{ pcaVarianceExplained }}%</p>
              </div>
            </BCardBody>
          </BCard>
        </BTab>
        
        <!-- Tab de métricas del modelo -->
        <BTab title="Métricas de Rendimiento">
          <BCard class="shadow-sm mb-4">
            <BCardBody>
              <h2 class="h4 mb-4">Métricas de Rendimiento del Modelo</h2>
              <p class="text-muted">
                Estadísticas detalladas sobre el rendimiento del modelo para cada grupo químico.
              </p>
              
              <div v-if="modelStats">
                <h3 class="h5 mt-4">Rendimiento Global</h3>
                <BTable striped hover :items="globalMetricsItems" :fields="globalMetricsFields"></BTable>
                
                <h3 class="h5 mt-4">Rendimiento por Grupo Químico</h3>
                <BTable striped hover responsive :items="classMetricsItems" :fields="classMetricsFields"></BTable>
              </div>
              
              <div v-else class="text-center py-4">
                <BSpinner variant="primary"></BSpinner>
                <p class="mt-2">Cargando métricas...</p>
              </div>
              
              <div class="mt-4 small">
                <p><strong>Interpretación:</strong></p>
                <ul>
                  <li><strong>Precisión (Precision):</strong> Porcentaje de minerales clasificados correctamente en un grupo específico.</li>
                  <li><strong>Sensibilidad (Recall):</strong> Porcentaje de minerales de un grupo que fueron identificados correctamente.</li>
                  <li><strong>Puntuación F1:</strong> Media armónica entre precisión y sensibilidad.</li>
                  <li><strong>Soporte:</strong> Número de minerales en el conjunto de datos para cada grupo.</li>
                </ul>
              </div>
            </BCardBody>
          </BCard>
        </BTab>
      </BTabs>
      
      <!-- Mensaje de error -->
      <BAlert v-model="showError" variant="danger" dismissible class="mt-3">
        <BIcon icon="exclamation-triangle-fill" aria-hidden="true"></BIcon>
        {{ errorMessage }}
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
    
    // Estado para los datos
    const classDistribution = ref<MetricsData | null>(null);
    const confusionMatrix = ref<MetricsData | null>(null);
    const featureImportance = ref<MetricsData | null>(null);
    const pcaData = ref<MetricsData | null>(null);
    const modelStats = ref<ModelStats | null>(null);
    
    // Estado para errores
    const errorMessage = ref('');
    const showError = ref(false);
    
    // Gráficos instanciados
    const charts = ref<{[key: string]: Chart | null}>({
      classDistribution: null,
      confusionMatrix: null,
      featureImportance: null,
      pca: null
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
      try {
        // Obtener todos los datos en paralelo
        const [
          classDistributionData,
          confusionMatrixData,
          featureImportanceData,
          pcaVisualizationData,
          modelStatsData
        ] = await Promise.all([
          ModelMetricsService.getClassDistribution(),
          ModelMetricsService.getConfusionMatrix(),
          ModelMetricsService.getFeatureImportance(),
          ModelMetricsService.getPCAVisualization(),
          ModelMetricsService.getModelStats()
        ]);
        
        // Guardar los datos
        classDistribution.value = classDistributionData;
        confusionMatrix.value = confusionMatrixData;
        featureImportance.value = featureImportanceData;
        pcaData.value = pcaVisualizationData;
        modelStats.value = modelStatsData;
        
        // Crear los gráficos una vez que tenemos los datos
        createCharts();
        
      } catch (error) {
        errorMessage.value = error instanceof Error 
          ? error.message 
          : 'Ha ocurrido un error al cargar los datos del modelo';
        showError.value = true;
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
      errorMessage,
      showError,
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
  background-color: #f8f9fa;
  min-height: calc(100vh - 60px - 100px); /* Considerando altura de navbar y footer */
}

.section-title {
  color: #1a4b8c;
  font-weight: bold;
}

.chart-container {
  margin: 20px 0;
}

/* Estilo para los tabs verticales */
:deep(.nav-pills .nav-link.active) {
  background-color: #1a4b8c;
}

:deep(.nav-pills .nav-link) {
  color: #1a4b8c;
}

:deep(.card-header:first-child) {
  background-color: rgba(26, 75, 140, 0.05);
}
</style> 