from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from simplemooc.core.utils import generate_hash_key
from .models import PasswordReset
from simplemooc.core.mail import send_mail_template

User=get_user_model()

class PasswordResetForm(forms.Form):
    email=forms.EmailField(label='E-mail para recuperação de senha')

    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError('E-mail não encontado no sistema')

    def save(self):
        user=User.objects.get(email=self.cleaned_data['email'])
        key=generate_hash_key(user.username)
        reset=PasswordReset(key=key, user=user)
        reset.save()
        template_name='registration/password_reset_mail.html'
        subject='Criar nova senha no Simple MOOC'
        context={
            'reset':reset
        }
        send_mail_template(subject=subject,template_name=template_name,context=context,recipient_list=[user.email])

class CreateUserForm(UserCreationForm):

    password1=forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2=forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem')
        return password2

    def save(self, commit=True):
        user=super(CreateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
    class Meta:
        model=User
        fields=['username', 'email']

class EditAccountForm(forms.ModelForm):

    class Meta:
        model=User
        fields=['username', 'email', 'name']