from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,
        help_text='Please provide a valid email address.',
        error_messages={'exists':
            'Already exists, please use a different email address.'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return email

class EmailEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password')