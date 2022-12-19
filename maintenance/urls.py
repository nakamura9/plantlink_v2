from django.urls import path
from maintenance import views

urlpatterns = [
    path('inbox/', views.Inbox.as_view(), name='inbox'),
    path('update-job-status/<int:id>/', views.update_status, name='update-status'),
    path('complete-checklist/<int:id>/', views.CheckListSubmitForm.as_view(), name='complete-checklist'),
]
