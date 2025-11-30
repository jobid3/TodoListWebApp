from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, MajorTaskForm, SubTaskForm
from .models import MajorTask, SubTask

def home(request):
    return redirect('tasks') if request.user.is_authenticated else redirect('login')

@login_required
def tasks(request):
    if request.method == 'POST':
        form = MajorTaskForm(request.POST)
        if form.is_valid():
            mt = form.save(commit=False)
            mt.owner = request.user
            mt.save()
            return redirect('tasks')
    else:
        form = MajorTaskForm()
    major_tasks = MajorTask.objects.filter(owner=request.user)
    return render(request, 'tasks/major_tasks_list.html', {'form': form, 'major_tasks': major_tasks})

@login_required
def task_detail(request, pk):
    major_task = get_object_or_404(MajorTask, pk=pk, owner=request.user)
    return render(
        request,
        'tasks/major_task_detail.html',
        {
            'major_task': major_task,
            'subtasks': major_task.subtasks.all(),
            'subtask_form': SubTaskForm(),
            'edit_form': MajorTaskForm(instance=major_task),
        },
    )

@login_required
def task_update(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    major_task = get_object_or_404(MajorTask, pk=pk, owner=request.user)
    form = MajorTaskForm(request.POST, instance=major_task)
    if form.is_valid():
        form.save()
    return redirect('task_detail', pk=pk)

@login_required
def task_delete(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    major_task = get_object_or_404(MajorTask, pk=pk, owner=request.user)
    major_task.delete()
    return redirect('tasks')

@login_required
def subtask_create(request, task_pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    major_task = get_object_or_404(MajorTask, pk=task_pk, owner=request.user)
    form = SubTaskForm(request.POST)
    if form.is_valid():
        st = form.save(commit=False)
        st.major_task = major_task
        st.save()
    return redirect('task_detail', pk=task_pk)

@login_required
def subtask_update(request, task_pk, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    major_task = get_object_or_404(MajorTask, pk=task_pk, owner=request.user)
    subtask = get_object_or_404(SubTask, pk=pk, major_task=major_task)
    form = SubTaskForm(request.POST, instance=subtask)
    if form.is_valid():
        form.save()
    return redirect('task_detail', pk=task_pk)

@login_required
def subtask_delete(request, task_pk, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    major_task = get_object_or_404(MajorTask, pk=task_pk, owner=request.user)
    subtask = get_object_or_404(SubTask, pk=pk, major_task=major_task)
    subtask.delete()
    return redirect('task_detail', pk=task_pk)

def login(request):
    if request.user.is_authenticated:
        return redirect('tasks')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        auth_login(request, form.get_user())
        return redirect('tasks')
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('tasks')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        auth_login(request, user)
        return redirect('tasks')
    return render(request, 'register.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')