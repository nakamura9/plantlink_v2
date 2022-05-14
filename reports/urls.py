from django.urls import path
from reports.views import ReportView, HomeView, get_report_data, ReportPDFView

urlpatterns = [
    path("reports/", HomeView.as_view(), name='reports'),
    path("report/<str:name>/", ReportView.as_view(), name='report'),
    path("report-pdf/<str:name>/", ReportPDFView.as_view(), name='report-pdf'),
    path("get-report-data/<str:name>/", get_report_data, name='get-report-data'),
    
]
