from . import views
from django.urls import path

urlpatterns = [
    path('', views.main, name='main'),
    path('product/<str:product_name>', views.product, name='product'),
    path('category/<int:category_id>', views.category, name='category'),
    path('category/<str:category_name>', views.category, name='category'),
    path('checkout', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('favorite/', views.favorite, name='favorite'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('product/cart/add', views.addcart, name='addcart'),
    path('product/cart/del', views.delcart, name='delcart'),
    path('product/cart/edit', views.edit, name='edit'), 
    path('product/favor/edit', views.favor, name='favor'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/main/', views.api_main, name='api_main'),
    path('api/products/<int:page>', views.api_products, name='api_products'),
    path('api/product/<str:product_name>', views.api_product, name='api_product'),
]