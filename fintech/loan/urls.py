from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^loan_process$', views.LoanProcess.as_view()),
    url(r'^approve_loans$', views.ApproveLoans.as_view()),
]