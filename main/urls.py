from django.urls import path
from main.views import show_main_page, show_xml, show_json, show_xml_by_id, show_json_by_id

urlpatterns = [
    path('', show_main_page, name='show_main_page'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:product_name>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_name>/', show_json_by_id, name='show_json_by_id')
]