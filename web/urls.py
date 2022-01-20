from django.contrib import admin
from django.urls import path, include
from hotdeal import views
from rest_framework import routers
import hotdeal.views

router = routers.DefaultRouter()
router.register("deals", hotdeal.views.DetailViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/', include(router.urls))
]
