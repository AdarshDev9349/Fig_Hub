from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.home,name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/",views.signup,name='signup'),
    path('accounts/logout/', views.logout, name='logout'),
    path('form',views.profile,name="profile"),
    path("search",views.search,name='search'),
    path("user",views.searchuser,name="searchuser"),
    path('v',views.render_figma_image,name='render_figma_image'),
 
]
