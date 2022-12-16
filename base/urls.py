from django.urls import path
from base.views import (
    HomeView, BaseCreateView,  BaseUpdateView,
    BaseListView, AppHome,
    get_child_table_content,
    get_child_table_fields, get_model_items,
    get_token_for_current_user , BaseDeleteView
)


urlpatterns = [
    path("home/", HomeView.as_view(), name='home'),
    path("app/<str:app>/", AppHome.as_view(), name='app-home'),
    path("create/<str:app>/<str:model>/", BaseCreateView.as_view(), name='create'),
    path("update/<str:app>/<str:model>/<str:id>/", BaseUpdateView.as_view(), name='update'),
    path("delete/<str:app>/<str:model>/<int:pk>/", BaseDeleteView.as_view(), name='delete'),
    path("list/<str:app>/<str:model>/", BaseListView.as_view(), name='list'),
    path('api/child-table-properties/<str:app>/<str:model>/', get_child_table_fields),
    path('api/child-table/<str:app>/<str:model>/<int:parent_id>/', get_child_table_content),
    path('api/model-items/<str:app_name>/<str:model_name>/', get_model_items),
    path('api/user-token/', get_token_for_current_user),
]
