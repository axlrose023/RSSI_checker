from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import rssi_show_dicts, graph_less, graph_more, download_excel, chart_more, chart_less, homepage, \
    get_data_by_day_less, table_erlang_more, table_erlang_less, graph_log_more, graph_log_less

urlpatterns = [
    path('admin/', admin.site.urls),
    path('refresh_dicts/', rssi_show_dicts, name='refresh_dicts'),
    path('less/', graph_less, name='less'),
    path('more/', graph_more, name='more'),
    path('chart_more/', chart_more, name='chart_more'),
    path('chart_less/', chart_less, name='chart_less'),
    path('download_excel/', download_excel, name='download_excel'),
    path('', homepage, name='homepage'),
    path('yesterday/', get_data_by_day_less, name='yesterday'),
    path('more-erlang/', table_erlang_more, name='table_erlang_more'),
    path('less-erlang/', table_erlang_less, name='table_erlang_less'),
    path('chart_log_more/', graph_log_more, name='chart_log_more'),
    path('chart_log_less/', graph_log_less, name='chart_log_less'),
]

handler404 = 'RSSI.views.page_not_found'
handler500 = 'RSSI.views.server_error'
