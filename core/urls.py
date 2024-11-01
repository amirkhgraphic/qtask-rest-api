from django.contrib import admin
from django.urls import (
    path,
    include,
)

from drf_spectacular import views

urlpatterns = [
    # django admin panel
    path('admin/', admin.site.urls),

    # apps endpoints
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('pairs/', include(('pairs.urls', 'pairs'), namespace='pairs')),

    # documentation endpoints
    path('api/schema/', views.SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger-ui/', views.SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', views.SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
