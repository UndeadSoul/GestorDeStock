"""
URL configuration for GestorDeStock project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views as viewscore


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', viewscore.home, name='home'),
    path('usermanage', viewscore.usermanage, name='usermanage'),
    path('records', viewscore.records, name='records'),
    path('inventory', viewscore.inventory, name='inventory'),
    path('movestock', viewscore.movestock, name='movestock'),
    path('addstock', viewscore.addstock, name='addstock'),
    path('addproduct', viewscore.addproduct, name='addproduct'),
    path('removestock', viewscore.removestock, name='removestock'),
    path('confirmremove', viewscore.confirmremove, name='confirmremove'),
    path('finalconfirm', viewscore.finalconfirm, name='finalconfirm'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)