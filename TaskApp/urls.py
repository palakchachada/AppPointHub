from django.urls import path,include
from .views import *

urlpatterns = [
    path("login/",login_page,name="login"),
    path("",home_page,name='home_page'),
    path('add_points/', add_points, name='add_points'),
    path('register/',register,name='register'),
    path('add_user/',add_user,name='add_user'),
    path('submit_points/',submit_points,name='submit_points'),
    path('all_users/',all_users,name='all_users'),
    path('delete_user/<slug:cust_user_id>/',delete_user,name='delete_user'),
    path('user_details/',user_details,name='user_details'),
    path('admin_logout/',admin_logout,name='logout'),
    path('change_role/',change_role,name='change_role'),
    path('task_details/<str:app_name>/',task_details,name='task_details'),
    # path("user_profile/",user_profile, name='user_profile'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('change_password/',change_password,name='change_password'),

]
