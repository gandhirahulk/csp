from django.urls import path
from csp_app import views
from csp_app import execute
from csp_app import exports
from csp_app import reporting_manager
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('clear_data/', views.clear_data, name='clear_data'),

    path('reporting_manager/joined/', reporting_manager.joined, name='rm_joined'),
    path('reporting_manager/joining_confirmation/', reporting_manager.joining_confirmation, name='rm_joining_confirmation'),
    path('reporting_manager/drop_out/', reporting_manager.drop_out, name='rm_drop_out'),
    path('reporting_manager/future_joining/', reporting_manager.future_joining, name='rm_future_joining'),



    path('resend_loi/<str:cid>/', views.resend_loi, name="resend_loi"),

    path('send/', views.custom_send_email, name="send"),
    path('export_entity/', exports.export_entity, name='export_entity'),
    path('export_department/', exports.export_department, name='export_department'),
    path('export_function/', exports.export_function, name='export_function'),
    path('export_team/', exports.export_team, name='export_team'),
    path('export_subteam/', exports.export_sub_team, name='export_subteam'),
    path('export_designation/', exports.export_designation, name='export_designation'),
    path('export_minimum_wages/', exports.export_minimum_wage, name='export_minimumwages'),
    path('export_vendor/', exports.export_vendor, name='export_vendor'),


    path('export_location/', exports.export_location, name='export_location'),
    path('export_state/', exports.export_state, name='export_state'),
    path('export_city/', exports.export_city, name='export_city'),
    path('export_region/', exports.export_region, name='export_region'),
    path('export_location/', exports.export_location, name='export_location'),
    path('export_candidate/', exports.export_candidate, name='export_candidate'),


    path('candidates/', views.index, name='index'),

    path('candidate/', views.candidate_profile, name='candidate_profile'),


    path('', views.csp_login, name= 'login'),
    path('logout/', views.csp_logout, name= 'csp_logout'),
    path('notlogin/', views.notlogin, name='notlogin'),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('change_password/',views.change_password,name='password_change'),
    path('view_salary_structure/<str:cid>/',views.view_ss,name='view_ss'),



    path('csp_admin/', views.admin, name= 'admin'),
    path('csp_admin/csp_user/', views.create_user_view, name= 'user'),
    path('csp_admin/csp_user/new_user/', views.create_user, name= 'create_user'),
    path('csp_admin/csp_disable_user/', views.disable_user, name= 'disable_user'),
    path('csp_admin/csp_enable_user/', views.enable_user, name= 'enable_user'),

    path('csp_minimum_wages/', views.minimum_wages, name="minimumwages"),
    path('csp_minimum_wages/new_minimum_wages/', views.create_wages, name= 'create_minimumwages'),
    path('csp_minimum_wages/edit_minimum_wages/', views.view_edit_wages, name= 'edit_minimumwages'),
    path('csp_minimum_wages/save_edit_minimum_wages/', views.save_edit_wages, name= 'save_edit_minimumwages'),
    path('csp_minimum_wages/view_minimum_wages/', views.view_wages, name= 'view_minimumwages'),
    path('csp_minimum_wages/delete_minimum_wages/', views.delete_wages, name= 'delete_minimumwages'),

    
    path('csp_candidates/', views.candidate, name= 'candidate'),
    path('csp_candidates/new_candidate/', views.new_candidate, name= 'new_candidate'),
    path('csp_candidates/view_edit_candidate/<str:cid>/', views.view_edit_candidate, name= 'view_edit_candidate'),
    path('csp_candidates/edit_candidate_salary/', views.edit_salary_structure, name= 'edit_salary_structure'),

    path('csp_candidates/edit_candidate/', views.edit_candidate, name= 'edit_candidate'),
    path('csp_candidates/create_new/', views.create_candidate, name= 'create_candidate'),
    path('csp_candidates/save_new/', views.save_new_candidate, name= 'save_new_candidate'),
    path('csp_candidates/check_duplicacy_new/', views.check_duplicate_candidate_new, name= 'check_duplicate_candidate_new'),
    path('csp_candidates/check_duplicacy_edit/', views.check_duplicate_candidate_edit, name= 'check_duplicate_candidate_edit'),
   
    path('csp_candidates/view_candidate/<str:cid>/', views.view_candidate, name= 'view_candidate'),
    path('csp_candidates/view_candidate/', views.view_candidate, name= 'view_candidate'),
    
    path('csp_candidates/change_status/', views.change_candidate_status, name= 'change_candidate_status'),
    path('csp_candidates/vendor_change_status/', views.change_candidate_status_vendor, name= 'change_candidate_status_vendor'),

    path('csp_candidates/document_upload/<str:candidate_id>/', views.candidate_document_upload, name= 'document_upload'),
    # path('csp_candidates/document_upload/delete_document/', views.candidate_delete_document, name= 'candidate_delete_document'),

    path('csp_candidates/pending_requests/', views.pending_requests, name= 'pending_request'),
    path('csp_candidates/approved_candidates/', views.approved_candidates, name= 'approved_candidates'),
    path('csp_candidates/future_joining_requests/', views.future_joining_requests, name= 'future_joining_request'),

    path('csp_candidates/process_requests/<str:cid>/', views.process_requests, name= 'process_request'),
    path('csp_candidates/process_requests/reject_request/<str:cid>/', views.reject_candidate_vendor, name= 'reject_candidate_vendor'),

    path('csp_candidates/process_requests/reject_request/<str:cid>/', views.reject_candidate_onboarding, name= 'reject_candidate_onboarding'),
    path('csp_candidates/process_requests/salary_structure/<str:cid>/', views.edit_salary_structure_process, name= 'edit_salary_structure_process'),
    #ajax
    path('csp_minimum_wage_list/', views.minimum_wage_list, name="csp_minimum_wage_list"),
    path('csp_candidates/check_rm_email/', views.check_rm_email, name="csp_rm_email_check"),





    path('csp_entity/', views.entity, name= 'entity'),
    path('csp_entity/new_entity/', views.create_entity, name= 'create_entity'),
    path('csp_entity/edit_entity/', views.view_edit_entity, name= 'edit_entity'),
    path('csp_entity/save_edit_entity/', views.save_edit_entity, name= 'save_edit_entity'),
    path('csp_entity/view_entity/', views.view_entity, name= 'view_entity'),
    path('csp_entity/delete_entity/', views.delete_entity, name= 'delete_entity'),

    path('csp_vendor/', views.vendor, name= 'vendor'),
    path('csp_vendor/create_new/', views.new_vendor, name= 'new_vendor'),

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