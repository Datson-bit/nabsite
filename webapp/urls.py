from django.urls import path

from .views import home, about, contact, gallery,newsletter_subscribe, video, blog, events, service, event_detail, registration_success, causes, donation, custom_404_test, test,members, executives,  blog_view, parliamentary, video, vidtext
urlpatterns = [
    path('', home, name='home'),
    path('test/', test),
    path("blog/", blog, name='blog'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('events/', events, name='events'),
    path('gallery/', gallery, name='gallery'),
    path('video/', video, name='video'),
    path('vidtext/', vidtext, name='vidtext'),
    path('service/', service, name='service'),
    path('causes/', causes, name='causes'),
    path('executives/', executives, name='executives'),
    path('parliamentary/', parliamentary, name='team_spc'),
    path('donation/', donation, name='donation'),
    path('error_404/', custom_404_test, name='error_404'),
    path('members/', members, name='members'),
    path('blog/<int:pk>/', blog_view, name="view"),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('registration-success/<int:registration_id>/', registration_success, name='registration_success'),
    path('subscribe/', newsletter_subscribe, name="newsletter_subscribe"),
    
]