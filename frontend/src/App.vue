<template>
  <div id="app">
    <!-- Background shape -->
    <div class="background-shape"></div>
    
    <!-- Navbar moderno -->
    <BNavbar toggleable="lg" class="modern-navbar py-2" sticky>
      <BContainer fluid="md">
        <BNavbarBrand to="/" class="brand-container">
          <div class="brand-icon-container me-2">
            <BIcon icon="gem" aria-hidden="true" class="brand-icon"></BIcon>
          </div>
          <span class="brand-text">Clasificador de Minerales y Rocas</span>
        </BNavbarBrand>

        <BNavbarToggle target="nav-collapse" class="ms-auto custom-toggler"></BNavbarToggle>

        <BCollapse id="nav-collapse" is-nav>
          <BNavbarNav class="ms-auto">
            <BNavItem to="/" exact class="nav-item-modern mx-1">
              <BIcon icon="house-door" class="menu-icon me-1"></BIcon>
              Inicio
            </BNavItem>
            
            <!-- Menú desplegable de Clasificación -->
            <BNavItemDropdown class="nav-item-modern mx-1" id="classification-dropdown">
              <template #button-content>
                <BIcon icon="clipboard-data" class="menu-icon me-1"></BIcon>
                Clasificación
              </template>
              <BDropdownItem to="/classify" class="mineral-dropdown-item">
                <BIcon icon="gem" class="me-1" variant="primary"></BIcon>
                Minerales
              </BDropdownItem>
              <BDropdownItem to="/classify-rocks" class="rock-dropdown-item">
                <BIcon icon="layers" class="me-1" variant="purple"></BIcon>
                Rocas
              </BDropdownItem>
            </BNavItemDropdown>
            
            <!-- Menú desplegable de Historiales -->
            <BNavItemDropdown class="nav-item-modern mx-1" id="history-dropdown">
              <template #button-content>
                <BIcon icon="clock-history" class="menu-icon me-1"></BIcon>
                Historiales
              </template>
              <BDropdownItem to="/history" class="mineral-dropdown-item">
                <BIcon icon="gem" class="me-1" variant="primary"></BIcon>
                Minerales
              </BDropdownItem>
              <BDropdownItem to="/rock-history" class="rock-dropdown-item">
                <BIcon icon="layers" class="me-1" variant="purple"></BIcon>
                Rocas
              </BDropdownItem>
            </BNavItemDropdown>
            
            <!-- Análisis -->
            <BNavItem to="/model-analysis" class="nav-item-modern mx-1">
              <BIcon icon="graph-up" class="menu-icon me-1"></BIcon>
              Análisis
            </BNavItem>
          </BNavbarNav>
        </BCollapse>
      </BContainer>
    </BNavbar>

    <!-- Router View -->
    <main>
      <router-view/>
    </main>

    <!-- Footer moderno -->
    <footer class="modern-footer py-4 mt-5">
      <BContainer>
        <BRow>
          <BCol cols="12" md="6">
            <h5 class="footer-title">Clasificador de Minerales y Rocas</h5>
            <p class="footer-text">Una aplicación para identificar y clasificar minerales y rocas utilizando aprendizaje automático.</p>
          </BCol>
          <BCol cols="12" md="6" class="text-md-end">
            <p class="footer-copyright">© 2025 Clasificador de Minerales y Rocas. Todos los derechos reservados.</p>
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
:root {
  --primary-color: #1a4b8c;
  --primary-light: #3498db;
  --primary-gradient: linear-gradient(120deg, #1a4b8c, #3498db);
  --text-light: #f8fafc;
  --text-dark: #1e293b;
  --bg-light: #f8fafc;
  --bg-card: rgba(255, 255, 255, 0.98);
  --shadow-sm: 0 2px 8px rgba(15, 23, 42, 0.08);
  --shadow-md: 0 8px 24px rgba(15, 23, 42, 0.12);
  --radius-sm: 8px;
  --radius-md: 12px;
  --transition-normal: all 0.3s ease;
}

/* Base styles */
body {
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  background-color: var(--bg-light);
  color: var(--text-dark);
  overflow-x: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
}

/* Background decoration */
.background-shape {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at top right, rgba(26, 75, 140, 0.05), transparent 70%),
              radial-gradient(circle at bottom left, rgba(52, 152, 219, 0.05), transparent 70%);
  z-index: -1;
}

/* Modern Navbar Styles */
.modern-navbar {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 20px rgba(15, 23, 42, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: var(--transition-normal);
  border-bottom: 1px solid rgba(226, 232, 240, 0.7);
}

.brand-container {
  display: flex;
  align-items: center;
}

.brand-icon-container {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--primary-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(26, 75, 140, 0.2);
}

.brand-icon {
  color: white;
  font-size: 1.2rem;
}

.brand-text {
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--primary-color);
  letter-spacing: -0.01em;
}

.nav-item-modern {
  position: relative;
  transition: var(--transition-normal);
}

.nav-item-modern a {
  color: var(--text-dark);
  font-weight: 500;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-sm);
  transition: var(--transition-normal);
}

.nav-item-modern a:hover {
  color: var(--primary-color);
  background-color: rgba(26, 75, 140, 0.05);
}

.nav-item-modern a.router-link-exact-active {
  color: var(--primary-color);
  font-weight: 600;
}

.nav-item-modern a.router-link-exact-active:after {
  content: '';
  position: absolute;
  left: 0.75rem;
  right: 0.75rem;
  bottom: 0;
  height: 3px;
  background: var(--primary-gradient);
  border-radius: 3px 3px 0 0;
}

.custom-toggler {
  border: none;
  padding: 0.25rem;
  color: var(--primary-color);
}

/* Main content area */
main {
  flex: 1;
}

/* Modern Footer Styles */
.modern-footer {
  background-color: var(--primary-color);
  background-image: linear-gradient(160deg, #1a4b8c 0%, #2c5d9e 100%);
  color: var(--text-light);
  box-shadow: 0 -4px 20px rgba(15, 23, 42, 0.1);
  margin-top: auto;
}

.footer-title {
  font-weight: 600;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.footer-text {
  opacity: 0.9;
  font-size: 0.95rem;
  line-height: 1.5;
}

.footer-copyright {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Estilos específicos para los menús desplegables */
.menu-icon {
  font-size: 1rem;
  vertical-align: -2px;
}

.dropdown-menu {
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(15, 23, 42, 0.1);
  border: 1px solid rgba(226, 232, 240, 0.7);
  padding: 0.5rem;
  min-width: 180px;
}

.dropdown-item {
  border-radius: 6px;
  padding: 0.6rem 1rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.mineral-dropdown-item:hover, .mineral-dropdown-item:focus {
  background-color: rgba(26, 75, 140, 0.07);
  color: #1a4b8c;
}

.rock-dropdown-item:hover, .rock-dropdown-item:focus {
  background-color: rgba(92, 48, 125, 0.07);
  color: #5c307d;
}

/* Corregir el icono morado que no está definido en Bootstrap */
.b-icon.text-purple {
  color: #5c307d !important;
}

.nav-item-modern .dropdown-toggle::after {
  margin-left: 0.4em;
  vertical-align: 0.15em;
}

.navbar .nav-item.show > .nav-link {
  color: var(--primary-color) !important;
  background-color: rgba(26, 75, 140, 0.05);
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .nav-item-modern a.router-link-exact-active:after {
    left: 0;
    right: 0;
    bottom: -2px;
  }
}

@media (max-width: 768px) {
  .brand-text {
    font-size: 1rem;
  }
  
  .brand-icon-container {
    width: 32px;
    height: 32px;
  }
}
</style>
