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
# 2	"Pending"
# 0	"Rejected"
# 1	"Approved"
# 7	"Delay In Joining"
# 8	"Delay Request"

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

    return render(request, 'reporting_manager/joined.html',{ 'joined_candidates': joined_candidates})

def joining_confirmation(request):
    today = date.today() 
    last_ten_days = today - timedelta(days = 10)
   
    request_candidates = master_candidate.objects.filter(Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= last_ten_days,status=active_status, vendor_status=approve_vendor, joining_status=joining_status.objects.get(pk=0), candidate_status=candidate_status.objects.get(pk=1)).exclude(Date_of_Joining__gt=today)

    if request.method == 'POST' and request.POST.get('cid') != None:
        cid = request.POST.get('cid')
        
        selected_candidate = master_candidate.objects.get(pk=cid)
        choice = request.POST.get('choosed_option')
        print(choice)
        future_date = request.POST.get('calendar_input_future')
        joining_date = request.POST.get("calendar_input")
        remark = request.POST.get("remark")
        if choice == None or choice == '':
            messages.warning(request, "Please select an option to continue.")
            return redirect("csp_app:rm_joining_confirmation")
     
        if choice == '6':
            subject, from_email = 'Candidate Dropped Out', 'workmail052020@gmail.com'
   
            html_content = render_to_string('emailtemplates/candidate_dropped_out.html',{'cid': selected_candidate.pk})
            text_content = strip_tags(html_content) 
            msg = EmailMultiAlternatives(subject, text_content, from_email, [ selected_candidate.fk_vendor_code.vendor_email_id, selected_candidate.Onboarding_Spoc_Email_Id ])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            selected_candidate.candidate_status = candidate_status.objects.get(pk=6)

            selected_candidate.save()
            messages.success(request, "Candidate Status Updated")
            return redirect("csp_app:rm_joining_confirmation")
        if choice == '5':
            # print(1)
            # expected = selected_candidate.Date_of_Joining
            # rm_input = joining_date
            # if rm_input <= expected:
            #     print(2)
            if remark != None or remark != '':
                selected_candidate.remarks = remark
                selected_candidate.save()
                subject, from_email = 'Candidate Wants To Join Early', 'workmail052020@gmail.com'   
                html_content = render_to_string('emailtemplates/candidate_joined.html',{'cid': selected_candidate.pk})
                text_content = strip_tags(html_content) 
                msg = EmailMultiAlternatives(subject, text_content, from_email, [ selected_candidate.fk_vendor_code.vendor_email_id, selected_candidate.Onboarding_Spoc_Email_Id, selected_candidate.TA_Spoc_Email_Id ])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.success(request, "Details Mailed To Concerned Team.")
                return redirect("csp_app:rm_joining_confirmation")
            subject, from_email = 'Candidate Joined', 'workmail052020@gmail.com'   
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
            selected_candidate.candidate_status = candidate_status.objects.get(pk=5)
            selected_candidate.joining_status = joining_status.objects.get(pk=1)
            selected_candidate.save()

            messages.success(request, "Candidate Status Updated")
            return redirect("csp_app:rm_joining_confirmation")
            # else:
            #     messages.error(request, "Invalid Joining Date")
            #     return redirect("csp_app:rm_joining_confirmation")
        if choice == '7':
            if future_date == None or future_date == '':
                messages.warning(request, "Please provide a future date")
                return redirect("csp_app:rm_joining_confirmation")
            selected_candidate.candidate_status = candidate_status.objects.get(pk=7)
            selected_candidate.delay_date = future_date
            selected_candidate.joining_status = joining_status.objects.get(pk=4)

            subject, from_email = 'Request for future date of joining', 'workmail052020@gmail.com'   
            html_content = render_to_string('emailtemplates/request_for_future.html',{'cid': selected_candidate.pk})
            text_content = strip_tags(html_content) 
            msg = EmailMultiAlternatives(subject, text_content, from_email, [ selected_candidate.fk_vendor_code.vendor_email_id, selected_candidate.Onboarding_Spoc_Email_Id ])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            selected_candidate.save()

            messages.success(request, "Request Sent To Onboarding SPOC")
            return redirect("csp_app:rm_joining_confirmation")
        

        messages.success(request, "")
        return redirect("csp_app:rm_joining_confirmation")
    return render(request, 'reporting_manager/joining_confirmation.html',{ 'request_candidates': request_candidates})

def drop_out(request):
    drop_out_candidates = master_candidate.objects.filter( candidate_status=dropout_candidate, Reporting_Manager_E_Mail_ID= str(request.user),status=active_status)

    return render(request, 'reporting_manager/drop_out.html',{ 'drop_out_candidates': drop_out_candidates})

def future_joining(request):
    today = date.today()
 
    future_candidates = master_candidate.objects.filter(Reporting_Manager_E_Mail_ID= str(request.user), Date_of_Joining__gt= today,status=active_status, joining_status=joining_status.objects.get(pk=0), vendor_status= approve_vendor)
    print(future_candidates)
    return render(request, 'reporting_manager/future_joining.html',{'future_candidates': future_candidates})