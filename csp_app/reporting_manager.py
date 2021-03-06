from csp_app.models import * 
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from datetime import date
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags###
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .constants import *
from num2words import num2words
from django.core.mail import get_connection

# 4	"Hold"
# 5	"Joined"
# 6	"Dropout"
# 2	"Pending"
# 0	"Rejected"
# 1	"Approved"
# 7	"Delay In Joining"
# 8	"Delay Request"
# 9 "Change in DOJ"

# 1	"Joined"
# 2	"Sent - Pending With Manager"
# 0	"Not Joined"
# 3	"N/A"
# 4	"Delay Request"

deactive_status = status.objects.get(pk=0)
active_status = status.objects.get(pk=1)
approve_candidate = candidate_status.objects.get(pk=1)

joined_candidate = candidate_status.objects.get(pk=5)
dropout_candidate = candidate_status.objects.get(pk=6)

approve_onboarding = onboarding_status.objects.get(pk = 1)
approve_vendor = vendor_status.objects.get(pk = 1)

candidate_list = master_candidate.objects.filter(status=active_status)

#change 'chirag.phor@udaan.com' to request.user



def get_onbording_spoc():
    try:
        Onboarding_SPOC_list = User.objects.get(groups__name='Onboarding SPOC')
        Onboarding_SPOC_Mail = Onboarding_SPOC_list.email
        Onboarding_SPOC_Name = str(Onboarding_SPOC_list.first_name) + ' ' + str(Onboarding_SPOC_list.last_name)
        Onboarding_SPOC_first_name = str(Onboarding_SPOC_list.first_name)
    except ObjectDoesNotExist:
        Onboarding_SPOC_Mail = FROM_EMAIL
        Onboarding_SPOC_Name = ONBOARDING_SPOC_NAME
        x = ONBOARDING_SPOC_NAME.split(' ', 1)[0]
        if len(x) < 3:
            Onboarding_SPOC_first_name = ONBOARDING_SPOC_NAME
        else:
            Onboarding_SPOC_first_name = x
    return Onboarding_SPOC_Mail, Onboarding_SPOC_Name, Onboarding_SPOC_first_name

def get_first_name(name):
    x = name.split(' ', 1)[0]
    if len(x) > 2:
        my_first_name = x
    else:
        my_first_name = name
    print(my_first_name)
    return my_first_name

def get_recruiter_spoc(ta_spoc_mail):
    try:
        recruiter = User.objects.get(username=ta_spoc_mail)
        recruiter_name = str(recruiter.first_name) + ' ' + str(recruiter.last_name)
        recruiter_first_name = str(recruiter.first_name)
    except ObjectDoesNotExist:
        recruiter_name = ADMIN_NAME
        x = recruiter_name.split(' ', 1)[0]
        if len(x) < 3:
            recruiter_first_name = ADMIN_NAME
        else:
            recruiter_first_name = x
    return recruiter_name, recruiter_first_name


def doj_limit(request):
    
    candidate_id = request.GET.get('candidate_id')
    

    limit = {}
    try:                
        c = master_candidate.objects.get(pk=candidate_id, status= active_status)
        d = c.Date_of_Joining
        last_ten_days = d - timedelta(days = 10)
        limit['max'] = c.Date_of_Joining
        limit['min'] = last_ten_days
        return JsonResponse(limit)
    except ObjectDoesNotExist:
        limit['max'] = ''
    return JsonResponse(limit)

def joined(request):
    joined_candidates = master_candidate.objects.filter( candidate_status=joined_candidate, Reporting_Manager_E_Mail_ID= str(request.user),status=active_status)
    today = date.today() 
    last_ten_days = today - timedelta(days = 10)   
    request_candidates = master_candidate.objects.filter(Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= last_ten_days,status=active_status, vendor_status=approve_vendor, joining_status=joining_status.objects.get(pk=0), candidate_status=candidate_status.objects.get(pk=1)).exclude(Date_of_Joining__gt=today)
    count = len(request_candidates)
    future_candidates = master_candidate.objects.filter(Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= today,status=active_status, joining_status=joining_status.objects.get(pk=0), vendor_status= approve_vendor)
    doj_count = len(future_candidates)
    return render(request, 'reporting_manager/joined.html',{'count':count,'doj_count':doj_count, 'joined_candidates': joined_candidates})

