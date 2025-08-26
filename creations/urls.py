from django.urls import path
from .views import listCreations, creationDetail



urlpatterns = [
    path("", listCreations, name="creationList"),
    path("<slug:slug>/", creationDetail, name="creationDetail"),
]
