from django.urls import path
from . import views

app_name='item'


urlpatterns= [
    path('<int:id>/',views.detail,name='detail'),
    path('new/',views.newitem,name='new-item')
]