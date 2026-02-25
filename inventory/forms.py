from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItem, Profile

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)

    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'category']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class HealthInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['sex', 'weight', 'height', 'age']
        widgets = {
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in kg'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height in cm'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
        }
        labels = {
            'sex': 'Sex',
            'weight': 'Weight (kg)',
            'height': 'Height (cm)',
            'age': 'Age',
        }