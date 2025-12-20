# app/forms.py
from django import forms
from .models import SystemUser, Doctor


class LoginForm(forms.Form):
    email = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class AddAdminForm(forms.ModelForm):
    class Meta:
        model = SystemUser
        fields = ["full_name", "email", "hashed_password"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите полное имя"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email"}),
            "hashed_password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and SystemUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

class AddDoctorForm(forms.ModelForm):
    specialization = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите специализацию"})
    )
    license_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите license_number"})
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите номер телефона"})
    )

    class Meta:
        model = SystemUser
        fields = ["full_name", "email", "hashed_password"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите полное имя"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email"}),
            "hashed_password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and SystemUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email


    def clean_license_number(self):
        license_number = self.cleaned_data.get("license_number")
        if Doctor.objects.filter(license_number=license_number).exists():
            raise forms.ValidationError("Доктор с такой лицензией уже существует!")
        return license_number

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if Doctor.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Доктор с таким телефоном уже существует!")
        return phone