<template>
  <div id="app">
    <!-- Navbar -->
    <BNavbar toggleable="lg" type="dark" variant="primary" sticky>
      <BContainer>
        <BNavbarBrand to="/">
          <BIcon icon="gem" aria-hidden="true"></BIcon>
          Clasificador de Minerales
        </BNavbarBrand>

        <BNavbarToggle target="nav-collapse"></BNavbarToggle>

        <BCollapse id="nav-collapse" is-nav>
          <BNavbarNav class="ml-auto">
            <BNavItem to="/" exact>Inicio</BNavItem>
            <BNavItem to="/classify">Clasificación</BNavItem>
            <BNavItem to="/history">Historial</BNavItem>
            <BNavItem to="/model-analysis">Análisis del Modelo</BNavItem>
          </BNavbarNav>
        </BCollapse>
      </BContainer>
    </BNavbar>

    <!-- Router View -->
    <router-view/>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4 mt-5">
      <BContainer>
        <BRow>
          <BCol cols="12" md="6">
            <h5>Clasificador de Minerales</h5>
            <p>Una aplicación para identificar y clasificar minerales utilizando aprendizaje automático.</p>
          </BCol>
          <BCol cols="12" md="6" class="text-md-right">
            <p>© 2025 Clasificador de Minerales. Todos los derechos reservados.</p>
          </BCol>
        </BRow>
      </BContainer>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'AppMain'
}
</script>

<style>
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
  color: #343a40;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

footer {
  margin-top: auto;
}

.router-link-exact-active {
  font-weight: bold;
}
</style>
