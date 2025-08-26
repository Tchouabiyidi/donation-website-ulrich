from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MeView,
    LogoutView,
    UsersListView,
    UserDeleteView,
    CampaignCreateView,
    CampaignPendingListView,
    CampaignValidateView,
    CampaignApprovedListView,
    NotificationListView,
    NotificationReadToggleView,
    NotificationDeleteView,
    # Payments (Campay)
    CampayCollectView,
    CampayWebhookView,
)

urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/me/', MeView.as_view(), name='me'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/', UsersListView.as_view(), name='users-list'),
    path('users/<int:pk>/', UserDeleteView.as_view(), name='users-delete'),
    path('campaigns/', CampaignCreateView.as_view(), name='campaigns-create'),
    path('campaigns/pending/', CampaignPendingListView.as_view(), name='campaigns-pending'),
    path('campaigns/<int:pk>/validate/', CampaignValidateView.as_view(), name='campaigns-validate'),
    path('campaigns/approved/', CampaignApprovedListView.as_view(), name='campaigns-approved'),
    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notifications-list'),
    path('notifications/<int:pk>/toggle-read/', NotificationReadToggleView.as_view(), name='notifications-toggle-read'),
    path('notifications/<int:pk>/', NotificationDeleteView.as_view(), name='notifications-delete'),
    # Payments - Campay
    path('payments/campay/collect', CampayCollectView.as_view(), name='campay-collect'),
    path('payments/campay/webhook/', CampayWebhookView.as_view(), name='campay-webhook'),
]