def joining_confirmation(request):
    today = date.today() 
    last_ten_days = today - timedelta(days = 10)   
    request_candidates = master_candidate.objects.filter(Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= last_ten_days,status=active_status, vendor_status=approve_vendor, joining_status=joining_status.objects.get(pk=0), candidate_status=candidate_status.objects.get(pk=1)).exclude(Date_of_Joining__gt=today)
    count = len(request_candidates)
    future_candidates = master_candidate.objects.filter(Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= today,status=active_status, joining_status=joining_status.objects.get(pk=0), vendor_status= approve_vendor)
    doj_count = len(future_candidates)
    Onboarding_SPOC, Onboarding_SPOC_name, Onboarding_first_name = get_onbording_spoc()
    if request.method == 'POST' and request.POST.get('cid') != None:
        cid = request.POST.get('cid')
        
        selected_candidate = master_candidate.objects.get(pk=cid)
        Onboarding_SPOC, Onboarding_SPOC_name, Onboarding_first_name = get_onbording_spoc()
        recruiter_name, recruiter_first_name = get_recruiter_spoc(selected_candidate.TA_Spoc_Email_Id)
        vendor_spoc_first_name = get_first_name(selected_candidate.fk_vendor_code.spoc_name)
        choice = request.POST.get('choosed_option')
        future_date = request.POST.get('calendar_input_future')
        joining_date = request.POST.get("calendar_input")
        remark = request.POST.get("remark")
        Onboarding_SPOC, Onboarding_SPOC_name, Onboarding_first_name = get_onbording_spoc()
        try:
            Onboarding_SPOC_list = User.objects.get(groups__name='Onboarding SPOC')
            Onboarding_SPOC_first_name = Onboarding_SPOC_list.first_name
        except ObjectDoesNotExist:
            Onboarding_SPOC_first_name = 'Admin'
        Onboarding_SPOC, Onboarding_SPOC_name, Onboarding_first_name = get_onbording_spoc()
        if choice == None or choice == '':
            messages.warning(request, "Please select an option to continue.")
            return redirect("csp_app:rm_joining_confirmation")
     
        if choice == '6':
            subject = 'Candidate Dropped Out : ' + str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name) + ' | ' + str(selected_candidate.pk_candidate_code)
            to_email = [ selected_candidate.TA_Spoc_Email_Id, selected_candidate.Onboarding_Spoc_Email_Id ]   
            cc_email = [ selected_candidate.Reporting_Manager_E_Mail_ID , selected_candidate.fk_vendor_code.spoc_email_id]
            bcc_email = [ 'sadaf.shaikh@udaan.com' , 'rahul.gandhi@udaan.com' ]
            from_email = 'associateonboarding@udaan.com'
            html_content = render_to_string('emailtemplates/candidate_dropped_out.html' , {'recruiter_first_name': recruiter_first_name, 'candidate_full_name': str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name),  'onboarding_spoc': Onboarding_SPOC_name, 'onboarding_first_name': Onboarding_first_name, 'onboarding_spoc_mail': Onboarding_SPOC, 'company_name': selected_candidate.fk_entity_code.entity_name, 'candidate_name': selected_candidate.First_Name, 'candidate_full_name': str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name), 'candidate_id': selected_candidate.pk, 'vendor_name': selected_candidate.fk_vendor_code.vendor_name, 'dept_name': selected_candidate.fk_department_code.department_name, 'function_name': selected_candidate.fk_function_code.function_name, 'team_name': selected_candidate.fk_team_code.team_name, 'sub_team_name': selected_candidate.fk_subteam_code.sub_team_name, 'onboarding_spoc_mail': Onboarding_SPOC, 'onboarding_spoc': Onboarding_SPOC_name,'region_name': selected_candidate.fk_region_code.region_name.zone_name, 'city_name': selected_candidate.fk_city_code.city_name,
            'desg_name': selected_candidate.fk_designation_code.designation_name, 'reason': remark , 'state_name': selected_candidate.fk_state_code.state_name.state_name, 'location_name': selected_candidate.fk_location_code.location_name, 'location_code': selected_candidate.fk_location_code.location_code, 'salary_num': selected_candidate.Gross_Salary_Amount, 'salary_word': num2words(selected_candidate.Gross_Salary_Amount, lang = 'en_IN'), 'rm_name': selected_candidate.Reporting_Manager, 'rm_mail': selected_candidate.Reporting_Manager_E_Mail_ID, 'doj': selected_candidate.Date_of_Joining, 'recruitment_spoc': selected_candidate.TA_Spoc_Email_Id, 'recruiter_name': recruiter_name, 'manual_link': MANUAL_LINK, 'admin' : ADMIN_NAME, 'admin_mail': ADMIN_MAIL}) 
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email , bcc= bcc_email, cc= cc_email )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            selected_candidate.candidate_status = candidate_status.objects.get(pk=6)
            selected_candidate.status = status.objects.get(pk=0)
            selected_candidate.save()
            selected_user = User.objects.get(username=selected_candidate.Personal_Email_Id)
            selected_user.delete()
            
            my_host = selected_candidate.fk_vendor_code.vendor_smtp
            my_port = selected_candidate.fk_vendor_code.vendor_email_port.port
            my_username = selected_candidate.fk_vendor_code.vendor_email_id
            my_password = selected_candidate.fk_vendor_code.vendor_email_id_password
            my_use_tls = selected_candidate.fk_vendor_code.vendor_email_port.tls
            my_use_ssl = selected_candidate.fk_vendor_code.vendor_email_port.ssl
            candidate_salary_structure = salary_structure.objects.get(candidate_code= selected_candidate.pk)
            
            subject1 = 'Offer Withdrawal : ' + str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name)
            html_content = render_to_string('emailtemplates/offer_withdrawel.html', {'recruiter_first_name': recruiter_first_name,'candidate_name': selected_candidate.First_Name, 'candidate_full_name': str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name), 'designation': selected_candidate.fk_designation_code, 'vendor_spoc': selected_candidate.fk_vendor_code.spoc_name,'vendor_spoc_email': selected_candidate.fk_vendor_code.spoc_email_id , 'vendor_phone': selected_candidate.fk_vendor_code.vendor_phone_number, 'offer_date': selected_candidate.offer_letter_date})
            body1 = strip_tags(html_content)
            from1 = my_username
            with get_connection(
            host=my_host, 
            port=my_port, 
            username=my_username, 
            password=my_password, 
            use_tls=my_use_tls,
            use_ssl= my_use_ssl
            ) as connection:
                msg = EmailMultiAlternatives(subject1, body1, from1, [selected_candidate.Personal_Email_Id], cc= [ selected_candidate.fk_vendor_code.spoc_email_id ], bcc= [ selected_candidate.TA_Spoc_Email_Id, selected_candidate.Onboarding_Spoc_Email_Id, 'sadaf.shaikh@udaan.com', 'rahul.gandhi@udaan.com' ], connection=connection)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            messages.success(request, "Candidate Dropped Out Details Mailed To Concerned Team")
            return redirect("csp_app:rm_joining_confirmation")
        if choice == '5':
            try:
                IT_email = IT_Email_ID.objects.get(pk=1)
                IT_email_id = IT_email.email_id
            except ObjectDoesNotExist:
                IT_email_id = 'rahul.gandhi@udaan.com'
            if str(selected_candidate.Date_of_Joining) == str(joining_date):
                subject = 'Candidate Date of Joining Confirmed : ' + str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name) +' | ' + str(selected_candidate.pk_candidate_code)
                to_email = [ selected_candidate.TA_Spoc_Email_Id, selected_candidate.Onboarding_Spoc_Email_Id ]   
                cc_email = [ selected_candidate.Reporting_Manager_E_Mail_ID ]
                bcc_email = [ 'sadaf.shaikh@udaan.com' , 'rahul.gandhi@udaan.com' ]
                from_email = 'associateonboarding@udaan.com'
                html_content = render_to_string('emailtemplates/candidate_joined.html' , {'recruiter_first_name': recruiter_first_name,'candidate_full_name': str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name),  'onboarding_spoc': Onboarding_SPOC_name, 'onboarding_first_name': Onboarding_first_name, 'onboarding_spoc_mail': Onboarding_SPOC,  'company_name': selected_candidate.fk_entity_code.entity_name, 'candidate_name': selected_candidate.First_Name, 'candidate_full_name':str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name), 'candidate_id': selected_candidate.pk, 'vendor_name': selected_candidate.fk_vendor_code.vendor_name, 'dept_name': selected_candidate.fk_department_code.department_name, 'function_name': selected_candidate.fk_function_code.function_name, 'team_name': selected_candidate.fk_team_code.team_name, 'sub_team_name': selected_candidate.fk_subteam_code.sub_team_name, 'onboarding_spoc_mail': Onboarding_SPOC, 'onboarding_spoc': Onboarding_SPOC_name,'region_name': selected_candidate.fk_region_code.region_name.zone_name, 'city_name': selected_candidate.fk_city_code.city_name,
                'desg_name': selected_candidate.fk_designation_code.designation_name, 'reason': remark , 'state_name': selected_candidate.fk_state_code.state_name.state_name, 'location_name': selected_candidate.fk_location_code.location_name, 'location_code': selected_candidate.fk_location_code.location_code, 'salary_num': selected_candidate.Gross_Salary_Amount, 'salary_word': num2words(selected_candidate.Gross_Salary_Amount, lang = 'en_IN'), 'rm_name': selected_candidate.Reporting_Manager, 'rm_mail': selected_candidate.Reporting_Manager_E_Mail_ID, 'doj': selected_candidate.Date_of_Joining, 'recruitment_spoc': selected_candidate.TA_Spoc_Email_Id, 'recruiter_name': recruiter_name, 'manual_link': MANUAL_LINK, 'admin' : ADMIN_NAME, 'admin_mail': ADMIN_MAIL}) 
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email, to_email , bcc= bcc_email, cc= cc_email )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                subject = 'Candidate Date of Joining Confirmed : ' + str(selected_candidate.First_Name) +' '+ str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name)+ ' | ' + str(selected_candidate.pk_candidate_code)
                cc_email = [ selected_candidate.TA_Spoc_Email_Id, selected_candidate.Onboarding_Spoc_Email_Id ]   
                to_email = [ selected_candidate.fk_vendor_code.spoc_email_id ]
                bcc_email = [ 'sadaf.shaikh@udaan.com' , 'rahul.gandhi@udaan.com' ]
                from_email = 'associateonboarding@udaan.com'
                html_content = render_to_string('emailtemplates/candidate_joined_to_vendor.html' , {'recruiter_first_name': recruiter_first_name,'candidate_full_name': str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name),  'onboarding_spoc': Onboarding_SPOC_name, 'onboarding_first_name': Onboarding_first_name, 'onboarding_spoc_mail': Onboarding_SPOC,  'company_name': selected_candidate.fk_entity_code.entity_name, 'candidate_name': selected_candidate.First_Name, 'candidate_id': selected_candidate.pk, 'vendor_name': selected_candidate.fk_vendor_code.vendor_name, 'dept_name': selected_candidate.fk_department_code.department_name, 'function_name': selected_candidate.fk_function_code.function_name, 'team_name': selected_candidate.fk_team_code.team_name, 'sub_team_name': selected_candidate.fk_subteam_code.sub_team_name, 'onboarding_spoc_mail': Onboarding_SPOC, 'onboarding_spoc': Onboarding_SPOC_name, 'vendor_spoc': selected_candidate.fk_vendor_code.spoc_name,'region_name': selected_candidate.fk_region_code.region_name.zone_name, 'city_name': selected_candidate.fk_city_code.city_name,
                'desg_name': selected_candidate.fk_designation_code.designation_name, 'reason': remark , 'state_name': selected_candidate.fk_state_code.state_name.state_name, 'location_name': selected_candidate.fk_location_code.location_name, 'location_code': selected_candidate.fk_location_code.location_code, 'salary_num': selected_candidate.Gross_Salary_Amount, 'salary_word': num2words(selected_candidate.Gross_Salary_Amount, lang = 'en_IN'), 'rm_name': selected_candidate.Reporting_Manager, 'rm_mail': selected_candidate.Reporting_Manager_E_Mail_ID, 'doj': selected_candidate.Date_of_Joining, 'recruitment_spoc': selected_candidate.TA_Spoc_Email_Id, 'recruiter_name': recruiter_name, 'manual_link': MANUAL_LINK, 'admin' : ADMIN_NAME, 'admin_mail': ADMIN_MAIL}) 
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email, to_email , bcc= bcc_email, cc= cc_email )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                selected_candidate.candidate_status = candidate_status.objects.get(pk=5)
                selected_candidate.joining_status = joining_status.objects.get(pk=1)
                selected_candidate.save()
            else:
                if len(remark) > 1:                
                    selected_candidate.remarks = remark
                    selected_candidate.save()                
                subject = 'Change in Date of Joining : ' + str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name) +' | ' + str(selected_candidate.pk_candidate_code)
                cc_email = [ selected_candidate.Reporting_Manager_E_Mail_ID ]   
                to_email = [ selected_candidate.Onboarding_Spoc_Email_Id, selected_candidate.TA_Spoc_Email_Id ]
                bcc_email = [ 'sadaf.shaikh@udaan.com' , 'rahul.gandhi@udaan.com' ]
                from_email = 'associateonboarding@udaan.com'
                html_content = render_to_string('emailtemplates/candidate_joining_early.html' , {'recruiter_first_name': recruiter_first_name,'candidate_full_name': str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name),  'onboarding_spoc': Onboarding_SPOC_name, 'onboarding_first_name': Onboarding_first_name, 'onboarding_spoc_mail': Onboarding_SPOC,  'company_name': selected_candidate.fk_entity_code.entity_name, 'candidate_name': selected_candidate.First_Name, 'candidate_full_name':str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name), 'candidate_id': selected_candidate.pk, 'vendor_name': selected_candidate.fk_vendor_code.vendor_name, 'dept_name': selected_candidate.fk_department_code.department_name, 'function_name': selected_candidate.fk_function_code.function_name, 'team_name': selected_candidate.fk_team_code.team_name, 'sub_team_name': selected_candidate.fk_subteam_code.sub_team_name, 'onboarding_spoc_mail': Onboarding_SPOC, 'onboarding_spoc': Onboarding_SPOC_name, 'new_doj' : joining_date,
                'desg_name': selected_candidate.fk_designation_code.designation_name, 'reason': remark , 'state_name': selected_candidate.fk_state_code.state_name.state_name, 'location_name': selected_candidate.fk_location_code.location_name, 'location_code': selected_candidate.fk_location_code.location_code, 'salary_num': selected_candidate.Gross_Salary_Amount, 'salary_word': num2words(selected_candidate.Gross_Salary_Amount, lang = 'en_IN'), 'rm_name': selected_candidate.Reporting_Manager, 'rm_mail': selected_candidate.Reporting_Manager_E_Mail_ID, 'doj': selected_candidate.Date_of_Joining, 'recruitment_spoc': selected_candidate.TA_Spoc_Email_Id,'recruiter_name': recruiter_name, 'manual_link': MANUAL_LINK, 'admin' : ADMIN_NAME, 'admin_mail': ADMIN_MAIL, 'region_name': selected_candidate.fk_region_code.region_name.zone_name}) 
                text_content = strip_tags(html_content)
                msg = EmailMultiAlternatives(subject, text_content, from_email, to_email , bcc= bcc_email, cc= cc_email )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                selected_candidate.candidate_status = candidate_status.objects.get(pk=7)
                selected_candidate.delay_date = joining_date
                selected_candidate.joining_status = joining_status.objects.get(pk=4)
                selected_candidate.save()
                messages.success(request, "Details Mailed To Concerned Team.")
                return redirect("csp_app:rm_joining_confirmation")

            messages.success(request, "Candidate Marked as joined")
            return redirect("csp_app:rm_joining_confirmation")
            
        if choice == '7':
            if future_date == None or future_date == '':
                messages.warning(request, "Please provide a future date")
                return redirect("csp_app:rm_joining_confirmation")
            
            subject = 'Delay in Joining Request :  ' + str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name) +' | ' + str(selected_candidate.pk_candidate_code)
            to_email = [ selected_candidate.Onboarding_Spoc_Email_Id ]   
            cc_email = [ selected_candidate.fk_vendor_code.spoc_email_id , selected_candidate.TA_Spoc_Email_Id]
            bcc_email = [ 'sadaf.shaikh@udaan.com' , 'rahul.gandhi@udaan.com' ]
            from_email = 'associateonboarding@udaan.com'
            html_content = render_to_string('emailtemplates/request_for_future_doj.html' , {'recruiter_first_name': recruiter_first_name,'candidate_full_name': str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name),  'onboarding_spoc': Onboarding_SPOC_name, 'onboarding_first_name': Onboarding_first_name, 'onboarding_spoc_mail': Onboarding_SPOC,  'company_name': selected_candidate.fk_entity_code.entity_name, 'candidate_name': selected_candidate.First_Name,'candidate_full_name': str(selected_candidate.First_Name) + ' ' + str(selected_candidate.Middle_Name) + ' ' + str(selected_candidate.Last_Name), 'candidate_id': selected_candidate.pk, 'vendor_name': selected_candidate.fk_vendor_code.vendor_name, 'dept_name': selected_candidate.fk_department_code.department_name, 'function_name': selected_candidate.fk_function_code.function_name, 'team_name': selected_candidate.fk_team_code.team_name, 'sub_team_name': selected_candidate.fk_subteam_code.sub_team_name, 'onboarding_spoc_mail': Onboarding_SPOC, 'onboarding_spoc': Onboarding_SPOC_name, 'new_doj': future_date,
            'desg_name': selected_candidate.fk_designation_code.designation_name, 'reason': remark , 'state_name': selected_candidate.fk_state_code.state_name.state_name, 'location_name': selected_candidate.fk_location_code.location_name, 'location_code': selected_candidate.fk_location_code.location_code, 'salary_num': selected_candidate.Gross_Salary_Amount, 'salary_word': num2words(selected_candidate.Gross_Salary_Amount, lang = 'en_IN'), 'rm_name': selected_candidate.Reporting_Manager, 'rm_mail': selected_candidate.Reporting_Manager_E_Mail_ID, 'doj': selected_candidate.Date_of_Joining, 'recruitment_spoc': selected_candidate.TA_Spoc_Email_Id,'recruiter_name': recruiter_name, 'manual_link': MANUAL_LINK, 'admin' : ADMIN_NAME, 'admin_mail': ADMIN_MAIL}) 
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email , bcc= bcc_email, cc= cc_email )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            selected_candidate.candidate_status = candidate_status.objects.get(pk=7)
            selected_candidate.delay_date = future_date
            selected_candidate.joining_status = joining_status.objects.get(pk=4)
            selected_candidate.save()

            messages.success(request, "Request Sent To Onboarding SPOC")
            return redirect("csp_app:rm_joining_confirmation")
        

        messages.success(request, "")
        return redirect("csp_app:rm_joining_confirmation")
    return render(request, 'reporting_manager/joining_confirmation.html',{'count':count,'doj_count':doj_count, 'request_candidates': request_candidates})

