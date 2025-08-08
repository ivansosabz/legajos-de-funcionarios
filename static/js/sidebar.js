document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("sidebarToggle");
    const mainContent = document.getElementById("mainContent");

    // Verificar el estado guardado o el tamaño de la pantalla
    const isMobile = window.matchMedia("(max-width: 767.98px)").matches;
    const savedState = localStorage.getItem('sidebarCollapsed');

    // Estado inicial basado en preferencias guardadas o tamaño de pantalla
    const initialState = isMobile ?
        { collapsed: true, show: false } :
        { collapsed: savedState ? JSON.parse(savedState) : false, show: true };

    // Aplicar estado inicial
    applySidebarState(initialState);

    // Manejar el botón de toggle
    if (toggleBtn) {
        toggleBtn.addEventListener("click", function() {
            const isCollapsed = sidebar.classList.contains("collapsed");
            const isHidden = !sidebar.classList.contains("show");

            if (isMobile) {
                // En móvil, solo alternar visibilidad
                sidebar.classList.toggle("show", !isHidden);
            } else {
                // En escritorio, alternar estado colapsado
                const newState = {
                    collapsed: !isCollapsed,
                    show: true
                };
                applySidebarState(newState);
                localStorage.setItem('sidebarCollapsed', newState.collapsed);
            }
        });
    }

    // Manejar cambios en el tamaño de la pantalla
    window.addEventListener("resize", function() {
        const isMobileNow = window.matchMedia("(max-width: 767.98px)").matches;
        const isCollapsed = sidebar.classList.contains("collapsed");

        if (isMobileNow) {
            // Cambió a móvil: ocultar sidebar
            applySidebarState({ collapsed: true, show: false });
        } else {
            // Cambió a escritorio: restaurar estado guardado
            const savedState = localStorage.getItem('sidebarCollapsed');
            applySidebarState({
                collapsed: savedState ? JSON.parse(savedState) : false,
                show: true
            });
        }
    });

    // Función para aplicar el estado del sidebar
    function applySidebarState(state) {
        sidebar.classList.toggle("collapsed", state.collapsed);
        sidebar.classList.toggle("show", state.show);

        // Ajustar el contenido principal en móvil
        if (window.matchMedia("(max-width: 767.98px)").matches) {
            mainContent.style.marginLeft = state.show ? "0" : "0";
        }
    }

    // Cerrar sidebar al hacer clic fuera en móvil
    document.addEventListener("click", function(event) {
        if (window.matchMedia("(max-width: 767.98px)").matches &&
            sidebar.classList.contains("show") &&
            !sidebar.contains(event.target) &&
            event.target !== toggleBtn) {
            sidebar.classList.remove("show");
        }
    });
});