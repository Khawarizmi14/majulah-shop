from django import forms
from main.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'thumbnail', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-500 focus:border-red-500 block w-full p-2.5',
                'placeholder': 'e.g., Nike Phantom Boots'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-500 focus:border-red-500 block w-full p-2.5',
                'placeholder': 'e.g., 1500000'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-red-500 focus:border-red-500',
                'rows': 4,
                'placeholder': 'Product details...'
            }),
            'category': forms.Select(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-500 focus:border-red-500 block w-full p-2.5'
            }),
            'thumbnail': forms.URLInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-500 focus:border-red-500 block w-full p-2.5',
                'placeholder': 'https://example.com/image.jpg'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-red-600 bg-gray-100 border-gray-300 rounded focus:ring-red-500'
            }),
        }