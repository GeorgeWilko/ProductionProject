from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.home,
         name='home'
         ),
    path('equipment/',
         views.equipment_list,
         name='equipment_list'
         ),
    path('confirm/',
         views.confirm,
         name='confirm'
         ),
]