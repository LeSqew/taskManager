from django.db import migrations

def create_initial_statuses(apps, schema_editor):
    Status = apps.get_model('tasks', 'Status')
    
    # Создаем начальные статусы
    statuses = [
        'В планах',
        'В работе',
        'Завершено'
    ]
    
    for status_name in statuses:
        Status.objects.create(name=status_name)

def remove_initial_statuses(apps, schema_editor):
    Status = apps.get_model('tasks', 'Status')
    Status.objects.filter(name__in=['В планах', 'В работе', 'Завершено']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_statuses, remove_initial_statuses),
    ] 