<template>
  <div class="home">
    <!-- Hero Section -->
    <BContainer fluid class="hero p-5">
      <BRow class="align-items-center">
        <BCol cols="12" md="6" class="text-white">
          <h1 class="display-4 fw-bold mb-4">Clasificador de Minerales</h1>
          <p class="lead mb-4">
            Analiza y clasifica minerales usando aprendizaje automático con precisión.
            Nuestra plataforma te permite identificar grupos químicos de minerales a partir de sus propiedades físicas.
          </p>
          <BButton variant="light" size="lg" to="/classify" class="me-3">
            <BIcon icon="gem" aria-hidden="true"></BIcon> Iniciar Clasificación
          </BButton>
          <BButton variant="outline-light" size="lg" to="/history">
            <BIcon icon="clock-history" aria-hidden="true"></BIcon> Ver Historial
          </BButton>
        </BCol>
        <BCol cols="12" md="6" class="d-none d-md-block">
          <img src="@/assets/crystal.svg" alt="Mineral Crystal" class="img-fluid" />
        </BCol>
      </BRow>
    </BContainer>

    <!-- Features Section -->
    <BContainer class="py-5">
      <h2 class="text-center mb-5 section-title">Características Principales</h2>
      <BRow>
        <BCol cols="12" md="4" class="mb-4">
          <BCard bg-variant="light" class="h-100 feature-card">
            <BCardBody class="text-center">
              <div class="feature-icon mb-3">
                <BIcon icon="lightning" scale="2" variant="primary"></BIcon>
              </div>
              <h3 class="h4">Clasificación Rápida</h3>
              <p class="card-text">
                Obtén resultados instantáneos al ingresar las propiedades del mineral.
              </p>
            </BCardBody>
          </BCard>
        </BCol>
        <BCol cols="12" md="4" class="mb-4">
          <BCard bg-variant="light" class="h-100 feature-card">
            <BCardBody class="text-center">
              <div class="feature-icon mb-3">
                <BIcon icon="graph-up" scale="2" variant="primary"></BIcon>
              </div>
              <h3 class="h4">Alta Precisión</h3>
              <p class="card-text">
                Algoritmos de machine learning entrenados con extensas bases de datos mineralógicas.
              </p>
            </BCardBody>
          </BCard>
        </BCol>
        <BCol cols="12" md="4" class="mb-4">
          <BCard bg-variant="light" class="h-100 feature-card">
            <BCardBody class="text-center">
              <div class="feature-icon mb-3">
                <BIcon icon="clock-history" scale="2" variant="primary"></BIcon>
              </div>
              <h3 class="h4">Historial Completo</h3>
              <p class="card-text">
                Accede al historial de todas tus clasificaciones anteriores para análisis comparativos.
              </p>
            </BCardBody>
          </BCard>
        </BCol>
      </BRow>
      
      <!-- Nueva sección para visualización de modelo -->
      <BRow class="mt-5">
        <BCol cols="12">
          <BCard bg-variant="light" class="h-100 feature-card p-0 overflow-hidden">
            <BRow class="g-0">
              <BCol md="8">
                <BCardBody>
                  <h3 class="h4 mb-3">Análisis Avanzado del Modelo</h3>
                  <p class="card-text">
                    Explora en profundidad el funcionamiento interno del modelo de clasificación de minerales. 
                    Visualiza métricas clave como matriz de confusión, importancia de características y distribución 
                    de grupos químicos para entender cómo el algoritmo toma sus decisiones.
                  </p>
                  <BButton to="/model-analysis" variant="primary">
                    <BIcon icon="bar-chart" aria-hidden="true" class="me-2"></BIcon>
                    Ver Análisis del Modelo
                  </BButton>
                </BCardBody>
              </BCol>
              <BCol md="4" class="d-flex align-items-center justify-content-center p-4">
                <div class="analysis-icon">
                  <BIcon icon="graph-up" scale="4" variant="primary"></BIcon>
                </div>
              </BCol>
            </BRow>
          </BCard>
        </BCol>
      </BRow>
    </BContainer>

    <!-- Call to Action -->
    <BContainer fluid class="cta-section p-5 text-center">
      <h2 class="mb-4 text-white">¿Listo para clasificar un mineral?</h2>
      <p class="lead mb-4 text-white">
        Ingresa las propiedades de tu mineral y descubre su grupo químico
      </p>
      <BButton variant="light" size="lg" to="/classify">
        Comenzar Ahora
      </BButton>
    </BContainer>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'HomeView'
})
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #1a4b8c 0%, #0d2a4e 100%);
  padding: 80px 0;
  border-radius: 0 0 20px 20px;
  margin-bottom: 40px;
}

.feature-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: none;
  border-radius: 10px;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 30px rgba(26, 75, 140, 0.15);
}

.feature-icon {
  background-color: rgba(26, 75, 140, 0.1);
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.section-title {
  color: #1a4b8c;
  font-weight: bold;
}

.cta-section {
  background: linear-gradient(135deg, #2980b9 0%, #1a4b8c 100%);
  margin-top: 40px;
  border-radius: 20px 20px 0 0;
}

h1, h2, h3 {
  font-weight: 700;
}

.btn {
  padding: 10px 25px;
  border-radius: 30px;
  font-weight: 600;
}

.btn-light {
  background-color: #ffffff;
  color: #1a4b8c;
}

.btn-outline-light:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.analysis-icon {
  background-color: rgba(26, 75, 140, 0.1);
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style> 