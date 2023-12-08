from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):

    username = forms.CharField(
        label="Username: ", 
        initial=None,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    password = forms.CharField(
        label="Password: ", 
        initial=None,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(help_text='a valid email please', required=True)

    class Meta:
        model= get_user_model()
        fields=['first_name', 'last_name', 'username', 'email', 'password1','password2']

    def save(self,commit=True):
        user=super(UserRegistrationForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user