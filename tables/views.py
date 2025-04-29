from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import ScrumTable
from django.contrib import messages


# Create your views here.
@login_required
def home(request):
    
    # Получаем только таблицы, доступные текущему пользователю
    tables = ScrumTable.objects.filter(assigned_users=request.user)
    return render(request, 'home.html', {'tables': tables})

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
    
    return render(request, 'tables/create_table.html')

@login_required
def scrum_tables(request, table_id):
    table = get_object_or_404(ScrumTable, id=table_id, assigned_users=request.user)
    return render(request, 'tables/scrum_tables.html', {'table': table})

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
    
    return render(request, 'tables/edit_table.html', {'table': table})
