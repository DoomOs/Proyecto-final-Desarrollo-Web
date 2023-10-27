from django.urls import path

from cards.views import CardListView, CardView, ItemListView, ItemView, TagListView, TagView, project_cards, item_tags_view, manage_item_tags_view, moved_object_view


app_name = 'cards'
urlpatterns = [
    path('cards/<int:project_id>', CardListView.as_view(), name='card-list'),
    path('card/<str:uuid>', CardView.as_view(), name='card'),

    path('card/<str:uuid>/items', ItemListView.as_view(), name='items-list'),
    path('item/<str:uuid>', ItemView.as_view(), name='item'),

    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tag/<str:uuid>', TagView.as_view(), name='tag'),


    path('item/<str:uuid>/tags/', item_tags_view, name='item-tags'),
    path('item/<str:uuid>/tags/update', manage_item_tags_view, name='update-item-tags'),
    path('moved/', moved_object_view, name='moved-object'),

    path('project/<int:project_id>/cards/', project_cards, name='project-cards'),
]