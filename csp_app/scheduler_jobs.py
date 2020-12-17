from datetime import datetime
from .constants import *
from pytz import utc
from csp_app.models import *
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
###
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
###
from django.conf import settings
from django.template.loader import render_to_string

active = status.objects.get(pk=1)

def RemindVendor():
    pending = vendor_status.objects.get(pk=2)
    approve = onboarding_status.objects.get(pk=1)
    active = status.objects.get(pk=1)
    pending_action_candidates = master_candidate.objects.filter(vendor_status=pending, onboarding_status= approve, status= active)
    for each in pending_action_candidates: 
        vendor_email = each.fk_vendor_code.vendor_email_id
        reminder_template = render_to_string('csp_app/reminder_template.html', {'candidate_code':each.pk ,'vendor': each.fk_vendor_code})
        our_email = EmailMessage(
            'Daily Reminder UDAAN:CSP_APP',
            reminder_template,
            settings.EMAIL_HOST_USER,
            [ vendor_email, 'sadaf.shaikh@udaan.com'],
        ) 
        our_email.fail_silently = False
        our_email.send()
        print("Reminder Mail Sent to " + str(each.fk_vendor_code) + " in reference to candidate with ID " + str(each.pk) + " .")

def DocumentReminder():
    vendor_approve = vendor_status.objects.get(pk=1)
    onboard_approve = onboarding_status.objects.get(pk=1)
    all_candidates_list = master_candidate.objects.filter(status=active, vendor_status= vendor_approve, onboarding_status= onboard_approve)
    mandatory_list = mandatory_documents.objects.all().exclude(pk=0)
    mandatory_document_len = len(mandatory_list)
    for selected_candidate in all_candidates_list:
        candidate_document_list = candidate_document.objects.filter(fk_candidate_code = selected_candidate.pk).exclude(document_catagory_id=0)
        candidate_document_len = len(candidate_document_list)
        if mandatory_document_len == candidate_document_len:
            do_nothing = 1
        else:
            
            my_host = selected_candidate.fk_vendor_code.vendor_smtp
            my_port = selected_candidate.fk_vendor_code.vendor_email_port.port
            my_username = selected_candidate.fk_vendor_code.vendor_email_id
            my_password = selected_candidate.fk_vendor_code.vendor_email_id_password
            my_use_tls = selected_candidate.fk_vendor_code.vendor_email_port.tls
            my_use_ssl = selected_candidate.fk_vendor_code.vendor_email_port.ssl
            subject = 'Document Upload Pending : ' + str(selected_candidate.First_Name) + ' | ' + str(selected_candidate.pk_candidate_code)
            bcc_email = [ selected_candidate.TA_Spoc_Email_Id, selected_candidate.Onboarding_Spoc_Email_Id , 'sadaf.shaikh@udaan.com', ADMIN_MAIL]   
            to_email = [ selected_candidate.Personal_Email_Id ]
            cc_email = [ selected_candidate.fk_vendor_code.vendor_email_id ]
            html_content = render_to_string('emailtemplates/reminder_template.html', {'candidate_name': selected_candidate.First_Name, 'designation': selected_candidate.fk_designation_code, 'vendor_name': selected_candidate.fk_vendor_code,'vendor_spoc_email': selected_candidate.fk_vendor_code.spoc_email_id , 'vendor_phone': selected_candidate.fk_vendor_code.vendor_phone_number, 'offer_date': 'offer_date'})
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
                msg = EmailMultiAlternatives(subject1, body1, from1, to_email , bcc= bcc_email , cc= cc_email, connection=connection)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            print("Reminder Mail Sent to " + str(selected_candidate.fk_vendor_code) + " and "+ str(selected_candidate.pk_candidate_code) +" in reference to document upload.")

def confirmJoining():
    approve_candidate = candidate_status.objects.get(pk=2)
    active = status.objects.get(pk=1)
    not_joined = joining_status.objects.get(pk = 0)
    pending_confirmation_candidates = master_candidate.objects.filter( candidate_status=approve_candidate, joining_status=not_joined, status= active, Date_of_Joining=datetime.date.today())
    for selected_candidate in pending_confirmation_candidates: 
        # send_mail_code
        subject = 'Joining Confirmation Required : ' + str(selected_candidate.First_Name) + ' | ' + str(selected_candidate.pk)
        cc_email = [ selected_candidate.Onboarding_Spoc_Email_Id,selected_candidate.TA_Spoc_Email_Id ]
        to_email = [ selected_candidate.Reporting_Manager_E_Mail_ID ]
        bcc_email = [ 'sadaf.shaikh@udaan.com' , ADMIN_MAIL ]
        from_email = FROM_EMAIL
        html_content = render_to_string('emailtemplates/candidate_offer_closure.html' , {'changes':changes_list, 'vendor_spoc': selected_candidate.fk_vendor_code.spoc_name, 'company_name': selected_candidate.fk_entity_code.entity_name, 'candidate_name': selected_candidate.First_Name, 'candidate_id': selected_candidate.pk, 'vendor_name': selected_candidate.fk_vendor_code.vendor_name, 'dept_name': selected_candidate.fk_department_code.department_name , 'function_name': selected_candidate.fk_function_code.function_name, 'team_name': selected_candidate.fk_team_code.team_name, 'sub_team_name': selected_candidate.fk_subteam_code.sub_team_name, 
        'desg_name': selected_candidate.fk_designation_code.designation_name, 'region_name': selected_candidate.fk_region_code.region_name.zone_name , 'state_name': selected_candidate.fk_state_code.state_name.state_name, 'location_name': selected_candidate.fk_location_code.location_name, 'location_code': selected_candidate.fk_location_code.location_code, 'salary_num': selected_candidate.Gross_Salary_Amount , 'salary_word': num2words(selected_candidate.Gross_Salary_Amount, lang = 'en_IN'), 'rm_name': selected_candidate.Reporting_Manager, 'rm_mail': selected_candidate.Reporting_Manager_E_Mail_ID, 'doj': selected_candidate.Date_of_Joining, 'recruitment_spoc': selected_candidate.TA_Spoc_Email_Id, 'onboarding_spoc': selected_candidate.Onboarding_Spoc_Email_Id, 'manual_link': MANUAL_LINK, 'admin' : ADMIN_NAME, 'admin_mail': ADMIN_MAIL}) 
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email , bcc= bcc_email, cc= cc_email )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Date of joining Confirmation Mail Sent to " + str(selected_candidate.Reporting_Manager_E_Mail_ID) + " in reference to candidate with ID " + str(selected_candidate.pk) + " .")

