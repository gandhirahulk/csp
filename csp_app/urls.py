from django.urls import path
from csp_app import views

urlpatterns = [
    path('candidates/', views.index, name='index'),

    path('', views.csp_login, name= 'login'),
    path('logout/', views.csp_logout, name= 'csp_logout'),
    path('notlogin/', views.notlogin, name='notlogin'),

    path('csp_admin/', views.admin, name= 'admin'),
    path('csp_admin/csp_create_user/', views.create_user_view, name= 'user'),
    path('csp_admin/csp_create_user/new_user/', views.create_user, name= 'create_user'),
    path('csp_admin/csp_disable_user/', views.disable_user, name= 'disable_user'),
    
    path('csp_vendor/', views.vendor, name= 'vendor'),
    path('csp_candidates/', views.candidate, name= 'candidate'),
    path('csp_candidates/create_new/', views.create_candidate, name= 'create_candidate'),
    path('csp_candidates/view_candidate/', views.view_candidate, name= 'view_candidate'),



    path('csp_entity/', views.entity, name= 'entity'),
    path('csp_entity/new_entity/', views.create_entity, name= 'create_entity'),
    path('csp_entity/edit_entity/', views.view_edit_entity, name= 'edit_entity'),
    path('csp_entity/save_edit_entity/', views.save_edit_entity, name= 'save_edit_entity'),
    path('csp_entity/view_entity/', views.view_entity, name= 'view_entity'),


    path('csp_agency/', views.agency, name= 'agency'),
    path('csp_agency/new_agency/', views.create_agency, name= 'create_agency'),

    path('csp_department/', views.department, name= 'department'),
    path('csp_department/new_dept/', views.create_department, name= 'create_department'),

    path('csp_function/', views.function, name= 'function'),
    path('csp_function/new_function/', views.create_function, name= 'create_function'),

    path('csp_team/', views.team, name= 'team'),
    path('csp_team/new_team/', views.create_team, name= 'create_team'),

    path('csp_sub_team/', views.subteam, name= 'subteam'),
    path('csp_sub_team/new_sub_team/', views.create_subteam, name= 'create_subteam'),

    path('csp_designation/', views.designation, name= 'designation'),
    path('csp_designation/new_designation/', views.create_designation, name= 'create_designation'),

    path('csp_region/', views.region, name= 'region'),
    path('csp_region/new_region/', views.create_region, name= 'create_region'),

    path('csp_state/', views.state, name= 'state'),
    path('csp_state/new_state/', views.create_state, name= 'create_state'),

    path('csp_city/', views.city, name= 'city'),
    path('csp_city/new_city/', views.create_city, name= 'create_city'),

    path('csp_location/', views.location, name= 'location'),
    path('csp_location/new_location/', views.create_location, name= 'create_location'),


    # path('csp_admin/csp_candidates/', views.candidate, name= 'candidate'),

   

]