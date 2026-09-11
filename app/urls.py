from django.urls import path
from app.views import login_view,upload_students
from . import views

urlpatterns = [
    path("login/",login_view,name='login'),
    path('',                         views.home,           name='home'),
     path('upload/', views.upload_students, name='upload_students'),
      path('ai/', views.ai_chat_page, name='ai_chat'),
    path('ai/ask/', views.ai_ask, name='ai_ask')
]



 
