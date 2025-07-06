from django.urls import path
from . import views

app_name = 'openpage'  # Namespace for the app's URLs

urlpatterns = [
    path('', views.post_list_view, name='post_list'),
    path('post/create/', views.create_post_view, name='create_post'),
    path('post/<int:pk>/', views.post_detail_view, name='post_detail'),
]
