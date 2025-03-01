from django import forms
from .models import Comment, Registration,Subscriber, Payment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['text', 'email', 'author']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model= Registration
        fields= ['full_name', 'email', 'phone']

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            })
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'phone_number','email', ]
        widgets={
            'name':forms.TextInput(attrs={
                'class': 'form-control',
            }),

           
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            
        }