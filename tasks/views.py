from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, Status
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import TaskEditForm, TaskCreateForm
from django.contrib import messages
from tables.models import Sprint, Project
from functools import wraps

def check_task_access(view_func):
    @wraps(view_func)
    def wrapper(request, task_id, *args, **kwargs):
        task = get_object_or_404(Task, id=task_id)
        if not request.user.is_authenticated:
            messages.error(request, 'Необходимо войти в систему.')
            return redirect('login')
        if task.sprint:
            project = task.sprint.project
            if request.user != project.creator and request.user not in project.editors.all():
                messages.error(request, 'У вас нет доступа к этой задаче.')
                return redirect('home')
        else:
            messages.error(request, 'Задача не привязана к спринту.')
            return redirect('home')
            
        return view_func(request, task, *args, **kwargs)
    return wrapper

def check_sprint_access(view_func):
    @wraps(view_func)
    def wrapper(request, sprint_id, *args, **kwargs):
        sprint = get_object_or_404(Sprint, id=sprint_id)
        
        if request.user != sprint.project.creator and request.user not in sprint.project.editors.all():
            messages.error(request, 'У вас нет доступа к этому спринту.')
            return redirect('home')
            
        return view_func(request, sprint, *args, **kwargs)
    return wrapper

@login_required
@check_task_access
def delete_task(request, task):
    if request.method == 'POST':
        task.soft_delete()
        messages.success(request, 'Задача успешно удалена!')
        return redirect('sprint_detail', sprint_id=task.sprint.id)
    
    return render(request, 'tasks/delete_task.html', {
        'task': task
    })

@login_required
@check_task_access
def view_task(request, task):
    return render(request, 'tasks/view_task.html', {
        'task': task
    })

@login_required
@check_sprint_access
def create_task(request, sprint):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST, sprint=sprint)
        if form.is_valid():
            task = form.save(commit=False)
            task.sprint = sprint
            task.save()
            form.save_m2m()  # Сохраняем связи many-to-many
            messages.success(request, 'Задача успешно создана!')
            return redirect('sprint_detail', sprint_id=sprint.id)
    else:
        form = TaskCreateForm(sprint=sprint)
    
    return render(request, 'tasks/create_task.html', {
        'form': form,
        'sprint': sprint,
        'project': sprint.project
    })

@login_required
@check_task_access
def edit_task(request, task):
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task, sprint=task.sprint)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена!')
            return redirect('sprint_detail', sprint_id=task.sprint.id)
    else:
        form = TaskEditForm(instance=task, sprint=task.sprint)
    
    return render(request, 'tasks/edit_task.html', {
        'form': form,
        'task': task
    })
