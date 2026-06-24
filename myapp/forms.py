from django import forms
from django.contrib.auth.models import User
from .models import Patient


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)

    email = forms.EmailField(
        error_messages={
            'invalid': 'Invalid Email Address'
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Username already exists'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Email already exists'
            )

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError(
                'Password must contain at least 8 characters'
            )

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    'Passwords do not match'
                )

        return cleaned_data
    

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = [
            'patient_name',
            'age',
            'bmi_category',
            'symptoms',
            'image'
        ]
        widgets = {
            'symptoms': forms.SelectMultiple(
                attrs={'class': 'symptom-select'}
            ),
        }

    def clean_symptoms(self):

        symptoms = self.cleaned_data.get('symptoms')

        if not symptoms:
            raise forms.ValidationError(
                "Please select at least one symptom."
            )

        return symptoms

    def clean_image(self):

        image = self.cleaned_data.get('image')

        if not image:
            raise forms.ValidationError(
                "Please upload an ultrasound image."
            )

        return image

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)

        self.fields['patient_name'].required = True
        self.fields['age'].required = True
        self.fields['bmi_category'].required = True
        self.fields['symptoms'].required = True
        self.fields['image'].required = True

        self.fields['patient_name'].error_messages = {
            'required': 'Patient name is required.'
        }

        self.fields['age'].error_messages = {
            'required': 'Age is required.'
        }

        self.fields['bmi_category'].error_messages = {
            'required': 'BMI category is required.'
        }

        self.fields['symptoms'].error_messages = {
            'required': 'Please select at least one symptom.'
        }

        self.fields['image'].error_messages = {
            'required': 'Please upload an ultrasound image.'
        }

