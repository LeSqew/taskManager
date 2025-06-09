from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ScrumTable
from .forms import ScrumTableForm
from tasks.models import Task


# Create your views here.
@login_required
def home(request):
    tables = ScrumTable.objects.filter(assigned_users=request.user)
    return render(request, 'tables/home.html', {'tables': tables})

@login_required
def create_table(request):
    if request.method == 'POST':
        form = ScrumTableForm(request.POST)
        if form.is_valid():
            table = form.save(commit=False)
            table.isMainTable = False
            table.save()
            table.assigned_users.add(request.user)
            messages.success(request, 'Таблица успешно создана!')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ScrumTableForm()
    
    return render(request, 'tables/create_table.html', {'form': form})

@login_required
def edit_table(request, table_id):
    table = get_object_or_404(ScrumTable, id=table_id)
    
    if request.user not in table.assigned_users.all():
        messages.error(request, 'У вас нет доступа к этой таблице.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ScrumTableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            messages.success(request, 'Таблица успешно обновлена!')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ScrumTableForm(instance=table)
    
    return render(request, 'tables/edit_table.html', {'form': form, 'table': table})

@login_required
def sprint_table(request, table_id):
    table = get_object_or_404(ScrumTable, id=table_id)
    
    if request.user not in table.assigned_users.all():
        messages.error(request, 'У вас нет доступа к этой таблице.')
        return redirect('home')
    
    # Получаем только неудаленные задачи для таблицы
    active_tasks = Task.get_active_tasks().filter(scrum_tables=table)
    
    return render(request, 'tables/scrum_table.html', {
        'table': table,
        'active_tasks': active_tasks
    })

@login_required
def delete_table(request, table_id):
    table = get_object_or_404(ScrumTable, id=table_id)
    
    if request.user not in table.assigned_users.all():
        messages.error(request, 'У вас нет доступа к этой таблице.')
        return redirect('home')
    
    if request.method == 'POST':
        table.delete()
        messages.success(request, 'Таблица успешно удалена!')
        return redirect('home')
    
    return render(request, 'tables/delete_table.html', {
        'table': table
    })
