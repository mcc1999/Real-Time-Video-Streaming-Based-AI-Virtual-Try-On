from django.urls import path
from . import views

urlpatterns = {
    path("clothShot/", views.ClothShot.as_view()),
    path("getCloth/", views.GetCloth.as_view()),
    path("getCutCloth/", views.GetCutCloth.as_view()),
    path("getTryOnCloth/", views.GetTryOnCloth.as_view()),
    path("getAICloth/", views.GetAICloth.as_view()),
}