from django.contrib import admin
from django.urls import path, include
from board.views import index_view, project_detail_view, create_project_view, delete_projet,update_project

app_name = 'board'

urlpatterns = [
    path('', index_view, name='board-index'), 
    path('project/<int:project_id>/', project_detail_view, name='project_detail'),  
    path('create_project/', create_project_view, name='create_project'),  
    path('delete_projet/<int:project_id>/', delete_projet, name='delete_projet'),
    path('update_project/<int:project_id>/', update_project, name='update_project'),
    #path('project/<int:project_id>/cards/', views.project_cards, name='project_cards'),
]
