from django.urls import path
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from .import views


def forzar_400(request):
    raise SuspiciousOperation("Prueba 400")

def forzar_403(request):
    raise PermissionDenied("Prueba 403")

def forzar_500(request):
    return 1 / 0

urlpatterns = [
    path('', views.index ,name='index'),
    path('', views.index, name='index'),
    path('test-400/', forzar_400),
    path('test-403/', forzar_403),
    path('test-500/', forzar_500),
]