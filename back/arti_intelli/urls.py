from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view


app_name = "arti_intelli"
urlpatterns = [
    # path('/', views.index, name="main"),
    # path('all/', views.all, name="management"),
    path('rocog/', views.recognition, name="recognition"),
]
