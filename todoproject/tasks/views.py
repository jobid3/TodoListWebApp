from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, MajorTaskForm, SubTaskForm
from .models import MajorTask, SubTask
from django.db.models import Count, Q

def home(request):
    return redirect('tasks') if request.user.is_authenticated else redirect('login')

@login_required
def tasks(request):
    if request.method == 'POST':
        form = MajorTaskForm(request.POST)
        if form.is_valid():
            mt = form.save(commit=False)
            mt.user = request.user
            mt.save()
            return redirect('tasks')
    else:
        form = MajorTaskForm()
    
    major_tasks = MajorTask.objects.filter(user=request.user).annotate(
        subtask_count=Count('subtasks'),
        completed_subtask_count=Count('subtasks', filter=Q(subtasks__is_completed=True))
    )
    
    return render(request, 'tasks/major_tasks_list.html', {
        'major_tasks': major_tasks,
        'form': form
    })

@login_required
def task_detail(request, user_task_id):
    major_task = get_object_or_404(MajorTask, user=request.user, user_task_id=user_task_id)
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
def task_update(request, user_task_id):
    major_task = get_object_or_404(MajorTask, user=request.user, user_task_id=user_task_id)
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    form = MajorTaskForm(request.POST, instance=major_task)
    if form.is_valid():
        form.save()
    return redirect('task_detail', user_task_id=user_task_id)

@login_required
def task_delete(request, user_task_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    major_task = get_object_or_404(MajorTask, user=request.user, user_task_id=user_task_id)
    major_task.delete()
    return redirect('tasks')

@login_required
def subtask_create(request, user_task_id):
    major_task = get_object_or_404(MajorTask, user_task_id=user_task_id, user=request.user)
    if request.method == 'POST':
        form = SubTaskForm(request.POST)
        if form.is_valid():
            st = form.save(commit=False)
            st.major_task = major_task
            st.save()  # task_subtask_id auto-assigned
    return redirect('task_detail', user_task_id=user_task_id)


@login_required
def subtask_update(request, user_task_id, task_subtask_id):
    major_task = get_object_or_404(MajorTask, user_task_id=user_task_id, user=request.user)
    subtask = get_object_or_404(SubTask, task_subtask_id=task_subtask_id, major_task=major_task)
    if request.method == 'POST':
        form = SubTaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
    return redirect('task_detail', user_task_id=user_task_id)


@login_required
def subtask_delete(request, user_task_id, task_subtask_id):
    major_task = get_object_or_404(MajorTask, user_task_id=user_task_id, user=request.user)
    subtask = get_object_or_404(SubTask, task_subtask_id=task_subtask_id, major_task=major_task)
    if request.method == 'POST':
        subtask.delete()
    return redirect('task_detail', user_task_id=user_task_id)

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