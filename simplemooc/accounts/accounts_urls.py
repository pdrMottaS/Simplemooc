from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.registration, name="register"),
    path('painel/', views.dashboard, name="dashboard"),
    path('edit/', views.edit, name="edit"),
    path('edit_pass/', views.edit_pass, name="edit_pass"),
]