from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('home/',views.home,name="home"),
    path('question/<int:question_id>/vote/<str:vote_type>/', views.vote_question, name='vote_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('answer/<int:answer_id>/vote/<str:vote_type>/', views.vote_answer, name='vote_answer'),
    path('question/<int:question_id>/answer/', views.post_answer, name='post_answer'),
    path('question/<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('answer/<int:pk>/edit/', views.edit_answer, name='edit_answer'),
    path('answer/<int:pk>/delete/', views.delete_answer, name='delete_answer'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout')
]