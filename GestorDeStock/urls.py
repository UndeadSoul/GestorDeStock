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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from core import views as viewscore
from registerlogin import views as viewsreglog
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', viewscore.home, name='home'),
    path('usermanage', viewscore.usermanage, name='usermanage'),
    path('records', viewscore.records, name='records'),
    path('inventory', viewscore.inventory, name='inventory'),
    path('movestock', viewscore.movestock, name='movestock'),
    path('addstock', viewscore.addStockCreateView.as_view(), name='addstock'),
    path('addproduct', viewscore.addProductCreateView.as_view(), name='addproduct'),
    path('removestock', viewscore.removeStockCreateView.as_view(), name='removestock'),
    path('finalconfirm', viewscore.finalconfirm, name='finalconfirm'),
    # Relación entre las urls y las views de login/register
    path('accounts/login/', viewsreglog.LoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(next_page="login"), name="logout"),
    path('', include("registerlogin.urls")),
    path("custom_redirect/", viewscore.custom_login_redirect, name="custom_login_redirect"),

    # Registro de usuario
    path('adduser/', viewscore.AddUserView.as_view(), name="adduser"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#     document_root=settings.MEDIA_ROOT)
