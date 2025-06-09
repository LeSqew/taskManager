from django import forms
from .models import Project, Sprint

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'links']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'links': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Введите ссылки, по одной на строку'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['name', 'start_date', 'deadline']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 