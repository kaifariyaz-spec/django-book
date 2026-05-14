
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from movies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('',include('users.urls')),
    path('movies/', include('movies.urls')),
    path('payment/',views.payment_page,name='payment'),
    path('payment-success/',views.payment_success,name='payment_success'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
