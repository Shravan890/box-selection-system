from django.urls import path
from . import views

urlpatterns = [path("", views.home, name="home"), path("orders/<int:pk>/", views.order_detail, name="order_detail")]
