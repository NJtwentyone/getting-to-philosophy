from django.conf.urls import url, include
#from django.urls import path
from rest_framework import routers
from philosophyrest.core import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^wiki/degreeOfSeperation/path/', views.DegreeOfSeperationPath, ),
    url(r'^wiki/degreeOfSeperation/find/', views.DegreeOfSeperationFind, ),
    url(r'^wiki/degreeOfSeperation/status/', views.DegreeOfSeperationStatus, ),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
