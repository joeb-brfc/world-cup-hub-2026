from django.contrib import admin
from django.urls import path, include

# Project URL routes
urlpatterns = [
    path("admin/", admin.site.urls),

    # Prediction application
    path("", include("predictor.urls")),

    # Pontoon competition
    path("pontoon/", include("pontoon.urls")),

    # User authentication
    path("accounts/", include("allauth.urls")),
]