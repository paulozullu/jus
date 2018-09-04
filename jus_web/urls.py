from django.conf.urls import url

from jus_web.views import search_process

urlpatterns = [
    url(r'^search_process/$', search_process, name='search_process'),
]
