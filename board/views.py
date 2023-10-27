
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .models import Project
from .forms import ProjectForm
from django.shortcuts import render
from board.models import Project
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def index_view(request):
    user_projects = Project.objects.filter(board__user=request.user)
    project_form = ProjectForm()

    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.board = request.user.board
            project.save()
            return redirect('board:board-index')

    return render(request, 'board/index.html', {'user_projects': user_projects, 'project_form': project_form})
@login_required
def project_detail_view(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'board/project_detail.html', {'project': project})


@login_required
def project_cards(request, project_id):
    project = Project.objects.get(id=project_id)
    cards = project.card_set.all()

    return render(request, 'board/project_cards.html', {'project': project, 'cards': cards})

@login_required
def create_project_view(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.board = request.user.board
            project.save()
            return redirect('board:index')
    else:
        project_form = ProjectForm()

    return render(request, 'board/create_project.html', {'project_form': project_form})

from django.shortcuts import get_object_or_404, redirect
@login_required
def delete_projet(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, 'El proyecto se ha eliminado exitosamente.')
    return redirect('board:board-index')

@csrf_exempt
def update_project(request, project_id):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        new_description = request.POST.get('new_description')
        
        # Realiza la lógica para actualizar el proyecto en tu base de datos
        try:
            project = Project.objects.get(id=project_id)
            project.name = new_name
            project.description = new_description
            project.save()
            return JsonResponse({'success': True})
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'El proyecto no existe.'})

    return JsonResponse({'success': False, 'error': 'Método no permitido.'})