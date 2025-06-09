from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Sprint
from .forms import ProjectForm, SprintForm
from tasks.models import Task, Status


# Create your views here.
@login_required
def home(request):
    # Получаем проекты, где пользователь является создателем или редактором
    created_projects = Project.objects.filter(creator=request.user)
    editable_projects = Project.objects.filter(editors=request.user)
    return render(request, 'tables/home.html', {
        'created_projects': created_projects,
        'editable_projects': editable_projects
    })

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            
            # Добавляем редакторов
            editors = form.cleaned_data.get('editors', [])
            project.editors.add(*editors)
            
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'tables/create_project.html', {'form': form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if not project.has_access(request.user):
        return redirect('home')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            
            # Обновляем список редакторов
            editors = form.cleaned_data.get('editors', [])
            project.editors.clear()  # Удаляем всех текущих редакторов
            project.editors.add(*editors)  # Добавляем новых
            
            return redirect('project_detail', project_id=project.id)
    else:
        # Подготавливаем начальные данные для поля editors
        initial_data = {
            'editors': '\n'.join(editor.username for editor in project.editors.all())
        }
        form = ProjectForm(instance=project, initial=initial_data)
    
    return render(request, 'tables/edit_project.html', {'form': form, 'project': project})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.user != project.creator and request.user not in project.editors.all():
        messages.error(request, 'У вас нет доступа к этому проекту.')
        return redirect('home')
    
    sprints = project.sprints.all()
    return render(request, 'tables/project_detail.html', {
        'project': project,
        'sprints': sprints
    })

def ensure_statuses_exist():
    """Проверяет наличие статусов и создает их, если они отсутствуют"""
    statuses = ['В планах', 'В работе', 'Завершено']
    for status_name in statuses:
        Status.objects.get_or_create(name=status_name)

@login_required
def create_sprint(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Проверяем доступ к проекту
    if request.user != project.creator and request.user not in project.editors.all():
        messages.error(request, 'У вас нет доступа к этому проекту.')
        return redirect('home')
    
    # Проверяем наличие статусов
    ensure_statuses_exist()
    
    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.project = project
            sprint.save()
            messages.success(request, 'Спринт успешно создан!')
            return redirect('project_detail', project_id=project.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = SprintForm()
    
    return render(request, 'tables/create_sprint.html', {
        'form': form,
        'project': project
    })

@login_required
def edit_sprint(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    project = sprint.project
    
    if request.user != project.creator and request.user not in project.editors.all():
        messages.error(request, 'У вас нет доступа к этому спринту.')
        return redirect('home')
    
    if request.method == 'POST':
        form = SprintForm(request.POST, instance=sprint)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спринт успешно обновлен!')
            return redirect('project_detail', project_id=project.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = SprintForm(instance=sprint)
    
    return render(request, 'tables/edit_sprint.html', {'form': form, 'sprint': sprint, 'project': project})

@login_required
def sprint_detail(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    project = sprint.project
    
    if request.user != project.creator and request.user not in project.editors.all():
        messages.error(request, 'У вас нет доступа к этому спринту.')
        return redirect('home')
    
    tasks = Task.get_active_tasks().filter(sprint=sprint)
    return render(request, 'tables/sprint_detail.html', {
        'sprint': sprint,
        'project': project,
        'tasks': tasks
    })

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.user != project.creator:
        messages.error(request, 'Только создатель может удалить проект.')
        return redirect('home')
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Проект успешно удален!')
        return redirect('home')
    
    return render(request, 'tables/delete_project.html', {'project': project})

@login_required
def delete_sprint(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    project = sprint.project
    
    if request.user != project.creator and request.user not in project.editors.all():
        messages.error(request, 'У вас нет доступа к этому спринту.')
        return redirect('home')
    
    if request.method == 'POST':
        sprint.delete()
        messages.success(request, 'Спринт успешно удален!')
        return redirect('project_detail', project_id=project.id)
    
    return render(request, 'tables/delete_sprint.html', {'sprint': sprint, 'project': project})
