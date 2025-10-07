from django.urls import path
from main.views import show_main_page, show_xml, show_json, show_xml_by_id, show_json_by_id, create_product, show_detail, register, login_user, logout_user, edit_product, delete_product, add_product_ajax, get_product_json, update_product_ajax, delete_product_ajax, login_ajax, register_ajax
app_name = "main"

urlpatterns = [
    path('', show_main_page, name='show_main_page'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('create-product/', create_product, name='create_product'),
    path('show/<str:id>/', show_detail, name='show_detail'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('edit/<str:id>/', edit_product, name='edit_product'),
    path('delete/<str:id>/', delete_product, name='delete_product'),
    path('create-product-ajax/',add_product_ajax,name='add_product_ajax'),
    path('get-product-json/', get_product_json, name='get_product_json'),
    path('update-product-ajax/<str:id>/', update_product_ajax, name='update_product_ajax'),
    path('delete-product-ajax/<str:id>/', delete_product_ajax, name='delete_product_ajax'),
    path('login-ajax/', login_ajax, name='login_ajax'),
    path('register-ajax/', register_ajax, name='register_ajax'),
]