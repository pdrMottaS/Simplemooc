from django.urls import path
from . import views

app_name="courses"

urlpatterns = [
    path('',views.index, name="index"),
    path('<slug:slug>/',views.details, name="details"),
    path('<slug:slug>/subscribe', views.enrollment, name='enrollment'),
    path('<slug:slug>/announcements', views.announcements, name='announcements'),
    path('<slug:slug>/announcements/<int:pk>', views.show_announcements, name='show_announcements'),
    path('<slug:slug>/unsubscribe', views.undo_enrollment,name='undo_enrollment'),
    path('<slug:slug>/lessons', views.lessons, name='lessons'),
    path('<slug:slug>/lessons/<int:pk>', views.show_lesson, name='show_lesson'),
    path('<slug:slug>/materials/<int:pk>', views.material, name='material'),
]