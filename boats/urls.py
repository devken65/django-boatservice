from django.urls import path

from . import views

urlpatterns = [
    # "" 은 이미 boats/ 에 들어온 것이나 같다.
    path("", views.Boats.as_view()),
    path("<int:pk>", views.BoatDetail.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
]
