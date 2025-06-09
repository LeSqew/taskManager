from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, Status, File
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import TaskEditForm, TaskCreateForm, FileForm
from django.contrib import messages
from tables.models import ScrumTable

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    table = task.scrum_tables.first()
    
    if not table or request.user not in table.assigned_users.all():
        messages.error(request, 'У вас нет доступа к этой задаче.')
        return redirect('home')
    
    if request.method == 'POST':
        # task.delete()
        task.soft_delete()
        messages.success(request, 'Задача успешно удалена!')
        return redirect('scrum_tables', table_id=table.id)
    
    return render(request, 'tasks/delete_task.html', {
        'task': task,
        'table': table
    })

@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    table = task.scrum_tables.first()
    
    if not table or request.user not in table.assigned_users.all():
        messages.error(request, 'У вас нет доступа к этой задаче.')
        return redirect('home')
    
    return render(request, 'tasks/view_task.html', {
        'task': task,
        'table': table
    })

@login_required
def create_task(request, table_id):
    table = get_object_or_404(ScrumTable, id=table_id, assigned_users=request.user)
    
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        
        if form.is_valid() and file_form.is_valid():
            task = form.save(commit=False)
            task.save()
            table.tasks.add(task)
            
            # Обработка загруженного файла
            if 'file' in request.FILES:
                file_form.instance.task = task
                file_form.save()
            
            messages.success(request, 'Задача успешно создана!')
            return redirect('scrum_tables', table_id=table.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = TaskCreateForm()
        file_form = FileForm()
    
    return render(request, 'tasks/create_task.html', {
        'form': form,
        'file_form': file_form,
        'table': table
    })

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    table = task.scrum_tables.first()
    
    if not table or request.user not in table.assigned_users.all():
        messages.error(request, 'У вас нет доступа к этой задаче.')
        return redirect('home')
    
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        file_form = FileForm(request.POST, request.FILES)
        
        if form.is_valid() and file_form.is_valid():
            form.save()
            
            # Обработка загруженного файла
            if 'file' in request.FILES:
                file_form.instance.task = task
                file_form.save()
            
            messages.success(request, 'Задача успешно обновлена!')
            return redirect('scrum_tables', table_id=table.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = TaskEditForm(instance=task)
        file_form = FileForm()
    
    return render(request, 'tasks/edit_task.html', {
        'form': form,
        'file_form': file_form,
        'task': task,
        'table': table
    })
