from django import forms
from .models import Task, Status
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'priority', 'difficulty', 'status', 'assigned_users']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название задачи'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание задачи'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100',
                'placeholder': 'Приоритет (1-100)'
            }),
            'difficulty': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100',
                'placeholder': 'Сложность (1-100)'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_users': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '5',
                'style': 'height: auto;'
            })
        }

    def __init__(self, *args, **kwargs):
        sprint = kwargs.pop('sprint', None)
        super().__init__(*args, **kwargs)
        
        # Получаем список пользователей с доступом к проекту
        if sprint and sprint.project:
            project = sprint.project
            project_users = [project.creator]
            project_users.extend(project.editors.all())
            self.fields['assigned_users'].queryset = User.objects.filter(id__in=[user.id for user in project_users]).distinct()
            self.fields['assigned_users'].label = 'Ответственные пользователи'
            self.fields['assigned_users'].help_text = 'Выберите пользователей, ответственных за выполнение задачи (для множественного выбора используйте Ctrl/Cmd)'
        else:
            self.fields['assigned_users'].queryset = User.objects.none()

class TaskCreateForm(TaskForm):
    pass

class TaskEditForm(TaskForm):
    pass 