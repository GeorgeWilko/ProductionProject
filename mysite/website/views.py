from random import random
from django.shortcuts import render
from .models import Equipment, EquipmentCategory, Booking


def home(request):
    title = "Accessible Equipment Hire"
    subtitle = "A range of equipment for students to borrow and use."

    context = {
        "title": title,
        "subtitle": subtitle,
    }
    return render(request, 'website/Home.html', context)


def booking(request):
    categories = EquipmentCategory.objects.all().order_by("name")

    context = {
        "categories": categories,
    }
    return render(request, 'website/Booking_page.html', context)


def confirmation(request):
    booking = None
    error = None

    if request.method == "POST":
        category_id = request.POST.get("category_id")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if not category_id or not start_date or not end_date:
            error = "Missing item or dates."

        else:
            available = Equipment.objects.filter(
                category_id=category_id,
                status=Equipment.Status.AVAILABLE,
                quantity__gt=0,
            )

            if not available.exists():
                error = "No available items remaining."

            else:
                unit = random.choice(list(available))

                booking = Booking.objects.create(
                    user=request.user,
                    equipment=unit,
                    start_date=start_date,
                    end_date=end_date,
                    status=Booking.Status.CONFIRMED,
                )

                unit.status = Equipment.Status.UNAVAILABLE
                unit.save(update_fields=["status"])

    else:
        error = "Please book an item from the booking page."

    context = {
        "booking": booking,
        "error": error,
    }

    return render(request, "website/Confirmation_page.html", context)