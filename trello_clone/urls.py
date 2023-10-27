from django.contrib import admin
from django.urls import path, include
from board.views import index_view  


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='board'),  
    path('accounts/', include('accounts.urls')),
    path('cards/', include('cards.urls')),
    path('board/', include('board.urls')), 
]
