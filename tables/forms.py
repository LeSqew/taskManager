from django import forms
from .models import Project, Sprint
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
    editors = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Введите никнеймы редакторов, по одному на строку'
        }),
        help_text='Введите никнеймы пользователей, которым нужно дать доступ к проекту'
    )

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

    def clean_editors(self):
        editor_usernames = self.cleaned_data['editors'].strip().split('\n')
        editors = []
        for username in editor_usernames:
            username = username.strip()
            if username:
                try:
                    user = User.objects.get(username=username)
                    editors.append(user)
                except User.DoesNotExist:
                    raise forms.ValidationError(f'Пользователь {username} не найден')
        return editors

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