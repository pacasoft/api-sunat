from django.urls import path

from sunat import views

urlpatterns = [
    path('ruc/<str:numero>', views.RUCDetail.as_view()),
    path('dni/<str:numero>', views.DNIDetail.as_view()),
    path('get_padron', views.export_to_sqlite)

]
