from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path("equipment/<slug:slug>/",
         views.equipment_category,
         name="equipment_category"
         ),
     path("inventory/",
         views.inventory,
         name="inventory"
         ),
    path('orders/',
         views.my_orders,
         name='my_orders'),
    path('orders/<int:booking_id>/return/',
         views.return_booking,
         name='return_booking'),
    path('confirmation/',
         views.confirmation,
         name='confirmation'
         ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
