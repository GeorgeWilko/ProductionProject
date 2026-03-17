from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.home,
         name='home'
         ),
    path('booking/',
         views.booking,
         name='booking'
         ),
    path('equipment/peripherals/',
         views.peripherals,
         name='peripherals'
         ),
    path('equipment/computing/',
         views.computing,
         name='computing'
         ),
    path('equipment/display/',
         views.display,
         name='display'
         ),
    path('equipment/storage/',
         views.storage,
         name='storage'
         ),
    path('equipment/accessories/',
         views.accessories,
         name='accessories'
         ),
    path('confirmation/',
         views.confirmation,
         name='confirmation'
         ),
]
