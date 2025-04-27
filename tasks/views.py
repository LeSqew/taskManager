from django.shortcuts import render, get_object_or_404, redirect
from .models import ScrumTable, Status, Task
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import TaskEditForm

def create_test_table():
    # Создаем статусы
    statuses = [
        Status.objects.get_or_create(name='В планах')[0],
        Status.objects.get_or_create(name='В работе')[0],
        Status.objects.get_or_create(name='Сделано')[0]
    ]
    
    # Создаем тестовую таблицу
    test_table = ScrumTable.objects.create(
        name='Тестовая таблица',
        deadline=timezone.now() + timezone.timedelta(days=30),
        isMainTable=True
    )
    
    # Создаем тестовые задачи
    tasks = [
        Task.objects.create(
            tittle='Тестовая задача 1',
            description='Описание задачи 1',
            deadline=timezone.now() + timezone.timedelta(days=7),
            status=statuses[0],
            priority=1,
            difficulty=2
        ),
        Task.objects.create(
            tittle='Тестовая задача 2',
            description='Описание задачи 2',
            deadline=timezone.now() + timezone.timedelta(days=14),
            status=statuses[1],
            priority=2,
            difficulty=3
        ),
        Task.objects.create(
            tittle='Тестовая задача 3',
            description='Описание задачи 3',
            deadline=timezone.now() + timezone.timedelta(days=21),
            status=statuses[2],
            priority=3,
            difficulty=1
        )
    ]
    
    # Добавляем задачи в таблицу
    test_table.Tasks.add(*tasks)
    return test_table

def scrum_tables(request):
    # Создаем тестовую таблицу, если её нет
    if not ScrumTable.objects.filter(isMainTable=True).exists():
        create_test_table()
    
    tables = ScrumTable.objects.all()
    return render(request, 'tasks/scrum_tables.html', {'tables': tables})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('scrum_tables')
    else:
        form = TaskEditForm(instance=task)
    
    return render(request, 'tasks/edit_task.html', {
        'form': form,
        'task': task
    })
