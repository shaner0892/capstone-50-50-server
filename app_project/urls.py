"""app_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from rest_framework import routers
from django.urls import path
from app_api.views import register_user, login_user
from app_api.views.activity import ActivityView
from app_api.views.category import CategoryView
from app_api.views.city import CityView
from app_api.views.fifty_user import FiftyUserView
from app_api.views.state import StateView
from app_api.views.trip import TripView


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'categories', CategoryView, 'category')
router.register(r'trips', TripView, 'trip')
router.register(r'fiftyusers', FiftyUserView, 'fiftyuser')
router.register(r'states', StateView, 'state')
router.register(r'cities', CityView, 'city')
router.register(r'activities', ActivityView, 'activity')





urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
]
