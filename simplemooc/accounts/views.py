from django.shortcuts import render, redirect, get_object_or_404
from .form import CreateUserForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

User=get_user_model()

@login_required
def dashboard(request):
    template_name='registration/painel.html'
    return render(request, template_name)

@login_required
def edit(request):
    template_name='registration/edit.html'
    context={}
    if request.method=="POST":
        form=EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form=EditAccountForm(instance=request.user)
            messages.success(request,'As alterações foram feitas com sucesso')
            return redirect('accounts:dashboard')
    else:
        form=EditAccountForm(instance=request.user)
    context['form']=form
    return render(request, template_name, context)

@login_required
def edit_pass(request):
    template_name='registration/edit_pass.html'
    context={}
    if request.method=="POST":
        form=PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Sua senha foi alterada com sucesso')
            return redirect('accounts:dashboard')
    else:
        form=PasswordChangeForm(user=request.user)
    context['form']=form
    return render(request, template_name, context)

def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    else:
        template_name='registration/login.html'
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('accounts:dashboard')
            else:
                messages.info(request,'Login ou senha incorretos, tente novamente')
        return render(request, template_name)

def registration(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    else:
        template_name='registration/register.html'
        form=CreateUserForm()
        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user=authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
                auth_login(request, user)
                messages.success(request,'Bem-vindo ao simple MOOC\nSeu usuário foi criado com sucesso')
                return redirect('accounts:dashboard')
        context={
            'form':form
        }
        return render(request, template_name, context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('core:home')