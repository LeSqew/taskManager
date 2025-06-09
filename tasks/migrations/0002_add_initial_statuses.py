from django.db import migrations

def create_initial_statuses(apps, schema_editor):
    Status = apps.get_model('tasks', 'Status')
    Status.objects.create(name='В планах')
    Status.objects.create(name='В работе')
    Status.objects.create(name='Сделано')

def remove_initial_statuses(apps, schema_editor):
    Status = apps.get_model('tasks', 'Status')
    Status.objects.filter(name__in=['В планах', 'В работе', 'Сделано']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_statuses, remove_initial_statuses),
    ] 