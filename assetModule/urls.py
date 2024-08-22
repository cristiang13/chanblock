from . import views
from django.urls import include, path


urlpatterns = [
    path('manteniance', views.maintenance,name='manteniance'),
    path('indicators', views.getAssets, name='indicators'),
    path('coin_detail/<symbol>', views.coin_detail, name='coin_detalle'),
    path('showTable', views.showTable, name='showTable'),
    
    # graph
    path('plot', views.plot_view, name='graph_default'),
    path('plot_metrics/', views.plot_metrics_view, name='plot_metrics'),
    path('metrics_vara', views.plot_metrics_vara_view, name='metrics_vara'),
    path('stream-last-three-blocks', views.stream_last_three_blocks, name='stream_last_three_blocks'),

    # chat
    path('chat', views.chat_view, name='chat'),

    # gastracker
    path('checkFees', views.check_fees, name="checkFees"),
    path('findFees', views.find_fees, name="findFees"),

]
