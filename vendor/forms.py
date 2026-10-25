from django import forms

from .models import *

class CreateProductForm(forms.ModelForm):
    interior_title = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Name', 'class': 'form-control'}
    ))

    price = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'placeholder': 'Enter Price', 'class': 'form-control'}
    ))

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.Select(
            attrs={'class': 'form-control'}
    ))

    description = forms.HTMLFIELD(
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
    ))

    class Meta:
        model = Interior
        fields = ['interior_title', 'slug', 'interior_description', 'images']