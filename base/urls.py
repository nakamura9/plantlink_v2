from django.urls import path
from base.views import (
    HomeView, BaseCreateView,  BaseUpdateView,
    BaseListView, AppHome,
    get_child_table_content,
    get_child_table_fields #, BaseDeleteView
)


urlpatterns = [
    path("home/", HomeView.as_view(), name='home'),
    path("app/<str:app>/", AppHome.as_view(), name='app-home'),
    path("create/<str:app>/<str:model>/", BaseCreateView.as_view(), name='create'),
    path("update/<str:app>/<str:model>/<str:id>/", BaseUpdateView.as_view(), name='update'),
    # path("delete/<str:app>/<str:model>/<int:id>/", BaseDeleteView.as_view(), name='delete'),
    path("list/<str:app>/<str:model>/", BaseListView.as_view(), name='list'),
    path('api/child-table-properties/<str:app>/<str:model>/', get_child_table_fields),
    path('api/child-table/<str:app>/<str:model>/<int:parent_id>/', get_child_table_content),
]
