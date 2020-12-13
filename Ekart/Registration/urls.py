from django.urls import path
from Registration import views
app_name = 'Registration'
urlpatterns = [
    path('Register/',views.register,name = 'register'),
    path('user_login/',views.user_login,name = 'user_login'),
    path('user_logout/',views.user_logout,name = 'user_logout'),
    path('profileinfo/<uname>/',views.profileinfo,name = 'profile'),
    path('forget_password/',views.forget_password,name='forget_password'),
]
