from rest_framework.urlpatterns import path

from . import views

urlpatterns = [
    path("", views.Seaplatforms.as_view()),
    path("<int:pk>", views.SeaplatformDetail.as_view()),
    path("perks/", views.Perks.as_view()),
    path("perks/<int:pk>", views.PerkDetail.as_view()),
]
