from django.contrib import admin
from django.urls import (
    path,
    include,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('pairs/', include(('pairs.urls', 'pairs'), namespace='pairs')),
]
