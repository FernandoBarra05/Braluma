from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_narrative_view, name='home'),
    path('coleccion/', views.coleccion_catalog_view, name='coleccion'),
    path('espejo/<slug:slug>/', views.product_detail_view, name='espejo_detail'),
    path('panel/metricas/', views.dashboard_metricas_view, name='dashboard_metricas'),
]
