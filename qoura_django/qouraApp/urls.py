from django.urls import path
from . import views


urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('home/',views.home,name="home")
    # Add logout later: path('logout/', auth_views.LogoutView.as_view(), name='logout')
]