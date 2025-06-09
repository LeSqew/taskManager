from django import forms
from .models import ScrumTable

class ScrumTableForm(forms.ModelForm):
    class Meta:
        model = ScrumTable
        fields = ['name', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 