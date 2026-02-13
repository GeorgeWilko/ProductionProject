from django.shortcuts import render
from .models import Equipment

def home(request):
    title = "Accessible Equipment Hire"
    subtitle = "A range of equipment for students to borrow and use."

    context = {
        "title": title,
        "subtitle": subtitle,
    }
    return render(request, 'website/Home.html', context)

def equipment_list(request):
    equipment = Equipment.objects.select_related('category', 'location').all()

    context = {
        "equipment": equipment,
    }
    return render(request, 'website/Booking page.html', context)

def confirm(request):
    equipment_id = request.GET.get("equipment_id")
    selected = None

    if equipment_id:
        selected = Equipment.objects.get(id=equipment_id)

    context = {
        "selected": selected,
    }
    return render(request, 'website/Confirmation page.html', context)