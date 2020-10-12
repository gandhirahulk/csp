from datetime import datetime
from pytz import utc
from csp_app.models import master_candidate, master_vendor, vendor_status, onboarding_status, status
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

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

# def DocumentReminder():
#     approve = vendor_status.objects.get(pk=1)
#     approve = onboarding_status.objects.get(pk=1)
#     active = status.objects.get(pk=1)
#     pending_action_candidates = master_candidate.objects.filter(vendor_status=active, onboarding_status= approve, status= active)
#     for each in pending_action_candidates: 
#         vendor_email = each.fk_vendor_code.vendor_email_id
#         reminder_template = render_to_string('csp_app/reminder_template.html', {'candidate_code':each.pk ,'vendor': each.fk_vendor_code})
#         our_email = EmailMessage(
#             'Daily Reminder UDAAN:CSP_APP',
#             reminder_template,
#             settings.EMAIL_HOST_USER,
#             [ vendor_email, 'sadaf.shaikh@udaan.com'],
#         ) 
#         our_email.fail_silently = False
#         our_email.send()
#         print("Reminder Mail Sent to " + str(each.fk_vendor_code) + " in reference to candidate with ID " + str(each.pk) + " .")
