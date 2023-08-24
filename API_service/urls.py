from django.urls import path
from . import views
from .views import stattricksAPI

urlpatterns = [
            path("api2",views.stattricks_api,name="stattricks_api"),
            path("newapi",stattricksAPI.as_view(),name="stattricksAPI")

]