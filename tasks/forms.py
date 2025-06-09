from django import forms
from .models import Task, Status

class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_users', 'deadline', 'status', 'priority', 'difficulty']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'priority': forms.NumberInput(attrs={
                'min': 1,
                'max': 100,
                'class': 'form-control'
            }),
            'difficulty': forms.NumberInput(attrs={
                'min': 1,
                'max': 100,
                'class': 'form-control'
            })
        }

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_users', 'deadline', 'status', 'priority', 'difficulty']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'priority': forms.NumberInput(attrs={
                'min': 1,
                'max': 100,
                'class': 'form-control'
            }),
            'difficulty': forms.NumberInput(attrs={
                'min': 1,
                'max': 100,
                'class': 'form-control'
            })
        } 