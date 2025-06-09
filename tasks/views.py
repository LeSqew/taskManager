from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, Status
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import TaskEditForm, TaskCreateForm
from django.contrib import messages
from tables.models import Sprint, Project

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Проверяем доступ к задаче через спринт или проект
    if task.sprint:
        project = task.sprint.project
        if request.user != project.creator and request.user not in project.editors.all():
            messages.error(request, 'У вас нет доступа к этой задаче.')
            return redirect('home')
    else:
        messages.error(request, 'Задача не привязана к спринту.')
        return redirect('home')
    
    if request.method == 'POST':
        task.soft_delete()
        messages.success(request, 'Задача успешно удалена!')
        return redirect('sprint_detail', sprint_id=task.sprint.id)
    
    return render(request, 'tasks/delete_task.html', {
        'task': task
    })

@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Проверяем доступ к задаче через спринт или проект
    if task.sprint:
        project = task.sprint.project
        if request.user != project.creator and request.user not in project.editors.all():
            messages.error(request, 'У вас нет доступа к этой задаче.')
            return redirect('home')
    else:
        messages.error(request, 'Задача не привязана к спринту.')
        return redirect('home')
    
    return render(request, 'tasks/view_task.html', {
        'task': task
    })

@login_required
def create_task(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    project = sprint.project
    
    # Проверяем доступ к спринту через проект
    if request.user != project.creator and request.user not in project.editors.all():
        messages.error(request, 'У вас нет доступа к этому спринту.')
        return redirect('home')
    
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.sprint = sprint
            task.save()
            
            messages.success(request, 'Задача успешно создана!')
            return redirect('sprint_detail', sprint_id=sprint.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = TaskCreateForm()
    
    return render(request, 'tasks/create_task.html', {
        'form': form,
        'sprint': sprint
    })

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Проверяем доступ к задаче через спринт или проект
    if task.sprint:
        project = task.sprint.project
        if request.user != project.creator and request.user not in project.editors.all():
            messages.error(request, 'У вас нет доступа к этой задаче.')
            return redirect('home')
    else:
        messages.error(request, 'Задача не привязана к спринту.')
        return redirect('home')
    
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена!')
            return redirect('sprint_detail', sprint_id=task.sprint.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = TaskEditForm(instance=task)
    
    return render(request, 'tasks/edit_task.html', {
        'form': form,
        'task': task
    })
