from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model=User
        fields=['username','email','password1','password2']

class UserUpdateForms(forms.ModelForm):
    # username = forms.CharField()
    # email=forms.EmailField()

    class Meta:
        model=User
        fields=('username','email')



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['password']
