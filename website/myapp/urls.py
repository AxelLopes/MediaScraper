from django.urls import path
from . import views

urlpatterns=[
    #path('',views.home, name='home'),
    path("todos/",views.todos, name='todos'),
    path("send_keywords/",views.process_keywords, name='send_keywords'),    
    path("run_script/",views.test_script, name='run_script'),
    path('', views.home, name='afficher_dataframe'),  
]