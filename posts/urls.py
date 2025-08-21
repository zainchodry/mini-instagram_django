from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
]
