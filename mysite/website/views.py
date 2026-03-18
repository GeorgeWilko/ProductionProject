from random import choice
from django.shortcuts import render, redirect, get_object_or_404
from .models import Equipment, EquipmentCategory, Booking
from django.core.mail import send_mail
from collections import OrderedDict

def home(request):
    title = "Accessible Equipment Hire"
    subtitle = "A range of equipment for students to borrow and use."

    context = {
        "title": title,
        "subtitle": subtitle,
    }
    return render(request, 'website/Home.html', context)


def booking(request):
    categories = EquipmentCategory.objects.prefetch_related("equipment").order_by("name")
    grouped_categories = []

    for category in categories:
        grouped = OrderedDict()

        for item in category.equipment.all():
            base_name = item.name.split(" - Unit ")[0]

            if base_name not in grouped:
                grouped[base_name] = {
                    "name": base_name,
                    "category_id": category.id,
                    "available_count": 0,
                }

            if item.status == "available" and item.quantity > 0:
                grouped[base_name]["available_count"] += 1

        grouped_categories.append({
            "name": category.name,
            "description": category.description,
            "image": category.image,
            "slug": category.slug,
            "items": list(grouped.values()),
        })

    context = {
        "categories": grouped_categories,
    }

    return render(request, "website/Booking_page.html", context)

def equipment_category(request, slug):
    category = get_object_or_404(
        EquipmentCategory.objects.prefetch_related("equipment"),
        slug=slug
    )

    grouped_items = OrderedDict()

    for item in category.equipment.all():
        base_name = item.name.split(" - Unit ")[0]

        if base_name not in grouped_items:
            grouped_items[base_name] = {
                "name": base_name,
                "available_count": 0,
                "image": item.image,
            }

        if item.status == "available" and item.quantity > 0:
            grouped_items[base_name]["available_count"] += 1

    context = {
        "category": category,
        "items": list(grouped_items.values()),
    }

    return render(request, "website/Equipment.html", context)

def confirmation(request):
    booking = None
    error = None

    if request.method != "POST":
        return redirect("booking")

    print("POST:", request.POST)
    equipment_name = request.POST.get("equipment_name")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    if not equipment_name or not start_date or not end_date:
        return redirect("booking")

    available = Equipment.objects.filter(
        name__startswith=equipment_name,
        status=Equipment.Status.AVAILABLE,
        quantity__gt=0,
    )

    if not available.exists():
        return redirect("booking")

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

    return render(request, "website/Confirmation_page.html", {"booking": booking})
