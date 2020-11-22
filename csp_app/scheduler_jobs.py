from datetime import datetime
from pytz import utc
from csp_app.models import master_candidate, master_vendor, vendor_status, onboarding_status, status, mandatory_documents
from django.core.mail import EmailMessage
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
    for each_canidate in all_candidates_list:
        candidate_document_list = candidate_document.objects.filter(fk_candidate_code = each_canidate.pk).exclude(document_catagory_id=0)
        candidate_document_len = len(candidate_document_list)
        if mandatory_document_len == candidate_document_len:
            do_nothing = 1
        else:
            vendor_email = each_canidate.fk_vendor_code.vendor_email_id
            reminder_template = render_to_string('csp_app/reminder_template.html', {'candidate_code':each_canidate.pk ,'vendor': each_canidate.fk_vendor_code})
            our_email = EmailMessage(
                'Daily Reminder UDAAN:CSP_APP',
                reminder_template,
                settings.EMAIL_HOST_USER,
                [ vendor_email,each_canidate.Personal_Email_Id, 'sadaf.shaikh@udaan.com'],
            ) 
            our_email.fail_silently = False
            our_email.send()
            print("Reminder Mail Sent to " + str(each_canidate.fk_vendor_code) + " and "+ str(each_canidate.pk_candidate_code) +" in reference to document upload.")
