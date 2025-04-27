from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ScrumTable, Status, Task
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import TaskEditForm, TaskCreateForm
from django.contrib import messages

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

@login_required
def create_table(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        deadline = request.POST.get('deadline')
        
        if name and deadline:
            # Создаем новую таблицу
            table = ScrumTable.objects.create(
                name=name,
                deadline=deadline,
                isMainTable=False
            )
            # Добавляем текущего пользователя к таблице
            table.assigned_users.add(request.user)
            messages.success(request, 'Таблица успешно создана!')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
    
    return render(request, 'tasks/create_table.html')

@login_required
def home(request):
    # Создаем тестовую таблицу, если её нет
    if not ScrumTable.objects.filter(isMainTable=True).exists():
        create_test_table()
    
    # Получаем только таблицы, доступные текущему пользователю
    tables = ScrumTable.objects.filter(assigned_users=request.user)
    return render(request, 'tasks/home.html', {'tables': tables})

@login_required
def scrum_tables(request, table_id):
    table = get_object_or_404(ScrumTable, id=table_id, assigned_users=request.user)
    return render(request, 'tasks/scrum_tables.html', {'table': table})

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

@login_required
def edit_table(request, table_id):
    table = get_object_or_404(ScrumTable, id=table_id, assigned_users=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        deadline = request.POST.get('deadline')
        
        if name and deadline:
            table.name = name
            table.deadline = deadline
            table.save()
            messages.success(request, 'Таблица успешно обновлена!')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
    
    return render(request, 'tasks/edit_table.html', {'table': table})

@login_required
def create_task(request, table_id):
    table = get_object_or_404(ScrumTable, id=table_id, assigned_users=request.user)
    
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            table.Tasks.add(task)
            messages.success(request, 'Задача успешно создана!')
            return redirect('scrum_tables', table_id=table.id)
    else:
        form = TaskCreateForm()
    
    return render(request, 'tasks/create_task.html', {
        'form': form,
        'table': table
    })
