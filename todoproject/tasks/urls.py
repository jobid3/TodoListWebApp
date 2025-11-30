from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    # MajorTasks
    path('tasks/', views.tasks, name='tasks'),  # list + create
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),

    # SubTasks
    path('tasks/<int:task_pk>/subtasks/create/', views.subtask_create, name='subtask_create'),
    path('tasks/<int:task_pk>/subtasks/<int:pk>/edit/', views.subtask_update, name='subtask_update'),
    path('tasks/<int:task_pk>/subtasks/<int:pk>/delete/', views.subtask_delete, name='subtask_delete'),
]
