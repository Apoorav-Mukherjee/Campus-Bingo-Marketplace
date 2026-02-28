from django import forms
from .models import Product, ProductImage


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={
            'class': 'form-control'
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # ✅ FIX: If no files selected, return empty list instead of raising error
        if not data:
            return []

        # Normalize to list always
        if not isinstance(data, (list, tuple)):
            data = [data]

        # Validate each file individually using parent clean()
        result = []
        for item in data:
            try:
                cleaned = super().clean(item, initial)
                result.append(cleaned)
            except forms.ValidationError:
                pass  # Skip invalid/empty entries

        return result


class ProductForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        label='Product Images',
        help_text='You can select multiple images at once (hold Ctrl/Cmd to select several).'
    )

    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price',
            'condition', 'category', 'location'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. MacBook Pro 2021, Calculus Textbook...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your item — condition details, reason for selling, etc.'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0'
            }),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. North Campus, Dorm Block B...'
            }),
        }
        labels = {
            'title': 'Product Title',
            'price': 'Price (₹)',
            'location': 'Pickup Location (optional)',
        }