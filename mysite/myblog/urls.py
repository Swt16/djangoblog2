from django.urls import path
from .views import detail_view, edit_view, list_view

urlpatterns = [
    path('', list_view, name="blog_index"),
    path('posts/<int:post_id>/', detail_view, name="blog_detail"),
    path('posts/<int:post_id>/edit', edit_view, name="blog_edit"),
]
