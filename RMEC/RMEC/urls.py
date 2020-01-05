from django.contrib import admin
from django.urls import include, path



urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('', include('RMEC_Employee.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]


 
   