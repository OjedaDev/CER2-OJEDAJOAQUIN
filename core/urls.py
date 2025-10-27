
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('evento/<int:evento_id>/', views.evento_detalle, name='evento_detalle'),
    path('inscribir/<int:evento_id>/', views.inscribir_evento, name='inscribir_evento'),
    path('mis-eventos/', views.mis_eventos, name='mis_eventos'),
    path('anular/<int:inscripcion_id>/', views.anular_inscripcion, name='anular_inscripcion'),
]