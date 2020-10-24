from csp_app.models import * 
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from datetime import date
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
###
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


# 4	"Hold"
# 5	"Joined"
# 6	"Dropout"
# 7	"Delay In Joining"
# 2	"Pending"
# 0	"Rejected"
# 1	"Approved"

deactive_status = status.objects.get(pk=0)
active_status = status.objects.get(pk=1)
approve_candidate = candidate_status.objects.get(pk=1)

joined_candidate = candidate_status.objects.get(pk=5)
dropout_candidate = candidate_status.objects.get(pk=6)

approve_onboarding = onboarding_status.objects.get(pk = 1)
approve_vendor = vendor_status.objects.get(pk = 1)

candidate_list = master_candidate.objects.filter(status=active_status)

#change 'chirag.phor@udaan.com' to request.user


def joined(request):
    joined_candidates = master_candidate.objects.filter( candidate_status=joined_candidate, Reporting_Manager_E_Mail_ID= str(request.user), onboarding_status=approve_onboarding, vendor_status= approve_vendor, status=active_status)

    return render(request, 'reporting_manager/joined.html',{ 'joined_candidates': joined_candidates})

def joining_confirmation(request):
    today = date.today()
    last_ten_days = today - timedelta(days = 10)
 
    request_candidates = master_candidate.objects.filter( candidate_status=approve_candidate, Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__lt= last_ten_days, onboarding_status=approve_onboarding, vendor_status= approve_vendor, status=active_status)
    if request.method == 'POST' and request.POST.get('cid') != None:
        cid = request.POST.get('cid')
        
        selected_candidate = master_candidate.objects.get(pk=cid)
        choice = request.POST.get('choosed_option')
        if choice == None or choice == '':
            messages.warning(request, "Please select an option to continue.")
            return redirect("csp_app:rm_joining_confirmation")
        if choice == 6:
            selected_candidate.candidate_status = candidate_status.objects.get(pk=6)
            subject, from_email = 'Candidate Dropped Out', 'workmail052020@gmail.com'
   
            html_content = render_to_string('emailtemplates/candidate_dropped_out.html',{'cid': selected_candidate.pk})
            text_content = strip_tags(html_content) 
            msg = EmailMultiAlternatives(subject, text_content, from_email, [ selected_candidate.fk_vendor_code.vendor_email_id, selected_candidate.Onboarding_Spoc_Email_Id ])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, "Candidate Status Updated")
            return redirect("csp_app:rm_joining_confirmation")
        elif choice == 5:
            selected_candidate.candidate_status = candidate_status.objects.get(pk=7)
            subject, from_email = 'Request For Future Date of joining', 'workmail052020@gmail.com'   
            html_content = render_to_string('emailtemplates/candidate_joined.html',{'cid': selected_candidate.pk})
            text_content = strip_tags(html_content) 
            msg = EmailMultiAlternatives(subject, text_content, from_email, [ selected_candidate.fk_vendor_code.vendor_email_id, selected_candidate.Onboarding_Spoc_Email_Id, selected_candidate.TA_Spoc_Email_Id ])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            try:
                IT_email = IT_Email_ID.objects.get(pk=1)
                IT_email_id = IT_email.email_id
            except ObjectDoesNotExist:
                IT_email_id = 'rahul.gandhi@udaan.com'
            subject, from_email = 'Email ID Request', 'workmail052020@gmail.com'   
            html_content = render_to_string('emailtemplates/candidate_joined.html',{'cid': selected_candidate.pk})
            text_content = strip_tags(html_content) 
            msg = EmailMultiAlternatives(subject, text_content, from_email, [ IT_email_id ])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, "Candidate Status Updated")
            return redirect("csp_app:rm_joining_confirmation")
        else:
            selected_candidate.candidate_status = candidate_status.objects.get(pk=7)
            subject, from_email = 'Request for future date of joining', 'workmail052020@gmail.com'   
            html_content = render_to_string('emailtemplates/request_for_future.html',{'cid': selected_candidate.pk})
            text_content = strip_tags(html_content) 
            msg = EmailMultiAlternatives(subject, text_content, from_email, [ selected_candidate.fk_vendor_code.vendor_email_id, selected_candidate.Onboarding_Spoc_Email_Id ])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, "Request Sent To Onboarding SPOC")
            return redirect("csp_app:rm_joining_confirmation")
        

        messages.success(request, "")
        return redirect("csp_app:rm_joining_confirmation")
    return render(request, 'reporting_manager/joining_confirmation.html',{ 'request_candidates': request_candidates})

def drop_out(request):
    drop_out_candidates = master_candidate.objects.filter( candidate_status=dropout_candidate, Reporting_Manager_E_Mail_ID= str(request.user), onboarding_status=approve_onboarding, vendor_status= approve_vendor, status=active_status)

    return render(request, 'reporting_manager/drop_out.html',{ 'drop_out_candidates': drop_out_candidates})

def future_joining(request):
    today = date.today()
    last_ten_days = today - timedelta(days = 10)
 
    future_candidates = master_candidate.objects.filter( candidate_status=approve_candidate, Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= last_ten_days, onboarding_status=approve_onboarding, vendor_status= approve_vendor, status=active_status)
   
    return render(request, 'reporting_manager/future_joining.html',{'future_candidates': future_candidates})