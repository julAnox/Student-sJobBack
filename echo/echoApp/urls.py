from django.urls import path
from . import views

urlpatterns = [
    # Countries and Regions
    path('countries/', views.get_countries, name='get_countries'),

    # Comments
    path('comments/', views.comments, name='comments'),

    # Vacancies
    path('vacancies/', views.vacancies, name='vacancies'),
    path('vacancies/<int:pk>/', views.vacancy, name='vacancy'),

    # Filter Vacancies
    path('vacancies/filter/', views.filter_vacancies, name='filter_vacancies'),

    # Summaries
    path('summaries/', views.summaries, name='summaries'),
    path('summaries/<int:pk>/', views.summary, name='summary'),

    # Login
    path('login/', views.login, name='login'),

    # Signup
    path('signup/', views.signup, name='signup'),

    # User Profile
    path('profile/', views.profile, name='profile'),

    # My Summaries
    path('my_summaries/', views.my_summaries, name='my_summaries'),

    # Create Summary
    path('create_summary/', views.create_summary, name='create_summary'),

    # Company Management
    path('add_company/', views.add_company, name='add_company'),
    path('my_company/', views.my_company, name='my_company'),
]
