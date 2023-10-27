
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import django.views as views
from django.contrib.auth.mixins import LoginRequiredMixin
from sklearn import logger
from cards.forms import ItemDescriptionForm, TagForm
from board.models import Project
from django.template.loader import render_to_string
from cards.models import Card, Item, Tag

# Create your views here.
@login_required
def index_view(request,project_id):
    project = get_object_or_404(Project, pk=project_id)  
    cards = Card.objects.filter(project=project).order_by('order')
    tags_form = TagForm()
    return render(request, 'cards/index.html', {'cards': cards, 'tags_form': tags_form, 'project': project})


@login_required
def project_cards(request, project_id):
    project = get_object_or_404(Project, pk=project_id)  
    cards = Card.objects.filter(project=project).order_by('order')
    tags_form = TagForm()
    return render(request, 'cards/index.html', {'cards': cards, 'tags_form': tags_form, 'project': project})


class CardListView(LoginRequiredMixin, views.View):
   def post(self, request, project_id):
    try:
        title = request.POST.get('newcard', '')

        if title:
            project = get_object_or_404(Project, id=project_id)
            card = Card.objects.create(title=title, project=project)
            return render (request,'cards/partials/card.html', {'card': card} )   
        else:
            return HttpResponseBadRequest("Titulo vacío")
    except Exception as e:
        print(f"Error en la vista CardListView: {str(e)}")
        logger.error(f"Error en la vista CardListView: {str(e)}")
        return HttpResponseServerError("Error interno del servidor")

class CardView(LoginRequiredMixin, views.View):

    def get(self, request, uuid):
        card = get_object_or_404(Card, uuid=uuid)
        return render(request, 'cards/partials/card.html', {'card': card})


    def delete(self, request, uuid):

        card = get_object_or_404(Card, uuid=uuid)

        # movemos el objeto a la última posición para que se actualice el orden de las demás cards
        Card.objects.move(card, card.get_max_order() + 1)
        card.delete()
        return HttpResponse()

class ItemListView(LoginRequiredMixin, views.View):

    def get(self, request, uuid):
        card = get_object_or_404(Card, uuid=uuid)
        items = card.get_items()

        if 'tag-filter-item' in request.GET.keys():
            for tag in request.GET.getlist('tag-filter-item'):
                items = items.filter(tags__uuid__contains=tag)

        return render(request, 'cards/partials/item.html', {'items': items})

    def post(self, request, uuid):
        card = get_object_or_404(Card, uuid=uuid)

        item_title = request.POST[f'newitem-{uuid}']
        if len(item_title) > 0:
            item = Item.objects.create(title=item_title, card=card)
            item.save()

            # volvemos a renderizar la plantilla de elementos de la tarjeta, de modo que, en el html, 
            # podamos seleccionar el último elemento y agregarlo a la interfaz de usuario
            return render(request, 'cards/partials/item.html', {'items': card.get_items()})
        else:
            return HttpResponse()


class ItemView(LoginRequiredMixin, views.View):

    def get(self, request, uuid):
        item = get_object_or_404(Item, uuid=uuid)
        description_form = ItemDescriptionForm(None, instance=item)

        context = {'item': item, 'description_form': description_form}
        return render(request, 'cards/partials/item-details.html', context)

    def put(self, request, uuid):
        data = QueryDict(request.body)
        item = get_object_or_404(Item, uuid=uuid)

        description_form = ItemDescriptionForm(data, instance=item)
        if description_form.is_valid():
                description_form.save()
            
        return HttpResponse()

    def delete(self, request, uuid):
        item = get_object_or_404(Item, uuid=uuid)

        # movemos el objeto a la última posición para que se actualice el orden de los demás elementos
        Item.objects.move(item, item.get_max_order() + 1)
        item.delete()

        return HttpResponse()


class TagListView(LoginRequiredMixin, views.View):
    
    def get(self, request):
        tags = Tag.objects.filter(user=request.user)
        return render(request, 'cards/partials/user-tags.html', {'tags': tags})

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
        response = HttpResponse()
        response['HX-Trigger-After-Settle'] = 'tag-added'
        return response

class TagView(LoginRequiredMixin, views.View):
    def delete(self, request, uuid):
        tag = get_object_or_404(Tag, uuid=uuid)
        if tag is not None:
            tag.delete()

        response = HttpResponse()
        response['HX-Trigger-After-Settle'] = 'tag-deleted'
        return response


@login_required
def manage_item_tags_view(request, uuid):
    item = get_object_or_404(Item, uuid=uuid)
    selected_tags = request.POST.getlist('tag-update-item')
    all_tags = request.user.tag.all()

    for tag in all_tags:
        if str(tag.uuid) in selected_tags and tag not in item.tags.all():
            item.tags.add(tag)

        elif str(tag.uuid) not in selected_tags and tag in item.tags.all():
            item.tags.remove(tag)

    response = HttpResponse()
    response['HX-Trigger-After-Settle'] = f'item-{item.uuid}-tags-update'
    return response


@login_required
def item_tags_view(request, uuid):
    item = get_object_or_404(Item, uuid=uuid)
    return render(request, 'cards/partials/item-tags.html', {'item': item})


@login_required
def moved_object_view(request):

    object_uuid = request.POST['movedItem']
    new_order = int(request.POST['order']) + 1

    if object_uuid.startswith('item-'):
        item = get_object_or_404(Item, uuid=object_uuid.replace('item-', ''))

        if request.POST['fromCard'] != request.POST['toCard']:
            Item.objects.move(item, item.get_max_order())

            item.card = get_object_or_404(Card, uuid=request.POST['toCard'].replace('parent-card-', ''))
            item.order = item.get_max_order() + 1
            item.save()
        
        Item.objects.move(item, new_order)

    elif object_uuid.startswith('card-'):
        card = get_object_or_404(Card, uuid=object_uuid.replace('card-', ''))
        Card.objects.move(card, new_order)

    return HttpResponse()

