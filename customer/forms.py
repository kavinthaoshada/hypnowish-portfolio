from django import forms
from .models import Customer, Subscriber, Purchase
from django.contrib.auth.forms import UserCreationForm

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })
            
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone_number', 'address', 'two_factor_enabled']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
                }),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'two_factor_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email',
                'aria-label': 'Your email',
                'required': 'required',
            })
        }
        
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['customer', 'product']
        widgets = {
            'customer': forms.HiddenInput(),
            'product': forms.HiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if customer:
            self.fields['customer'].initial = customer
        if product:
            self.fields['product'].initial = product