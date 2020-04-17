from django.urls import path, include
from . import views
from rest_framework_swagger.views import get_swagger_view
# from rest_framework.permissions import AllowAny
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
from rest_framework_jwt.views import obtain_jwt_token

schema_view = get_swagger_view(title="API 문서")

app_name = "arti_intelli"
urlpatterns = [
    path('test/', views.test),
    path('account/', views.AddAccount.as_view()),
    path('recognition/', views.Recognition.as_view()),
    path('api-token-auth/', obtain_jwt_token),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('checks/out_calling/', views.out_calling, name="out_calling"),
    path('checks/in_calling/', views.in_calling, name="in_calling"),
    path('checks/notall/', views.not_allclick, name="not_allclick"),
    path('checks/notout/', views.not_outclick, name="not_outclick"),
    path('checks/notin/', views.not_inclick, name="not_inclick"),
    path('checks/', views.check_on, name="check_on"),
    path('accounts/', views.account_list, name="accounts_list"),
    path('campus/', views.campus_list, name="campus_list"),
    path('docs/', schema_view),
]
