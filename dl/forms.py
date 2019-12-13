from django import forms
from .models import Files

class DLFiles(forms.ModelForm):
    class Meta:
        model = Files
        fields = {'course','week','file','title','author','date'}