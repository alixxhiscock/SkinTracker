from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('skins/<str:skin_name>/', views.skin,name='skin'),
    path('skins/', views.skins,name='skins'),
    path('search_skins/', views.search_skins, name='search_skins'),
    path('skin_sale/<str:sale_id>', views.skin_sale, name='skin_sale'),
    path('user/<str:username>/', views.user,name='user'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)