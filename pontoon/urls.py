from django.urls import path
from . import views

urlpatterns = [

    # Pontoon game routes
    path(
        "",
        views.pontoon_home,
        name="pontoon_home",
    ),

    path(
        "select/<int:ball_id>/",
        views.select_ball,
        name="select_ball",
    ),

    path(
        "confirm/<int:ball_id>/",
        views.confirm_ball,
        name="confirm_ball",
    ),

    # Payment routes
    path(
        "checkout/",
        views.pontoon_checkout,
        name="pontoon_checkout",
    ),

    path(
        "payment-success/",
        views.pontoon_payment_success,
        name="pontoon_payment_success",
    ),

]