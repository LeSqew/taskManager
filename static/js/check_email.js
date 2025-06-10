document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('id_email');
    const feedback = document.getElementById('emailFeedback');
    const submitButton = document.querySelector('button[type="submit"]');
    let emailExists = false;

    if (!emailInput || !feedback) return;

    emailInput.addEventListener('input', function() {
        const email = emailInput.value.trim();

        if (email.length === 0) {
            feedback.textContent = '';
            feedback.className = 'form-text';
            submitButton.disabled = false;
            emailExists = false;
            return;
        }

        // Добавляем индикатор загрузки
        feedback.textContent = 'Проверка...';
        feedback.className = 'form-text text-muted';

        fetch(`/users/check_email/?email=${encodeURIComponent(email)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети');
                }
                return response.json();
            })
            .then(data => {
                if (data.exists) {
                    feedback.textContent = 'Этот email уже используется';
                    feedback.className = 'form-text text-danger';
                    submitButton.disabled = true;
                    emailExists = true;
                } else {
                    feedback.textContent = 'Email доступен';
                    feedback.className = 'form-text text-success';
                    submitButton.disabled = false;
                    emailExists = false;
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                feedback.textContent = 'Ошибка при проверке email';
                feedback.className = 'form-text text-danger';
                submitButton.disabled = false;
            });
    });

    // Предотвращаем отправку формы, если email уже существует
    const form = emailInput.closest('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (emailExists) {
                e.preventDefault();
                feedback.textContent = 'Пожалуйста, используйте другой email';
                feedback.className = 'form-text text-danger';
            }
        });
    }
}); 