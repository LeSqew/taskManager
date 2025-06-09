from django import forms
from .models import Task, Status, File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.content_type.startswith('image/'):
                raise forms.ValidationError('Файл должен быть изображением')
            if file.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('Размер файла не должен превышать 5MB')
        return file

class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'priority', 'difficulty']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'priority', 'difficulty']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 