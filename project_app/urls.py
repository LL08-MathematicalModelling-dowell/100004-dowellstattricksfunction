from django.urls import path
from . import views

urlpatterns=[
    path('',views.default,name="default"),
    path('form/',views.form,name="form"),
    path('insertData/',views.insertData,name="form"),
    path("dbConnection/",views.dbConnectionTest,name="dbTest"),
    path("fetchForm/",views.fetchDataForm,name="fetchDataForm"),
    path("fetchData/",views.fetchData,name="fetchData")
]