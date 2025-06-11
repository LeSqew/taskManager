// taskLoader.js
// Реализация загрузки задач с использованием jQuery, Deferred-объектов и прелоадера

// Функция для отображения прелоадера
function showPreloader() {
    $("#preloader").show();
}

// Функция для скрытия прелоадера
function hidePreloader() {
    $("#preloader").hide();
}

// Функция для загрузки задач с сервера с использованием Deferred
function loadTasks() {
    // Создаём Deferred-объект
    var deferred = $.Deferred();

    showPreloader(); // Показываем прелоадер при начале запроса

    // Выполняем AJAX-запрос
    $.ajax({
        url: '/api/sprint/' + window.sprintId + '/tasks/', // URL API для получения задач спринта
        method: 'GET',
        dataType: 'json'
    })
    .done(function(data) {
        // В случае успеха резолвим Deferred с полученными данными
        deferred.resolve(data);
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        // В случае ошибки реджектим Deferred с информацией об ошибке
        deferred.reject({
            status: textStatus,
            error: errorThrown,
            response: jqXHR.responseText
        });
    });

    // Возвращаем promise для дальнейшей обработки
    return deferred.promise();
}

// Функция для отображения списка задач
function renderTasks(tasks) {
    var $list = $("#task-list");
    $list.empty();
    if (tasks.length === 0) {
        $list.append('<li>Нет задач</li>');
        return;
    }
    tasks.forEach(function(task) {
        var html = '<li class="list-group-item d-flex justify-content-between align-items-center">';
        html += '<span>' + task.title + '</span>';
        html += '<div class="btn-group" role="group">';
        html += '<a href="/task/' + task.id + '/" class="btn btn-sm btn-outline-primary me-2">Просмотр</a>';
        html += '<a href="/task/' + task.id + '/edit/" class="btn btn-sm btn-outline-secondary me-2">Редактировать</a>';
        html += '<form id="deleteForm" method="post" action="{% url delete_task ' + task.id+'%}" class="d-inline">';
        html += '<input type="hidden" name="csrfmiddlewaretoken" value="' + $('input[name=csrfmiddlewaretoken]').val() + '">';
        html += '<input type="hidden" name="project_id" id="projectId">';
        html += '<button type="submit" class="btn btn-sm btn-outline-danger">Удалить</button>';
        html += '</form>';
        html += '</div></li>';
        $list.append(html);
    });
}

// Функция для отображения ошибки
function renderError(error) {
    var $list = $("#task-list");
    $list.empty();
    $list.append('<li class="error">Ошибка загрузки: ' + (error.error || error.status) + '</li>');
}

// Основная логика загрузки задач
$(document).ready(function() {
    // Скрываем прелоадер по умолчанию
    hidePreloader();

    // Запускаем загрузку задач
    loadTasks()
        .done(function(data) {
            // .done() вызывается при успешной загрузке задач
            renderTasks(data);
        })
        .fail(function(error) {
            // .fail() вызывается при ошибке загрузки
            renderError(error);
        })
        .always(function() {
            // .always() вызывается всегда после завершения запроса (успех или ошибка)
            hidePreloader();
        });
});

// Альтернативно можно использовать .then(success, fail) вместо .done() и .fail()
// loadTasks().then(renderTasks, renderError).always(hidePreloader); 