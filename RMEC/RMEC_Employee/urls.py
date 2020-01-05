from django.urls import path
from .views import ProfileUpdateView,CustomLoginView,CustomPasswordResetView,participants_hired,IndustrypartnerDelete,IndustrypartnerUpdate,IndustrypartnerlistView,participants_nothired,UsersView,UsersUpdate,UsersDelete,DashboardView,RMEC_EmployeeDelete
from RMEC_Employee import views
from django.contrib.auth.views import LoginView,PasswordResetCompleteView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView

urlpatterns = [
    path('partner_registration/', views.IndustryPartnerRegistration, name='IndustryPartnerRegistration'),
    path('dashboard/', views.Main, name='dashboard'),
    path("logout", views.logout_request, name="logout_request"),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('thankyou/', views.Thankyou, name='thankyou'),
    path('settings/',views.Setting_rmec, name='settings'),
    path('', DashboardView.as_view(), name='participants_list'),
    path('delete/<int:pk>',RMEC_EmployeeDelete.as_view(),name='RMEC_Employee_confirm_delete'),
    path('participants_add/',views.participantsAdd,name='participants_add'),
    path('participants_update/<int:pk>',views.RMEC_EmployeeUpdate,name='participants_update'),
    path('csv-upload',views.RMEC_Employee_upload,name='RMEC_Employee_upload'),
    path('csv-download',views.RMEC_Employee_download,name='RMEC_Employee_download'),
    path('users/', UsersView.as_view(), name='users'),
    path('industry_partners_list/', IndustrypartnerlistView.as_view(), name='IndustrypartnerlistView'),
    path('users/new', views.AdminRegistration, name='AdminRegistration'),
    path('users/update/<int:pk>',UsersUpdate.as_view(),name='user_update_form'),
    path('users/delete/<int:pk>',UsersDelete.as_view(),name='user_confirm_delete'),
    path('participants/', participants_nothired.as_view(), name='not_hired'),
    path('hiredby_partner/', participants_hired.as_view(), name='hiredby_partner'),
    path('password_change/', views.change_password, name='change_password'),
    path('login_success/', views.login_success, name='login_success'),
    path('hired_status/<int:pk>', views.hired_status, name='hired_status'),
    path('hired_status_none/<int:pk>', views.hired_status_none, name='hired_status_none'),
    path('profile_update/<int:pk>',ProfileUpdateView.as_view(), name='profile_update'),
    path('password_reset/',CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/',PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('industrypartner/update/<int:pk>',IndustrypartnerUpdate.as_view(),name='IndustrypartnerUpdate'),
    path('industrypartner/delete/<int:pk>',IndustrypartnerDelete.as_view(),name='IndustrypartnerDelete'),
    # path('export_data/', views.export_data ,name='export_data'),
    path('export/', views.export_data_template ,name='export_data_template'),
    
]