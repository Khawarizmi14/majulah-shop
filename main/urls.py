from django.urls import path
from main.views import show_main, add_product, show_product, edit_product, delete_product
from main.views import show_xml, show_json, show_xml_by_id, show_json_by_id
from main.views import register, login_user, logout_user, login_ajax, register_ajax
from main.views import add_product_ajax, delete_product_ajax
from main.views import add_product_flutter, proxy_image

app_name = 'main'

urlpatterns = [
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-flutter/', add_product_flutter, name='add_product_flutter'),

    path('', show_main, name='show_main'),
    path('add-product/', add_product, name='add_product'),
    path('product/<uuid:id>', show_product, name='show_product'),
    path('product/<uuid:id>/edit', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete', delete_product, name='delete_product'),

    path('json/', show_json, name='show_json'),
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),
    path('xml/', show_xml, name='show_xml'),
    path('xml/<uuid:id>/', show_xml_by_id, name='show_xml_by_id'),

    path('add-product-ajax/', add_product_ajax, name='add_product_ajax'),
    path('delete-product-ajax/', delete_product_ajax, name='delete_product_ajax'), 

    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('login-ajax/', login_ajax, name='login_ajax'),
    path('register-ajax/', register_ajax, name='register_ajax'),
]