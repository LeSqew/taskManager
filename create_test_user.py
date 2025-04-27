import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskManager.settings')
django.setup()

from django.contrib.auth.models import User
from tasks.models import ScrumTable

def create_test_user():
    # Создаем пользователя
    user = User.objects.create_user(
        username='testuser',
        password='123',
        email='test@example.com'
    )
    
    # Находим тестовую таблицу и добавляем пользователя
    table = ScrumTable.objects.filter(isMainTable=True).first()
    if table:
        table.assigned_users.add(user)
        print(f"Пользователь {user.username} добавлен в таблицу {table.name}")
    
    print(f"Создан тестовый пользователь: {user.username}")

if __name__ == '__main__':
    create_test_user() 