from django.urls import path, include
from . import views
from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import obtain_jwt_token

schema_view = get_swagger_view(title="API 문서")

app_name = "arti_intelli"
urlpatterns = [
    path('add/data/', views.add_data, name="add_data"),
    path('add/account/', views.AddAccount.as_view(), name="add_account"),
    path('recognition/', views.Recognition.as_view(), name="recognition"),
    path('add/campus/', views.add_campus),
    path('api-token-auth/', obtain_jwt_token),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('checks/c_attend/<int:pk1>/<int:pk2>/<int:pk3>/', views.classes_attendance, name="classes_attendance"),
    path('checks/notall/<int:pk1>/<int:pk2>/<int:pk3>/', views.not_allclick, name="not_allclick"),
    path('checks/notout/<int:pk1>/<int:pk2>/<int:pk3>/', views.not_outclick, name="not_outclick"),
    path('checks/notin/<int:pk1>/<int:pk2>/<int:pk3>/', views.not_inclick, name="not_inclick"),
    path('checks/daily/<int:pk1>/<int:pk2>/<int:pk3>/', views.check_on_daily, name="check_on_daily"),
    path('checks/month/student/<pk1>/<int:pk2>/<int:pk3>/', views.check_on_month_one, name="check_on_month_one"),
    path('checks/month/all/<int:pk1>/<int:pk2>/', views.check_on_month_all, name="check_on_month_all"),
    path('checks/month/<int:pk1>/<int:pk2>/<int:pk3>/<int:pk4>/<int:pk5>/', views.check_on_month, name="check_on_month"),
    path('checks/', views.check_on, name="check_on"),
    path('accounts/<int:pk1>/<int:pk2>/', views.account_list_region, name="account_list_region"),
    path('accounts/', views.account_list, name="accounts_list"),
    path('campus/', views.campus_list, name="campus_list"),
    path('docs/', schema_view),
]
