from django import forms
from products.models import Product

class ProductForm(forms.ModelForm):
    screenshots = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        required=False,
        label='Add Screenshots (up to 5)',
    )
    demoFile = forms.FileField(
        widget=forms.FileInput(attrs={'accept': '.zip,.rar'}),
        required=False,
        label='Demo File (ZIP or RAR only)',
    )
    downloadFile = forms.FileField(
        widget=forms.FileInput(attrs={'accept': '.zip,.rar'}),
        required=False,
        label='Download File (ZIP or RAR only)',
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'icon', 'image', 'screenshots', 'demoFile', 'downloadFile', 'demoName', 'demoDescription']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'price'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'id': 'icon'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'id': 'image'}),
            'demoName': forms.TextInput(attrs={'class': 'form-control', 'id': 'demoName'}),
            'demoDescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'demoDescription'}),
        }
