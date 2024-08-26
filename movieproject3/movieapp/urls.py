from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'movieapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:pk>/edit/', views.edit_movie, name='edit_movie'),
    path('movie/<int:pk>/delete/', views.delete_movie, name='delete_movie'),
    path('movie/<int:pk>/review/', views.add_review, name='add_review'),
    path('categories/<str:category>/', views.movies_by_category, name='movies_by_category'),
    path('search/', views.search, name='search'),
]




