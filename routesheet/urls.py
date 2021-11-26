from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views



urlpatterns = format_suffix_patterns([   
   path("driver/", views.DriverListView.as_view()), 
   path("loko/", views.LokoListView.as_view()), 
   path("norms/", views.NormListView.as_view()),
   path("region/", views.RegionListView.as_view()),
   path("loko/select/", views.LokoSelectView.as_view()),
   path("driver/select/", views.DriverSelectView.as_view()),
   path("loko/select-number/", views.LokoNumberSelectView.as_view()),
   #path("station/", views.StationListView.as_view()),
   path("area/",views.AreaSelectView.as_view()),
   path("station/",views.StationSelectView.as_view()),
   path("settings/",views.SettingsView.as_view()), 
   path("result/",views.ResultView.as_view()),
   path("result-oper/<str:slug>/",views.ResultView.as_view()),
   path("result/<str:slug>/",views.ResultTrailReport.as_view()),
   path("report/",views.ReportAll.as_view()),
   path("report/area/",views.ReportArea.as_view()),
   path("report/<int:pk>/", views.ReportID.as_view()),  
   path("report/<str:slug>/",views.ReportSlug.as_view()),   
   path("menu/", views.MenuAll.as_view()),
   path("result-edit/<str:slug>/", views.EditResult.as_view()),
   path("driver-edit/", views.EditDriver.as_view()),
   path("delete-operation/", views.DeleteOperation.as_view()),
   path("content/<str:slug>/", views.ReportContent.as_view()),
   path("perm/<str:slug>/",views.Permission.as_view()),
   path("user/",views.User_header.as_view()),
])
