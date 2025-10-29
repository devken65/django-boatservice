# Create your views here.
from django.shortcuts import render

from .models import Boat


def see_all_boats(request):
    boats = Boat.objects.all()
    return render(
        request,
        "all_boats.html",
        {
            "boats": boats,
            "title": "Hello! This from django",
        },
    )


def see_one_boat(request, boat_pk):
    try:
        boat = Boat.objects.get(pk=boat_pk)
        return render(
            request,
            "boat_details.html",
            {
                "boat": boat,
            },
        )
    except Boat.DoesNotExist:
        return render(
            request,
            "boat_details.html",
            {
                "not_found": True,
            },
        )
