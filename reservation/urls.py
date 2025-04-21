from django.urls import path
from reservation.apps import ReservationConfig
from reservation.views import (
    BookTableView,
    HomeView,
    InfoView,
    ReservationCancelView,
    ReservationCreateView,
    ReservationListView,
    ReservationUpdateView,
    ReservationView,
    confirm_booking,
)

app_name = ReservationConfig.name

urlpatterns = [
    path("reservation_list/", ReservationListView.as_view(), name="reservation_list"),
    path("book/", BookTableView.as_view(), name="book_table"),
    path("", HomeView.as_view(), name="home"),
    path("reservation_table/", ReservationCreateView.as_view(), name="reservation_table"),
    path("confirm-booking/<str:token>/", confirm_booking, name="confirm_booking"),
    path("info/", InfoView.as_view(), name="info"),
    path("reservation/<int:pk>/cancel/", ReservationCancelView.as_view(), name="reservation_cancel"),
    path("reservation_detail/<int:pk>/", ReservationView.as_view(), name="reservation_detail"),
    path("reservation_update/<int:pk>/", ReservationUpdateView.as_view(), name="reservation_update"),
]
