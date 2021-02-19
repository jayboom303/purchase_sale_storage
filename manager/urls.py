from django.contrib import admin
from django.urls import path
from . import views
 
urlpatterns = [

    path('manager', views.manager_views,name='manager'),
	path('tool/borrow', views.tool_borrow_views,name='tool-borrow'),
	path('tool/return', views.tool_return_views,name='tool-return'),
	path('manager/tool/sourcedata/upload', views.manager_tool_data_upload_views,name='manager-tool-data-upload'),
	path('manager/tool/sourcedata/query', views.manager_tool_data_query_views,name='manager-tool-data-query'),
	path('manager/success', views.manager_success_views,name='manager-success'),
	path('manager/employee/add', views.manager_employee_add_views,name='manager-employee-add'),
	path('manager/employee/query', views.manager_employee_query_views,name='manager-employee-query'),
	path('manager/user/jurisdiction/query', views.manager_user_jurisdiction_query_views,name='manager-user-jurisdiction-query'),
	path('tool-br/data/statistics', views.tool_br_data_statistics_views,name='tool-br-data-statistics'),
	path('tool-br/data/analysis', views.tool_br_data_analysis_views,name='tool-br-data-analysis'),
    
]