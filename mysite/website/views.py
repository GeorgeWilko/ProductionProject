from random import choice
from django.shortcuts import render, redirect, get_object_or_404
from .models import Equipment, EquipmentCategory, Booking
from django.core.mail import send_mail
from collections import OrderedDict
import json

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
    bookings = []
    unavailable_items = []

    if request.method != "POST":
        return redirect("booking")

    print("POST:", request.POST)
    equipment_name = request.POST.get("equipment_name")
    equipment_names_raw = request.POST.get("equipment_names", "")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    equipment_names = []

    if equipment_names_raw:
        try:
            parsed_names = json.loads(equipment_names_raw)
            if isinstance(parsed_names, list):
                equipment_names = [name for name in parsed_names if isinstance(name, str) and name.strip()]
        except json.JSONDecodeError:
            equipment_names = []

    if not equipment_names and equipment_name:
        equipment_names = [equipment_name]

    if not equipment_names or not start_date or not end_date:
        return redirect("booking")

    for name in equipment_names:
        available = Equipment.objects.filter(
            name__startswith=name,
            status=Equipment.Status.AVAILABLE,
            quantity__gt=0,
        )

        if not available.exists():
            unavailable_items.append(name)
            continue

        unit = choice(list(available))

        booking = Booking.objects.create(
            equipment=unit,
            start_date=start_date,
            end_date=end_date,
            status=Booking.Status.CONFIRMED,
        )

        unit.status = Equipment.Status.UNAVAILABLE
        unit.save(update_fields=["status"])
        bookings.append(booking)

    if not bookings:
        return redirect("booking")

    message_lines = [
        "================================================",
        "              SUCCESSFUL BOOKING",
        "================================================",
        "",
    ]

    for booking in bookings:
        message_lines.extend([
            f"Booking reference : #{booking.id}",
            f"Booked equipment  : {booking.equipment.name}",
            f"From              : {booking.start_date}",
            f"To                : {booking.end_date}",
            "",
        ])

    if unavailable_items:
        message_lines.append("Unavailable items:")
        for item_name in unavailable_items:
            message_lines.append(f"- {item_name}")
        message_lines.append("")

    message_lines.extend([
        "Thank you for choosing this service.",
        "================================================",
    ])

    message = "\n".join(message_lines)

    send_mail(
        "Confirmation of your booking request",
        message,
        "g.wilkinson6868@Student.leedsbeckett.ac.uk",
        ["g.wilkinson6868@Student.leedsbeckett.ac.uk"],
        fail_silently=False,
    )

    return render(request, "website/Confirmation_page.html", {
        "bookings": bookings,
        "unavailable_items": unavailable_items,
    })
