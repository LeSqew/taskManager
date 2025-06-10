document.addEventListener('DOMContentLoaded', function() {
    const deleteModal = document.getElementById('deleteModal');
    const projectNameSpan = document.getElementById('projectName');
    const projectIdInput = document.getElementById('projectId');
    const deleteForm = document.getElementById('deleteForm');
    
    // Обработчик открытия модального окна
    deleteModal.addEventListener('show.bs.modal', function(event) {
        // Получаем кнопку, которая вызвала модальное окно
        const button = event.relatedTarget;
        
        // Получаем данные из data-атрибутов
        const projectId = button.getAttribute('data-project-id');
        const projectName = button.getAttribute('data-project-name');
        
        // Обновляем содержимое модального окна
        projectNameSpan.textContent = projectName;
        projectIdInput.value = projectId;
        
        // Обновляем action формы
        deleteForm.action = `/projects/${projectId}/delete/`;
        
        console.log('Project ID:', projectId); // Для отладки
        console.log('Project Name:', projectName); // Для отладки
    });
});

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
