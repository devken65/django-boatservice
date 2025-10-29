from django.urls import path

from . import views

urlpatterns = [
    # "" 은 이미 boats/ 에 들어온 것이나 같다.
    path("", views.see_all_boats),
    path("<int:boat_pk>", views.see_one_boat),
]
