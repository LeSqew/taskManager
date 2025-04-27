from django import forms
from .models import Task, Status

class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['tittle', 'description', 'status', 'priority', 'difficulty', 'deadline']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 