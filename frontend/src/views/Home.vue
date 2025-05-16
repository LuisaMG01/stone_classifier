<template>
  <div class="home">
    <!-- Hero Section -->
    <BContainer fluid class="hero p-5">
      <BRow class="align-items-center">
        <BCol cols="12" md="6" class="text-white">
          <h1 class="display-4 fw-bold mb-4">Clasificador de Minerales y Rocas</h1>
          <p class="lead mb-4">
            Analiza y clasifica minerales y rocas usando tecnologías de aprendizaje automático con alta precisión.
            Nuestra plataforma te permite identificar grupos químicos de minerales a partir de sus propiedades físicas
            y tipos de rocas mediante análisis de imágenes.
          </p>
          <div class="d-flex flex-wrap gap-2">
            <BButton variant="light" size="lg" to="/classify" class="me-2 mb-2">
              <BIcon icon="gem" aria-hidden="true"></BIcon> Clasificar Minerales
            </BButton>
            <BButton variant="outline-light" size="lg" to="/classify-rocks" class="me-2 mb-2">
              <BIcon icon="layers" aria-hidden="true"></BIcon> Clasificar Rocas
            </BButton>
          </div>
        </BCol>
        <BCol cols="12" md="6" class="d-none d-md-block">
          <div class="hero-images">
            <img src="@/assets/crystal.svg" alt="Mineral Crystal" class="img-fluid minerals-img" />
            <div class="rocks-img-container">
              <BIcon icon="layers" scale="3" class="rocks-icon"></BIcon>
            </div>
          </div>
        </BCol>
      </BRow>
    </BContainer>

    <!-- Classification Options Section -->
    <BContainer class="my-5">
      <h2 class="text-center mb-5 section-title">Sistemas de Clasificación</h2>
      
      <BRow>
        <BCol md="6" class="mb-4">
          <BCard class="h-100 classification-card minerals-card">
            <BCardBody class="text-center p-4">
              <div class="classification-icon minerals-icon-container mb-3">
                <BIcon icon="gem" scale="2"></BIcon>
              </div>
              <h3 class="h3 mb-3">Clasificación de Minerales</h3>
              <p class="card-text mb-4">
                Identifica grupos químicos de minerales a partir de propiedades como dureza, gravedad específica, densidad y más.
              </p>
              <div class="d-flex justify-content-center flex-wrap gap-2">
                <BButton to="/classify" variant="primary" class="me-2 mb-2">
                  Clasificar
                </BButton>
                <BButton to="/history" variant="outline-primary" class="mb-2">
                  Ver Historial
                </BButton>
              </div>
            </BCardBody>
          </BCard>
        </BCol>
        
        <BCol md="6" class="mb-4">
          <BCard class="h-100 classification-card rocks-card">
            <BCardBody class="text-center p-4">
              <div class="classification-icon rocks-icon-container mb-3">
                <BIcon icon="layers" scale="2"></BIcon>
              </div>
              <h3 class="h3 mb-3">Clasificación de Rocas</h3>
              <p class="card-text mb-4">
                Identifica tipos de rocas a partir de imágenes utilizando tecnología de redes neuronales convolucionales.
              </p>
              <div class="d-flex justify-content-center flex-wrap gap-2">
                <BButton to="/classify-rocks" class="me-2 mb-2 btn-rock-primary">
                  Clasificar
                </BButton>
                <BButton to="/rock-history" class="mb-2 btn-rock-outline">
                  Ver Historial
                </BButton>
              </div>
            </BCardBody>
          </BCard>
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
                Obtén resultados instantáneos al ingresar propiedades o subir imágenes de tus muestras.
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
                Algoritmos avanzados entrenados con extensas bases de datos de minerales y rocas.
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
                Accede al historial de todas tus clasificaciones anteriores, tanto de minerales como de rocas.
              </p>
            </BCardBody>
          </BCard>
        </BCol>
      </BRow>
      
      <!-- Sección de análisis de modelo -->
      <BRow class="mt-5">
        <BCol cols="12">
          <BCard bg-variant="light" class="h-100 feature-card p-0 overflow-hidden">
            <BRow class="g-0">
              <BCol md="8">
                <BCardBody>
                  <h3 class="h4 mb-3">Análisis Avanzado del Modelo</h3>
                  <p class="card-text">
                    Explora en profundidad el funcionamiento interno de nuestros modelos de clasificación.
                    Visualiza métricas clave como matriz de confusión, importancia de características y distribución 
                    de clases para entender cómo funcionan los algoritmos de predicción.
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
      <h2 class="mb-4 text-white">¿Listo para clasificar?</h2>
      <p class="lead mb-4 text-white">
        Comienza ahora con nuestras herramientas de identificación de minerales y rocas
      </p>
      <div class="d-flex justify-content-center flex-wrap">
        <BButton variant="light" size="lg" to="/classify" class="me-3 mb-2">
          <BIcon icon="gem" aria-hidden="true" class="me-2"></BIcon> Clasificar Minerales
        </BButton>
        <BButton variant="outline-light" size="lg" to="/classify-rocks" class="mb-2">
          <BIcon icon="layers" aria-hidden="true" class="me-2"></BIcon> Clasificar Rocas
        </BButton>
      </div>
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

.hero-images {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.minerals-img {
  max-width: 80%;
  z-index: 1;
}

.rocks-img-container {
  position: absolute;
  bottom: 10%;
  right: 10%;
  background: rgba(92, 48, 125, 0.9);
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  box-shadow: 0 0 20px rgba(92, 48, 125, 0.5);
}

.rocks-icon {
  color: white;
}

.classification-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: none;
  border-radius: 15px;
  overflow: hidden;
}

.minerals-card {
  border-top: 5px solid #1a4b8c;
}

.rocks-card {
  border-top: 5px solid #5c307d;
}

.classification-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.classification-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  color: white;
}

.minerals-icon-container {
  background: linear-gradient(135deg, #1a4b8c 0%, #3498db 100%);
  box-shadow: 0 5px 15px rgba(26, 75, 140, 0.3);
}

.rocks-icon-container {
  background: linear-gradient(135deg, #5c307d 0%, #9561e2 100%);
  box-shadow: 0 5px 15px rgba(92, 48, 125, 0.3);
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
  position: relative;
  display: inline-block;
  padding-bottom: 15px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #1a4b8c, #3498db);
  border-radius: 3px;
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

.btn-rock-primary {
  background-color: #5c307d;
  color: white;
}

.btn-rock-primary:hover {
  background-color: #4a2766;
  color: white;
}

.btn-rock-outline {
  background-color: transparent;
  border: 1px solid #5c307d;
  color: #5c307d;
}

.btn-rock-outline:hover {
  background-color: #5c307d;
  color: white;
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

@media (max-width: 768px) {
  .rocks-img-container {
    width: 70px;
    height: 70px;
  }
}
</style> 