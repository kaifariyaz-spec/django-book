from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('',views.movie_list,name ='movie_list'),
    path('<int:movie_id>/theaters/',views.theater_list,name ='theater_list'),
    path('theater/<int:theater_id>/seats/book/',views.book_Seats,name ='book_Seats'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)