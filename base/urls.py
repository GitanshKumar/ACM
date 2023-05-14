from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= "home"),
    path('event/<str:pk>/', views.event, name= "event"),
    path('aboutus/', views.aboutus, name= "aboutus"),
    path('team/', views.team, name="team"),
    path('profile/<str:pk>', views.profile, name="profile"),
    path('events/', views.events, name="events"),
    path('logout/', views.logoutuser, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.loginuser, name="login"),
    path('edit/', views.edit_profile, name="edit_profile"),
    path('register/<str:pk>/<str:cat>', views.register, name="register"),
    path('viewteam/<str:pk>', views.viewteam, name="viewteam"),
    path('detail/<str:pk>', views.event_details, name="event_detail"),
]