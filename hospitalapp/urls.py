from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ----------------- HOME -----------------
    path('', views.home, name='home'),

    # ----------------- AUTH / REGISTER -----------------
    path('login/', auth_views.LoginView.as_view(template_name='hospitalapp/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('hospital/register/', views.hospital_register, name='hospital_register'),
    path('receiver/register/', views.receiver_register, name='receiver_register'),

    # ----------------- BLOOD SAMPLES -----------------
    path('samples/', views.available_samples, name='available_samples'),
    path('samples/add/', views.add_blood_info, name='add_blood_info'),
    path('samples/request/<int:sample_id>/', views.request_sample, name='request_sample'),

    # ----------------- REQUEST MANAGEMENT -----------------
    path('requests/', views.view_requests, name='view_requests'),
    path('requests/update/<int:request_id>/<str:status>/', views.update_request_status, name='update_request_status'),

    # ----------------- CAMPAIGNS -----------------
    path('campaigns/create/', views.campaign_create, name='campaign_create'),
    path("campaigns/<int:pk>/", views.campaign_detail, name="campaign_detail"),
    path('campaigns/', views.campaign_list, name='campaign_list'),
]
