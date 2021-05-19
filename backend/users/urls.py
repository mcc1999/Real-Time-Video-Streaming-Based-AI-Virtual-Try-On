from django.urls import path
from . import views

urlpatterns = {
    path('login/', views.Login.as_view()),
    path('register/', views.Register.as_view()),
    path('getUser/', views.GetUser.as_view()),
    path('signAnchor/', views.SignAnchor.as_view()),
    path('startLive/', views.StartLive.as_view()),
    path('stopLive/', views.StopLive.as_view()),
    path('watchLive/', views.WatchLive.as_view()),
    path('logout/', views.Logout.as_view()),
}
