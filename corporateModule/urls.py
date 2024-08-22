from . import views
from django.urls import include, path


urlpatterns = [
     path('', views.home, name='home'),
     path('home_es', views.home_es, name='home_es'),
     path('analysis', views.analysis, name='analysis'),
     path('regulation', views.regulation, name='regulation'),
     path('education', views.education,name='education'),
     path('monitoring', views.monitoring, name='monitoring')
]