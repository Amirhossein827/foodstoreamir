from django.urls import path
from accounts import views


urlpatterns = [

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user.get_user_data, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    path('register/sent_otp/',views.register_user.get_otp,name='send_otp')

]
