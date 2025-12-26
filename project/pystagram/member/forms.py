from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')
        labels = {
            'email' : '이메일',
            'password1' : '비밀번호',
            'password2' : '비밀번호 확인',
        }
        widgets = {
            'email' : forms.EmailInput(
                attrs={
                    'placeholder' : 'example@example.com',
                }
            )
        }
