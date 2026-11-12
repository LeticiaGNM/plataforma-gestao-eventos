from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/<int:pk>/', views.detalhe_evento, name='detalhe_evento'),
    path('eventos/<int:pk>/inscrever/', views.inscrever, name='inscrever'),
    path('eventos/<int:pk>/cancelar/', views.cancelar_inscricao, name='cancelar_inscricao'),
    path('minhas-inscricoes/', views.minhas_inscricoes, name='minhas_inscricoes'),
]