from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view


app_name = "arti_intelli"
urlpatterns = [
    path('test/', views.test),
    path('account/', views.AddAccount.as_view()),
    path('recognition/', views.Recognition.as_view()),
    
]
