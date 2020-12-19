
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('fetchFGSMAttack', views.fetchFGSMAttack, name='fetchFGSMAttack'),
    path('fetchOnePixelAttackPredict', views.fetchOnePixelAttackPredict,
         name='fetchOnePixelAttackPredict'),
    path('fetchOnePixelAttack', views.fetchOnePixelAttack,
         name='fetchOnePixelAttack'),
    path('fetchCWAttack', views.fetchCWAttack,
         name='fetchCWAttack'),
    path('fetchBIAttack', views.fetchBIAttack,
         name='fetchBIAttack'),
]
