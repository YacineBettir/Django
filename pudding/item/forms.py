from django import forms
from .models import item

INPUT_CLASSES='w-full py-4 px-6 rounded-xl border '
class NewItemForm(forms.ModelForm):
    class Meta:
        model=item
        fields=[
            'category',
            'name',
            'description',
            'price',
            'image',
            ]
        widgets={
            'category':forms.Select(attrs={
                'class':INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }