from django.urls import path
from . import views


urlpatterns = [
    path('api/signup/', views.signup, name='signup'),
    path('api/login/', views.login, name='login'),
    path('api/logout/', views.logout_view, name='logout'),
    path('api/profile/', views.profile_view, name='profile'),
    path('api/add_project/', views.add_project, name='add_project'),
    path('api/search_users/', views.search_users, name='search_users'),
    path('api/view_profile/<int:user_id>/', views.view_profile, name='view_profile'),
]

