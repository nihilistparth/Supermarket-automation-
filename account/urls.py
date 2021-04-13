from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.home, name = 'account-home'),
    path('register/',views.register, name='account-register'),
    path('login/',auth_views.LoginView.as_view(template_name="account/login.html"), name='account-login'),
    path('logout/',auth_views.LogoutView.as_view(template_name="account/logout.html"), name='account-logout'),
    path('profile/',views.profile, name="account-profile"),
    path('user/', views.edit_user, name="account-user-edit"),
    path('<int:u_id>/', views.del_user, name="account-user-del"),
]


