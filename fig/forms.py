from django import forms

from .models import profile

class proform(forms.ModelForm):
    class Meta:
      model= profile
      fields=['name','figma_file']
