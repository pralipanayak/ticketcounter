from django.urls import path
from . import views

urlpatterns = [
    path('', views.Tickets.as_view()),
    path('<ticketNo>', views.Ticket.as_view()),
]