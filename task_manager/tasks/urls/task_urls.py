from django.urls import path

from tasks.views import task_views as views


urlpatterns = [
    path('', views.task_list, name="task-list"),
    path('<str:pk>/', views.getProduct, name='task'),
    path('delete/<str:pk>/', views.deleteProduct, name="product-delete"),
    path('update/<str:pk>/', views.updateProduct, name="product-update"),
]