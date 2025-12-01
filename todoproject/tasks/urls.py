from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:user_task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:user_task_id>/update/', views.task_update, name='task_update'),
    path('tasks/<int:user_task_id>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:user_task_id>/subtasks/create/', views.subtask_create, name='subtask_create'),
    path('tasks/<int:user_task_id>/subtasks/<int:task_subtask_id>/update/', views.subtask_update, name='subtask_update'),
    path('tasks/<int:user_task_id>/subtasks/<int:task_subtask_id>/delete/', views.subtask_delete, name='subtask_delete'),
]
