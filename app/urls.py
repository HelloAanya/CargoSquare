from django.urls import path
from . import views 

urlpatterns = [
    path('', views.header, name='header'),
    path('user/signup/', views.user_signup, name='user_signup'),
    path('user/index/', views.user_index, name='user_index'),
    path('user/login/', views.user_login, name='login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('logout/', views.logout_view, name='logout'),
    path('add_product/', views.add_product, name='add_product'),
    path('remove_product/<int:product_id>/', views.remove_product, name='remove_product'),
    path('product_list/', views.product_list, name='product_list'),
    path('search/', views.search_product, name='search_product'),
    path('order_now/', views.order_now, name='order_now'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('user/search/', views.user_search, name='user_search'), 
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'), 
    path('view_order_list/', views.view_order_list, name='view_order_list'),
    path('shop/', views.shop, name='shop'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
