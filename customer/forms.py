from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'Your first name', 'last_name': 'Your last name',
            'email': 'you@example.com', 'password1': 'Create a password',
            'password2': 'Repeat the password',
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': placeholders.get(name, '')})
            field.help_text = ''

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EmailLoginForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        'staff_account': "This is an admin account. Please log in through the admin panel.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'you@example.com'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your password'})

    def clean_username(self):
        return self.cleaned_data['username'].strip().lower()

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if user.is_staff:
            raise forms.ValidationError(self.error_messages['staff_account'], code='staff_account')