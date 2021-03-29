from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('accounts/sign_up/', views.registerPage, name="sign-up"),
    path('accounts/login/', views.loginPage, name="log-in"),
    path('staff/post_numbers/', views.num_post, name="post-numbers"),
    path('staff/staff_index/', views.staff_index, name="staff-index"),
    path('utente/<int:pk>/', views.user_profile, name="profilo-utente"),
    path('staff/json/', views.last_hour, name="json-response"),
    path('staff/search/', views.search, name='search'),
    ]