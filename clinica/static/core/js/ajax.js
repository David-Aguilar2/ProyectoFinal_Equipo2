document.addEventListener('DOMContentLoaded', function() {
    const especialidadFilter = document.getElementById('id_especialidad_filter');
    const medicoSelect = document.getElementById('id_medico');
    
    if (especialidadFilter && medicoSelect) {
        especialidadFilter.addEventListener('change', function() {
            const especialidadId = this.value;
            
            if (especialidadId) {
                // Hacer petición AJAX para obtener médicos por especialidad
                fetch(`/sistema/api/medicos-por-especialidad/${especialidadId}/`)
                    .then(response => response.json())
                    .then(data => {
                        // Limpiar select
                        while (medicoSelect.options.length > 1) {
                            medicoSelect.remove(1);
                        }
                        
                        // Agregar nuevas opciones
                        data.medicos.forEach(medico => {
                            const option = document.createElement('option');
                            option.value = medico.id;
                            option.textContent = `Dr. ${medico.nombres} ${medico.apellidos} - ${medico.especialidad}`;
                            medicoSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error:', error));
            } else {
                // Recargar la página para mostrar todos los médicos
                location.reload();
            }
        });
    }
});