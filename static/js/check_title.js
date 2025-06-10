document.addEventListener('DOMContentLoaded', function () {
	const titleInput = document.getElementById('id_title');
	const feedback = document.getElementById('titleFeedback');
	const submitButton = document.querySelector('button[type="submit"]');
	let titleExists = false;
  
	if (!titleInput || !feedback) return; // Проверяем наличие элементов
  
	titleInput.addEventListener('input', function () {
	  const title = titleInput.value.trim();
  
	  if (title.length === 0) {
		feedback.textContent = '';
		feedback.className = 'form-text';
		submitButton.disabled = false;
		titleExists = false;
		return;
	  }
  
	  // Добавляем индикатор загрузки
	  feedback.textContent = 'Проверка...';
	  feedback.className = 'form-text text-muted';
  
	  fetch(`/tasks/check_title/?title=${encodeURIComponent(title)}`)
		.then((response) => {
		  if (!response.ok) {
			throw new Error('Ошибка сети');
		  }
		  return response.json();
		})
		.then((data) => {
		  if (data.exists) {
			feedback.textContent = 'Такая задача уже существует';
			feedback.className = 'form-text text-danger';
			submitButton.disabled = true;
			titleExists = true;
		  } else {
			feedback.textContent = 'Название доступно';
			feedback.className = 'form-text text-success';
			submitButton.disabled = false;
			titleExists = false;
		  }
		})
		.catch((error) => {
		  console.error('Ошибка:', error);
		  feedback.textContent = 'Ошибка при проверке названия';
		  feedback.className = 'form-text text-danger';
		  submitButton.disabled = false;
		});
	});
  
	// Предотвращаем отправку формы, если название уже существует
	const form = titleInput.closest('form');
	if (form) {
	  form.addEventListener('submit', function(e) {
		if (titleExists) {
		  e.preventDefault();
		  feedback.textContent = 'Пожалуйста, выберите другое название';
		  feedback.className = 'form-text text-danger';
		}
	  });
	}
  });