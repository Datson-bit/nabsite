from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard, approve_application, bursary_form, success_page, application_detail, disapprove_application, track_application
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', bursary_form, name='bursary_form'),
    path('dashboard/', dashboard, name="dashboard"),
    path('application/<int:application_id>/', application_detail, name='application_detail'),
    path('application/<int:application_id>/approve', approve_application, name='approve_application'),
    path('application/<int:application_id>/disapprove', disapprove_application, name='disapprove_application'),
    path("track-application/", track_application, name="track_application_page"),
    path("bursary/success/<str:reference_code>/", success_page, name="application_success"),
]