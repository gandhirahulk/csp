from django.urls import path
from csp_app import views
from csp_app import execute
from django.conf import settings
from django.conf.urls.static import static
#new
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('candidates/', views.index, name='index'),

    path('', views.csp_login, name= 'login'),
    path('logout/', views.csp_logout, name= 'csp_logout'),
    path('notlogin/', views.notlogin, name='notlogin'),

    path('csp_admin/', views.admin, name= 'admin'),
    path('csp_admin/csp_user/', views.create_user_view, name= 'user'),
    path('csp_admin/csp_user/new_user/', views.create_user, name= 'create_user'),
    path('csp_admin/csp_disable_user/', views.disable_user, name= 'disable_user'),
    path('csp_admin/csp_enable_user/', views.enable_user, name= 'enable_user'),
    
    path('csp_candidates/', views.candidate, name= 'candidate'),
    path('csp_candidates/new_candidate/', views.new_candidate, name= 'new_candidate'),
    path('csp_candidates/edit_candidate/', views.edit_candidate, name= 'edit_candidate'),
    path('csp_candidates/create_new/', views.create_candidate, name= 'create_candidate'),
    path('csp_candidates/view_candidate/', views.view_candidate, name= 'view_candidate'),
    path('csp_candidates/change_status/', views.change_candidate_status, name= 'change_candidate_status'),
    path('csp_candidates/vendor_change_status/', views.change_candidate_status_vendor, name= 'change_candidate_status_vendor'),

    path('csp_candidates/document_upload/<str:candidate_id>/', views.candidate_document_upload, name= 'document_upload'),
    path('csp_candidates/document_upload/delete/', views.delete_document, name= 'delete_document'),


    path('csp_candidates/candidate_document/', views.candidate_document, name= 'documents'),
    path('csp_candidates/candidate_document/<str:cid>', views.candidate_document, name= 'documents'),


    path('csp_entity/', views.entity, name= 'entity'),
    path('csp_entity/new_entity/', views.create_entity, name= 'create_entity'),
    path('csp_entity/edit_entity/', views.view_edit_entity, name= 'edit_entity'),
    path('csp_entity/save_edit_entity/', views.save_edit_entity, name= 'save_edit_entity'),
    path('csp_entity/view_entity/', views.view_entity, name= 'view_entity'),
    path('csp_entity/delete_entity/', views.delete_entity, name= 'delete_entity'),

    path('csp_vendor/', views.vendor, name= 'vendor'),
    path('csp_vendor/new_vendor/', views.create_vendor, name= 'create_vendor'),
    path('csp_vendor/edit_vendor/', views.view_edit_vendor, name= 'edit_vendor'),
    path('csp_vendor/save_edit_vendor/', views.save_edit_vendor, name= 'save_edit_vendor'),
    path('csp_vendor/view_vendor/', views.view_vendor, name= 'view_vendor'),
    path('csp_vendor/delete_vendor/', views.delete_vendor, name= 'delete_vendor'),

    path('csp_department/', views.department, name= 'department'),
    path('csp_department/new_dept/', views.create_department, name= 'create_department'),
    path('csp_department/edit_department/', views.view_edit_department, name= 'edit_department'),
    path('csp_department/save_edit_department/', views.save_edit_department, name= 'save_edit_department'),
    path('csp_department/view_department/', views.view_department, name= 'view_department'),
    path('csp_department/delete_department/', views.delete_department, name= 'delete_department'),

    path('csp_function/', views.function, name= 'function'),
    path('csp_function/new_function/', views.create_function, name= 'create_function'),
    path('csp_function/edit_function/', views.view_edit_function, name= 'edit_function'),
    path('csp_function/save_edit_function/', views.save_edit_function, name= 'save_edit_function'),
    path('csp_function/view_function/', views.view_function, name= 'view_function'),
    path('csp_function/delete_function/', views.delete_function, name= 'delete_function'),


    path('csp_team/', views.team, name= 'team'),
    path('csp_team/new_team/', views.create_team, name= 'create_team'),
    path('csp_team/edit_team/', views.view_edit_team, name= 'edit_team'),
    path('csp_team/save_edit_team/', views.save_edit_team, name= 'save_edit_team'),
    path('csp_team/view_team/', views.view_team, name= 'view_team'),
    path('csp_team/delete_team/', views.delete_team, name= 'delete_team'),

    path('csp_sub_team/', views.subteam, name= 'subteam'),
    path('csp_sub_team/new_sub_team/', views.create_subteam, name= 'create_subteam'),
    path('csp_sub_team/edit_subteam/', views.view_edit_subteam, name= 'edit_subteam'),
    path('csp_sub_team/save_edit_subteam/', views.save_edit_subteam, name= 'save_edit_subteam'),
    path('csp_sub_team/view_subteam/', views.view_subteam, name= 'view_subteam'),
    path('csp_sub_team/delete_subteam/', views.delete_subteam, name= 'delete_subteam'),

    path('csp_designation/', views.designation, name= 'designation'),
    path('csp_designation/new_designation/', views.create_designation, name= 'create_designation'),
    path('csp_designation/edit_designation/', views.view_edit_designation, name= 'edit_designation'),
    path('csp_designation/save_edit_designation/', views.save_edit_designation, name= 'save_edit_designation'),
    path('csp_designation/view_designation/', views.view_designation, name= 'view_designation'),
    path('csp_designation/delete_designation/', views.delete_designation, name= 'delete_designation'),

    path('csp_region/', views.region, name= 'region'),
    path('csp_region/new_region/', views.create_region, name= 'create_region'),
    path('csp_region/edit_region/', views.view_edit_region, name= 'edit_region'),
    path('csp_region/save_edit_region/', views.save_edit_region, name= 'save_edit_region'),
    path('csp_region/view_region/', views.view_region, name= 'view_region'),
    path('csp_region/delete_region/', views.delete_region, name= 'delete_region'),

    path('csp_state/', views.state, name= 'state'),
    path('csp_state/new_state/', views.create_state, name= 'create_state'),
    path('csp_state/edit_state/', views.view_edit_state, name= 'edit_state'),
    path('csp_state/save_edit_state/', views.save_edit_state, name= 'save_edit_state'),
    path('csp_state/view_state/', views.view_state, name= 'view_state'),
    path('csp_state/delete_state/', views.delete_state, name= 'delete_state'),

    path('csp_city/', views.city, name= 'city'),
    path('csp_city/new_city/', views.create_city, name= 'create_city'),
    path('csp_city/edit_city/', views.view_edit_city, name= 'edit_city'),
    path('csp_city/save_edit_city/', views.save_edit_city, name= 'save_edit_city'),
    path('csp_city/view_city/', views.view_city, name= 'view_city'),
    path('csp_city/delete_city/', views.delete_city, name= 'delete_city'),

    path('csp_location/', views.location, name= 'location'),
    path('csp_location/new_location/', views.create_location, name= 'create_location'),
    path('csp_location/edit_location/', views.view_edit_location, name= 'edit_location'),
    path('csp_location/save_edit_location/', views.save_edit_location, name= 'save_edit_location'),
    path('csp_location/view_location/', views.view_location, name= 'view_location'),
    path('csp_location/delete_location/', views.delete_location, name= 'delete_location'),

    # path('csp_admin/csp_candidates/', views.candidate, name= 'candidate'),

   

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)