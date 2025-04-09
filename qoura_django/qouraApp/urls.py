from django.urls import path
from . import views


urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('home/',views.home,name="home"),
    path('question/<int:question_id>/vote/<str:vote_type>/', views.vote_question, name='vote_question'),
    path('answer/<int:answer_id>/vote/<str:vote_type>/', views.vote_answer, name='vote_answer'),
    # Add logout later: path('logout/', auth_views.LogoutView.as_view(), name='logout')
]