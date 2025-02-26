from django import forms
from .models import BursaryApplication

class BursaryApplicationForm(forms.ModelForm):
    class Meta:
        model = BursaryApplication
        fields = '__all__'
    
    def clean_dob(self):
        dob = self.cleaned_data.get("dob")
        if dob == "":
            raise forms.ValidationError("Date of Birth cannot be empty.")
        return dob
