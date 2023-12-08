from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.login_view, name="login_path"),
    path('home/', views.home_view, name="home_path"),
    path('signup/', views.register_view, name='signup')           

]