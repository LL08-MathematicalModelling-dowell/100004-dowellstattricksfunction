from django.urls import path
from . import views
from .views import uploadfileform, uploadfile
from .api import publicAPI, stattricksAPI

urlpatterns=[
    path('',views.default,name="default"),
    path('form/',views.form,name="form"),
    path('insertQrImageData/',views.insertQrImageData,name="insertQrImageData"),
    path("fetchQrImageDataForm/",views.fetchDataForm,name="fetchDataForm"),
    # path("fetchQrImageData/",views.fetchData,name="fetchData"),
    path("fetchDataForm/",views.fetchDataForm,name="fetchDataForm"),
    path("fetchData/",views.fetchData,name="fetchData"),
    path("uploadfileform/",views.uploadfileform,name="uploadfileform"),
    path("uploadfile/",views.uploadfile,name="uploadfile"),
    path('uploadfile/', uploadfileform, name='uploadfileform'),
    path('uploadfile/upload/', uploadfile, name='uploadfile'),


    #API ROUTES
    path("oldapi",views.stattricks_api,name="stattricks_api"),
    path("api",publicAPI.as_view(),name="publicAPI"),
    path("processapi",stattricksAPI.as_view(),name="stattricksAPI"),
]