def drop_out(request):
    drop_out_candidates = master_candidate.objects.filter( candidate_status=dropout_candidate, Reporting_Manager_E_Mail_ID= str(request.user))
    today = date.today() 
    last_ten_days = today - timedelta(days = 10)   
    request_candidates = master_candidate.objects.filter(Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= last_ten_days,status=active_status, vendor_status=approve_vendor, joining_status=joining_status.objects.get(pk=0), candidate_status=candidate_status.objects.get(pk=1)).exclude(Date_of_Joining__gt=today)
    count = len(request_candidates)
    future_candidates = master_candidate.objects.filter(Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= today,status=active_status, joining_status=joining_status.objects.get(pk=0), vendor_status= approve_vendor)
    doj_count = len(future_candidates)
    return render(request, 'reporting_manager/drop_out.html',{ 'count':count,'doj_count':doj_count, 'drop_out_candidates': drop_out_candidates})

def future_joining(request):
    today = date.today() 
    last_ten_days = today - timedelta(days = 10)   
    request_candidates = master_candidate.objects.filter(Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= last_ten_days,status=active_status, vendor_status=approve_vendor, joining_status=joining_status.objects.get(pk=0), candidate_status=candidate_status.objects.get(pk=1)).exclude(Date_of_Joining__gt=today)
    count = len(request_candidates)
 
    future_candidates = master_candidate.objects.filter(Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= today,status=active_status, joining_status=joining_status.objects.get(pk=0), vendor_status= approve_vendor)
    doj_count = len(future_candidates)
    return render(request, 'reporting_manager/future_joining.html',{'count':count,'doj_count':doj_count,'future_candidates': future_candidates})