from django import forms
from .models import Comment, Registration,Subscriber

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