from django.urls import path
from app.views import login_view,upload_students
from . import views

urlpatterns = [
    path("login/",login_view,name='login'),
    path('',                         views.home,           name='home'),
     path('upload/', views.upload_students, name='upload_students'),
]



 
