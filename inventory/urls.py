from django.urls import path
from inventory import views

urlpatterns = [
    path('csv-dashboard/', views.CSVImportDashboard.as_view()),
    path('import/', views.ImportView.as_view()),
    path('get-all-children/<str:model_name>/<str:id>/', views.get_all_children),
]
