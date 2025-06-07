from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='materials-home'),
    path('list/', views.material_list, name='material-list'),
    path('add/', views.add_material, name='add-material'),

    path('request/', views.request_material, name='request_material'),
    path('requests/', views.view_requests, name='view_requests'),
    path('requests/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('decline/approve/<int:request_id>/', views.decline_request, name='decline_request'),

    path('shop/', views.shop_home, name='shop_home'),
    path('my-requests/', views.view_my_requests, name='view_my_requests'),
]
