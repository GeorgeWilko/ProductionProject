from random import choice
from django.shortcuts import render
from .models import Equipment, EquipmentCategory, Booking
from django.core.mail import send_mail


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
                unit = choice(list(available))

                booking = Booking.objects.create(
                    equipment=unit,
                    start_date=start_date,
                    end_date=end_date,
                    status=Booking.Status.CONFIRMED,
                )

                unit.status = Equipment.Status.UNAVAILABLE
                unit.save(update_fields=["status"])

                message = (
                    "================================================\n"
                    "              SUCCESSFUL BOOKING\n"
                    "================================================\n\n"
                    f"Booking reference : #{booking.id}\n"
                    f"Booked equipment  : {booking.equipment.name}\n"
                    f"From              : {booking.start_date}\n"
                    f"To                : {booking.end_date}\n\n"
                    "Thank you for choosing this service.\n"
                    "================================================"
                )

                send_mail(
                    "Confirmation of your booking request",
                    message,
                    "g.wilkinson6868@Student.leedsbeckett.ac.uk",
                    ["g.wilkinson6868@Student.leedsbeckett.ac.uk"],
                    fail_silently=False,
                )

    else:
        error = "Please book an item from the booking page."

    context = {
        "booking": booking,
        "error": error,
    }

    return render(request, "website/Confirmation_page.html", context)