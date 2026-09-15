from django.urls import path

from app.apps.booking.views import BookingCreateView
from app.apps.contract.views import ContractListView
from app.apps.favorites.views import FavoriteListView, FavoriteStateView
from app.apps.properties.views import PropertyDelistView, PropertyDetailView, PropertyListView
from app.apps.repair.views import RepairTicketView
from app.apps.users.views import LoginView, MeView

urlpatterns = [
    path('api/auth/login/', LoginView.as_view()),
    path('api/auth/me/', MeView.as_view()),
    path('api/properties/', PropertyListView.as_view()),
    path('api/properties/<int:property_id>/', PropertyDetailView.as_view()),
    path('api/properties/<int:property_id>/delist/', PropertyDelistView.as_view()),
    path('api/favorites/', FavoriteListView.as_view()),
    path('api/favorites/<int:property_id>/', FavoriteStateView.as_view()),
    path('api/bookings/', BookingCreateView.as_view()),
    path('api/contracts/', ContractListView.as_view()),
    path('api/repairs/', RepairTicketView.as_view()),
]
