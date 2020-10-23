from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
###
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
###
from django.conf import settings
from django.template.loader import render_to_string
from django.db.utils import IntegrityError, DataError
from csp_app.models import * 
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from itertools import chain
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
import xlwt
from csp_app import exports
from django.contrib.auth.hashers import make_password

a = default_token_generator


# 0 - reject
# 1 - approve
# 2 - pending
# 3 - not applicable
# 4 - modified


deactive_status = status.objects.get(pk=0)
active_status = status.objects.get(pk=1)
pending_status = candidate_status.objects.get(pk=2)
reject_onboarding = onboarding_status.objects.get(pk=0)
approve_onboarding = onboarding_status.objects.get(pk = 1)
pending_onboarding = onboarding_status.objects.get(pk=2)
pending_vendor = vendor_status.objects.get(pk=2)
reject_vendor = vendor_status.objects.get(pk=0)
approve_vendor = vendor_status.objects.get(pk = 1)

all_active_candidates = master_candidate.objects.filter(status=active_status)
candidate_list = master_candidate.objects.filter(status=active_status)

try:
    Onboarding_SPOC_list = User.objects.get(groups__name='Onboarding SPOC')
    Onboarding_SPOC = Onboarding_SPOC_list.email
except ObjectDoesNotExist:
    Onboarding_SPOC = 'workmail052020@gmail.com'


def resend_loi(request, cid):
    selected_candidate = master_candidate.objects.get(pk=cid)
    template = render_to_string('emailtemplates/loi.html', {'candidate_name': selected_candidate.First_Name, 'id':selected_candidate.pk ,'pwd': password,'status': 'Approved' })
    our_email = EmailMessage(
        'LOI',
        template,
        settings.EMAIL_HOST_USER,
        [ selected_candidate.Personal_Email_Id , 'sadaf.shaikh@udaan.com'],
    ) 
    our_email.fail_silently = False    
    our_email.send()
    try:
        my_host = selected_candidate.fk_vendor_code.vendor_smtp
        my_port = selected_candidate.fk_vendor_code.vendor_email_port.port
        my_username = selected_candidate.fk_vendor_code.vendor_email_id
        my_password = selected_candidate.fk_vendor_code.vendor_email_id_password
        my_use_tls = selected_candidate.fk_vendor_code.vendor_email_port.tls
        my_use_ssl = selected_candidate.fk_vendor_code.vendor_email_port.ssl
        subject1 = 'LOI'
        body1 = 'LOI'
        from1 = my_username
        with get_connection(
        host=my_host, 
        port=my_port, 
        username=my_username, 
        password=my_password, 
        use_tls=my_use_tls,
        use_ssl= my_use_ssl
        ) as connection:
            EmailMessage(subject1, body1, from1, [selected_candidate.Personal_Email_Id, 'sadaf.shaikh@udaan.com'],
            connection=connection).send()
    except TimeoutError:
        return HttpResponse("A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond")
    # except SMTPAuthenticationError:
    #     return HttpResponse("Username and Password not accepted. Bad Credentials")
    messages.success(request, "LOI Resent To Candidate")
    return redirect("csp_app:candidate")
    

def custom_send_email(request):
    subject, from_email, to = 'sdf', 'workmail052020@gmail.com', 'sadaf.shaikh@udaan.com'
   
    html_content = render_to_string('emailtemplates/sdf.html') # render with dynamic value
    text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # EMAIL_USE_SSL = False
    # try:
    #     my_host = 'send.one.com'
    #     my_port = 587
    #     my_username = 'sadaf.asgarali@aspire-nxt.com'
    #     my_password = 'sadaf@1234'
    #     my_use_tls = True
    #     subject1 = 'LOI'
    #     body1 = 'LOI'
    #     from1 = my_username
    #     with get_connection(
    #     host=my_host, 
    #     port=my_port, 
    #     username=my_username, 
    #     password=my_password, 
    #     use_tls=my_use_tls,
    #     use_ssl= False
    #     ) as connection:
    #         EmailMessage(subject1, body1, from1, ['sdfworkk@gmail.com'],
    #                     connection=connection).send()
    # except TimeoutError:
    #     return HttpResponse("A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond")
                    
    
    
    return HttpResponse("Mail Sent")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Candidate').exists())
def candidate_profile(request):
    print(request.user)
    try:
        me = master_candidate.objects.get(pk=request.user.username)
        return render(request, 'candidate/candidatesdashboard.html', {'me':me})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Recruiter').exists() or u.groups.filter(name='Onboarding SPOC').exists() or u.groups.filter(name='Vendor').exists())
def view_ss(request,cid):    
    try:
        salaryst = salary_structure.objects.filter(candidate_code=cid)
        candidate = master_candidate.objects.get(pk=cid)
        return render(request, 'candidate/viewsalarystructure.html', {'salaryst':salaryst, 'candidate':candidate})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
def change_password(request):
    selected_user = User.objects.get(email=request.user.email)
    if request.method == 'POST':
        
        pwd = request.POST.get('new_password2')
        selected_user.password = pwd
        selected_user.set_password(selected_user.password)
        selected_user.save()
        return render(request, 'registration/password_reset_complete.html')
    return render(request, 'registration/password_change.html')

def minimum_wage_list(request):
    state_id = request.GET.get('search_state')
    desg_id = request.GET.get('search_type')
    state = master_state.objects.get(pk=state_id)
    desg = master_designation.objects.get(pk=desg_id)
    output = {}
    try:
        wage_list = master_minimum_wages.objects.get(fk_state_code=state.state_name_id, fk_skill_code= desg.fk_skill_code_id, status=active_status)
        output['desg_type'] = wage_list.fk_skill_code.skill_name
        output['state_name'] = wage_list.fk_state_code.state_name
        output['amount'] = wage_list.wages
        return JsonResponse(output)
    except ObjectDoesNotExist:
        output['amount'] = -1
        return JsonResponse(output)

def check_duplicate_candidate_new(request):
    aadhaar = request.GET.get('aadhaar')
    pan = request.GET.get('pan')
    contact_no = request.GET.get('contact_no')
    fathername = request.GET.get('fathername')
    firstname = request.GET.get('firstname')
    middlename = request.GET.get('middlename')
    lastname = request.GET.get('lastname')
    dob = request.GET.get('dob')
    email = request.GET.get('email')
    result = {}
    try:                
        dup_candidate_aadhaar = master_candidate.objects.get(Aadhaar_Number= aadhaar, status= active_status)
        result['adhaar'] = dup_candidate_aadhaar.pk_candidate_code
        result['invalid_domain'] = ''
        return JsonResponse(result)
    except ObjectDoesNotExist:
        result['adhaar'] = ''
    try:
        dup_candidate_pan = master_candidate.objects.get(PAN_Number= pan, status= active_status)
        result['pan'] = dup_candidate_pan.pk_candidate_code
        result['invalid_domain'] = ''
        return JsonResponse(result)
    except ObjectDoesNotExist:
        result['pan'] = ''
    try:
        dup_candidate_contact = master_candidate.objects.get(Contact_Number= contact_no, status= active_status)
        result['contact'] = dup_candidate_contact.pk_candidate_code
        result['invalid_domain'] = ''
        return JsonResponse(result)
    except ObjectDoesNotExist:
        result['contact'] = ''
    try:
       
        dup_candidate_details = master_candidate.objects.get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob,Middle_Name= middlename, Last_Name = lastname, status= active_status)
        result['details'] = dup_candidate_details.pk_candidate_code
        result['invalid_domain'] = ''
        return JsonResponse(result)
    except ObjectDoesNotExist:
        result['details'] = ''
    try:
        if email.endswith('gmail.com') or email.endswith('yahoo.com') or email.endswith('hotmail.com') or email.endswith('outlook.com'):

            dup_candidate_email = master_candidate.objects.get(Personal_Email_Id=email, status= active_status)
            result['email'] = dup_candidate_email.pk_candidate_code
            result['invalid_domain'] = ''
            return JsonResponse(result)
        else:
            result['invalid_domain'] = 'Supported Domains : gmail.com, yahoo.com, hotmail.com, outlook.com'
            return JsonResponse(result)
    except ObjectDoesNotExist:
        result['email'] = ''
        result['invalid_domain'] = ''
    return JsonResponse(result)

def check_duplicate_candidate_edit(request):
    aadhaar = request.GET.get('aadhaar')
    pan = request.GET.get('pan')
    contact_no = request.GET.get('contact_no')
    fathername = request.GET.get('fathername')
    firstname = request.GET.get('firstname')
    middlename = request.GET.get('middlename')
    lastname = request.GET.get('lastname')
    dob = request.GET.get('dob')
    email = request.GET.get('email')
    candidate_id = request.GET.get('candidate_id')
    result = {}
    try:                
        dup_candidate_aadhaar = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Aadhaar_Number= aadhaar, status= active_status)
        result['adhaar'] = dup_candidate_aadhaar.pk_candidate_code
        result['invalid_domain'] = ''
        return JsonResponse(result)
    except ObjectDoesNotExist:
        result['adhaar'] = ''
    try:
        dup_candidate_pan = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(PAN_Number= pan, status= active_status)
        result['pan'] = dup_candidate_pan.pk_candidate_code
        result['invalid_domain'] = ''
        return JsonResponse(result)
    except ObjectDoesNotExist:
        result['pan'] = ''
    try:
        dup_candidate_contact = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Contact_Number= contact_no, status= active_status)
        result['contact'] = dup_candidate_contact.pk_candidate_code
        result['invalid_domain'] = ''
        return JsonResponse(result)
    except ObjectDoesNotExist:
        result['contact'] = ''
    try:
        # dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Date_of_Birth=dob, Father_Name = fathername, status= active_status)
       
        dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Middle_Name= middlename, Last_Name = lastname, Date_of_Birth=dob, status= active_status)
        result['details'] = dup_candidate_details.pk_candidate_code
        result['invalid_domain'] = ''
        return JsonResponse(result)
    except ObjectDoesNotExist:
        result['details'] = ''
    try:
        if email.endswith('gmail.com') or email.endswith('yahoo.com') or email.endswith('hotmail.com') or email.endswith('outlook.com'):

            dup_candidate_email = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Personal_Email_Id=email, status= active_status)
            result['email'] = dup_candidate_email.pk_candidate_code
            result['invalid_domain'] = ''
            return JsonResponse(result)
        else:
            result['invalid_domain'] = 'Supported Domains : gmail.com, yahoo.com, hotmail.com, outlook.com'
            return JsonResponse(result)
    except ObjectDoesNotExist:
        result['email'] = ''
        result['invalid_domain'] = ''
    return JsonResponse(result)


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def minimum_wages(request):
    try:
        wage_list = master_minimum_wages.objects.filter(status=active_status)
        state_list = states.objects.all().order_by('state_name')
        zone_list = zones.objects.all()
        skill_list = skill_type.objects.all().order_by('-skill_name')
        all_active_candidates = master_candidate.objects.filter(status=active_status)
        return render(request, 'csp_app/minimum_wages.html', {'w_list': created_by_wages(),'allcandidates': all_active_candidates, 'wage_list': wage_list, 'state_list': state_list, 'zone_list': zone_list, 'skill_list': skill_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def create_wages(request):
    try:
        if request.method == 'POST':
            state = request.POST.get('state')
            skill = request.POST.get('skill')
            wage = request.POST.get('wage')
            if state == None or state == '':
                messages.warning(request, "Choose  State And Try Again")
                return redirect("csp_app:minimumwages")
            state_fk = states.objects.get(pk= state)
       
            if skill == None or skill == '':
                messages.warning(request, "Choose  Skill And Try Again")
                return redirect("csp_app:minimumwages")
            skill_fk = skill_type.objects.get(pk= skill)
            if wage == None or wage == ' ':
                messages.warning(request, "Choose  Wage And Try Again")
                return redirect("csp_app:minimumwages")
            try:
                dup_wage = master_minimum_wages.objects.get(fk_state_code= state_fk, fk_skill_code= skill_fk,status= active_status)
                messages.error(request, "Minimum wages Already Exist")
                return redirect("csp_app:minimumwages")
            except ObjectDoesNotExist:
                new_wage = master_minimum_wages(fk_state_code= state_fk,fk_skill_code= skill_fk, wages= wage, created_by= str(request.user), created_date_time=  datetime.now())
                new_wage.save()
                messages.success(request, "Minimum wages saved succesfully")
                return redirect("csp_app:minimumwages")

        return render(request, 'csp_app/minimum_wages.html', {'w_list': created_by_wages(),'allcandidates': all_active_candidates, 'wage_list': wage_list, 'state_list': state_list, 'zone_list': zone_list, 'skill_list': skill_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_wages(request):
    try:
        if request.method == 'POST':
            wage_id = request.POST.get("delete_id")
        
            selected_wage = master_minimum_wages.objects.get(pk = wage_id)
            selected_wage.modified_by = str(request.user)
            selected_wage.modified_date_time = datetime.now()
            selected_wage.status = deactive_status
            selected_wage.save()
            messages.success(request, "Minimum Wage Deleted Successfully")
            return redirect('csp_app:minimumwages')
        return render(request, 'csp_app/minimum_wages.html', {'allcandidates': all_active_candidates, 'wage_list': wage_list, 'state_list': state_list, 'zone_list': zone_list, 'skill_list': skill_list})
        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_wages(request):
    wage_list = master_minimum_wages.objects.filter(status=active_status)
    state_list = states.objects.all().order_by('state_name')
    skill_list = skill_type.objects.all().order_by('-skill_name')
    try:
        if request.method == 'POST':
            wage_id = request.POST.get("view_id")
            view_wage_list = master_minimum_wages.objects.filter(pk = wage_id)
        return render(request, 'csp_app/view_minimum_wages.html', {'w_list': created_by_wages(),'allcandidates': all_active_candidates,'view_wage_list': view_wage_list, 'wage_list': wage_list, 'state_list': state_list, 'skill_list': skill_list})
        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_wages(request):
    wage_list = master_minimum_wages.objects.filter(status=active_status)
    state_list = states.objects.all().order_by('state_name')
    skill_list = skill_type.objects.all().order_by('-skill_name')
    
    try:
        if request.method == 'POST':
            wage_id = request.POST.get("view_id")
            selected_wage = master_minimum_wages.objects.filter(pk = wage_id)         
           
        return render(request, 'csp_app/edit_minimum_wages.html', {'w_list': created_by_wages(),'allcandidates': all_active_candidates,'view_wage_list': selected_wage, 'wage_list': wage_list, 'state_list': state_list, 'skill_list': skill_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_wages(request):
    wage_list = master_minimum_wages.objects.filter(status=active_status)
    state_list = states.objects.all().order_by('state_name')
    skill_list = skill_type.objects.all().order_by('-skill_name')
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_minimum_wages.objects.get(pk = request.POST.get("e_id"))
                selected_wage = master_minimum_wages.objects.filter(pk = request.POST.get("e_id"))
                if request.POST.get("wage") != None:
                    state = request.POST.get('state')
                    skill = request.POST.get('skill')
                    wage = request.POST.get('wage')
                    if state == None or state == '':
                        messages.warning(request, "Choose  State And Try Again")
                        return redirect("csp_app:minimumwages")
                    state_fk = states.objects.get(pk= state)
                   
                    if skill == None or skill == '':
                        messages.warning(request, "Choose  Skill And Try Again")
                        return redirect("csp_app:minimumwages")
                    skill_fk = skill_type.objects.get(pk= skill)
                    if wage == None or wage == ' ':
                        messages.warning(request, "Choose  Wage And Try Again")
                        return redirect("csp_app:minimumwages")
                    try:
                        d = master_minimum_wages.objects.get(fk_state_code=state_fk, fk_skill_code= skill_fk,status= active_status)
                        messages.error(request, "Minimum Wages Already Exist")
                        return redirect('csp_app:minimumwages')
                        # print(5)
                        
                    except ObjectDoesNotExist:
                        selected.fk_state_code = state_fk
                        selected.fk_skill_code = skill_fk
                        selected.wages = wage
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "Minimum Wages Updated Successfully")
                        return redirect('csp_app:minimumwages')
                else:
                    messages.warning(request, "Wages Cannot Be Blank")
                    return redirect('csp_app:minimumwages')         
           
        return render(request, 'csp_app/edit_minimum_wages.html', {'w_list': created_by_wages(),'allcandidates': all_active_candidates,'view_wage_list': selected_wage, 'wage_list': wage_list, 'state_list': state_list,  'skill_list': skill_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  


def vendor_candidates(usrname):
    try:
        a = []
        s_vendor = master_vendor.objects.filter(spoc_email_id= usrname, status=active_status)
        for e in s_vendor:
            a = chain(master_candidate.objects.filter(fk_vendor_code=e.pk,onboarding_status= approve_onboarding, status= active_status))
        
        vs_candidates = list(a)
        return vs_candidates
    except ObjectDoesNotExist:
        pass

def vendor_pending_candidates(usrname):
    try:
        s_vendor = master_vendor.objects.filter(spoc_email_id= usrname, status=active_status)
        a = []
        for e in s_vendor:
            a = chain(master_candidate.objects.filter(fk_vendor_code=e.pk, vendor_status= pending_vendor,onboarding_status= approve_onboarding, status= active_status) | master_candidate.objects.filter(fk_vendor_code=e.pk, vendor_status= pending_vendor,onboarding_status= onboarding_status.objects.get(pk=4), status= active_status))
        vs_candidates = list(a)
        
        return vs_candidates
    except ObjectDoesNotExist:
        pass

def onboarding_candidates(usrname):
    try:
        onb_candidates = master_candidate.objects.filter( Onboarding_Spoc_Email_Id=usrname,status= active_status)
        # print(onb_candidates)
        return onb_candidates
    except ObjectDoesNotExist:
        pass

def onboarding_pending_candidates(usrname):
    try:
        onb_candidates = master_candidate.objects.filter( Onboarding_Spoc_Email_Id=usrname, onboarding_status= pending_onboarding , status= active_status)
        # print(onb_candidates)
        return onb_candidates
    except ObjectDoesNotExist:
        pass

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Onboarding SPOC').exists() or u.groups.filter(name='Vendor').exists() or u.groups.filter(name='Admin').exists())
def process_requests(request, cid):
    candidate_id = cid
    for eachgroup in request.user.groups.all():
        if str(eachgroup) == 'Vendor':
            candidate_list = vendor_candidates(request.user)
            all_active_candidates = vendor_candidates(request.user)
            pending_candidate_list = vendor_pending_candidates(request.user)
            count = len(pending_candidate_list)
        elif str(eachgroup) == 'Onboarding SPOC':
            candidate_list = onboarding_candidates(request.user)
            all_active_candidates = onboarding_candidates(request.user)
            pending_candidate_list = onboarding_pending_candidates(request.user)
            count = len(pending_candidate_list)
        else:
            
            all_active_candidates = candidate_list = master_candidate.objects.filter(status=active_status)
            
            pending_candidate_list = master_candidate.objects.filter(onboarding_status= pending_onboarding,status=active_status ) 
            # | master_candidate.objects.filter(vendor_status= pending_vendor,status=active_status )
            count = len(pending_candidate_list)   
    try:
        selected_candidate_data = master_candidate.objects.filter(pk= cid)
        # selected_candidate = ''
        entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list = candidate_form_lists()
        c_status_list = candidate_status.objects.all()
        v_status_list = vendor_status.objects.all()
        if request.method == 'POST':
            candidate_id = request.POST.get('cid')
            firstname = request.POST.get("c_firstname").capitalize()
            middlename = request.POST.get("c_middlename").capitalize()
            lastname = request.POST.get("c_lastname").capitalize()
            dob = request.POST.get("c_dob")
            contact_no = request.POST.get("c_contact")
            emergency_no = request.POST.get("c_emergency")
            email = request.POST.get("c_email")
            c_gender = request.POST.get("c_gender")
            fathername = request.POST.get("c_fathername").capitalize()
            mothername = request.POST.get("c_mothername").capitalize()
            aadhaar = request.POST.get("c_aadhaar")
            Pan = request.POST.get("c_pan")
            hiring = request.POST.get("c_hiring_type")
            doj = request.POST.get("c_doj")        
            replacement = request.POST.get("c_replacement")
             
            referral = request.POST.get("c_referral")
             
            subsource = request.POST.get("c_sub_source")
            entity = request.POST.get("c_entity")
            vendor = request.POST.get("c_vendor")
            department = request.POST.get("c_dept")
            function = request.POST.get("c_function")
            team = request.POST.get("c_team")
            sub_team = request.POST.get("c_subteam")
            designation = request.POST.get("c_desg")
            region = request.POST.get("c_region")
            state = request.POST.get("c_state")
            city = request.POST.get("c_city")
            location = request.POST.get("c_location")
            # ta_spoc = request.user.email #check
            onboarding_spoc = Onboarding_SPOC #check
            reporting_manager = request.POST.get("c_reporting_manager")
            reporting_manager_email = request.POST.get("c_reporting_manager_email")
            email_creation = request.POST.get("c_email_creation")
            laptopallocation = request.POST.get("c_laptop_allocation")
            salarytype = request.POST.get("c_salary_type")
            gross_salary = request.POST.get("c_gross_salary")
            loc_code = request.POST.get("c_gross_salary")
            
            if hiring == None or hiring == '':
                messages.warning(request, "Choose Hiring Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            hiring_fk = hiring_type.objects.get(pk= hiring)
            if sub_source == None or sub_source == '':
                messages.warning(request, "Choose  Sub Source And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            subsource_fk = sub_source.objects.get(pk= subsource)
            if c_gender == None or c_gender == '':
                messages.warning(request, "Choose  Gender And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            gender_fk = gender.objects.get(pk= c_gender)
            if laptopallocation == None or laptopallocation == '':
                messages.warning(request, "Choose  Laptop Allocation And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            la_fk = laptop_allocation.objects.get(pk= laptopallocation)
            if salarytype == None or salarytype == '':
                messages.warning(request, "Choose  Salary Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            salarytype_fk = salary_type.objects.get(pk= salarytype)
            if entity == None or entity == '':
                messages.warning(request, "Choose  Company  And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            entity_fk = master_entity.objects.get(pk= entity)
            if vendor == None or vendor == '':
                messages.warning(request, "Choose  vendor And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            vendor_fk = master_vendor.objects.get(pk= vendor)
            if department == None or department == '':
                messages.warning(request, "Choose  Department  And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            department_fk = master_department.objects.get(pk= department)
            if function == None or function == '':
                messages.warning(request, "Choose  Function  And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            function_fk = master_function.objects.get(pk= function)
            if team == None or team == '':
                messages.warning(request, "Choose  Team  And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            team_fk = master_team.objects.get(pk= team)
            if sub_team == None or sub_team == '':
                messages.warning(request, "Choose  Sub Team  And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            sub_team_fk = master_sub_team.objects.get(pk= sub_team)
            if designation == None or designation == '':
                messages.warning(request, "Choose  Designation  And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            designation_fk = master_designation.objects.get(pk= designation)
            if region == None or region == '':
                messages.warning(request, "Choose  Region  And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            region_fk = master_region.objects.get(pk= region)
            if state == None or state == '':
                messages.warning(request, "Choose  State  And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            state_fk = master_state.objects.get(pk= state)
            if city == None or city == '':
                messages.warning(request, "Choose  City  And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            city_fk = master_city.objects.get(pk= city)
            if location == None or location == '':
                messages.warning(request, "Choose  Location And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            location_fk = master_location.objects.get(pk= location)
            spoc_status = request.POST.get('s_status')
            try:                
                dup_candidate_aadhaar = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Aadhaar_Number= aadhaar, status= active_status)
                messages.error( request, "Aadhaar Number Already Exist")
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_pan = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(PAN_Number= Pan, status= active_status)
                messages.error( request, "PAN  Already Exist")
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_contact = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Contact_Number= contact_no, status= active_status)
                messages.error( request, "Contact Number Already Exist")
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                pass
            try:
            
                dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                messages.error( request, "Candidate Already Exist")
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_email = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Personal_Email_Id=email, status= active_status)
                messages.error( request, "Candidate Email Already Exist")
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                messages.error( request, "Same Candidate Exist with ID : " + dup_candidate_details.pk)
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                selected_candidate = master_candidate.objects.get(pk= candidate_id)
                changes_list = check_for_changes(selected_candidate, firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, hiring, replacement, email, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, reporting_manager, reporting_manager_email, gender_fk, email_creation, onboarding_spoc, la_fk, salarytype_fk, salarytype, gross_salary)
                
                selected_candidate.modified_by = str(request.user)
                selected_candidate.modified_date_time= datetime.now()

                for eachgroup in request.user.groups.all():
                    if str(eachgroup) == 'Admin':
                        selected_candidate.onboarding_status = approve_onboarding
                        selected_candidate.vendor_status = pending_vendor
                        selected_candidate.loi_status = loi_status.objects.get(pk=0)
                        selected_candidate.documentation_status = documentation_status.objects.get(pk=2)
                        selected_candidate.offer_letter_status = offer_letter_status.objects.get(pk=0)
                        selected_candidate.it_intimation_status = IT_intimation_status.objects.get(pk=0)
                        selected_candidate.joining_status = joining_status.objects.get(pk=0)
                        e = ecode_generation_status.objects.get(pk=0)
                        selected_candidate.ecode_status = e.status_name
                        if selected_candidate.E_Mail_ID_Creation == 'Yes':
                            selected_candidate.email_creation_status = email_creation_request_status.objects.get(pk=0)
                        if selected_candidate.Laptop_Allocation_id == 1:
                            selected_candidate.laptop_status = laptop_request_status.objects.get(pk=0)
                        selected_candidate.candidate_status = candidate_status.objects.get(pk=2)
                        if len(changes_list) > 0:
                            selected_candidate.onboarding_status = onboarding_status.objects.get(pk=4)
                        selected_candidate.save()
                    
                        
                        limtemplate = render_to_string('emailtemplates/candidate_edited_by_onboarding_et.html', {'candidate_code':candidate_id ,'user': request.user, 'vendor': vendor_fk.vendor_name })
                        our_email = EmailMessage(
                            'Candidate Edited By Admin.',
                            limtemplate,
                            settings.EMAIL_HOST_USER,
                            [ vendor_fk.vendor_email_id , 'sadaf.shaikh@udaan.com'],
                        ) 
                        our_email.fail_silently = False
                        our_email.send()
                        
                        alltemplate = render_to_string('emailtemplates/candidate_edited_by_onboarding_admin_et.html', {'candidate_code':cid ,'user': request.user, 'changes': changes_list})
                        our_email = EmailMessage(
                            'Candidate account edited by admin.',
                            alltemplate,
                            settings.EMAIL_HOST_USER,
                            [ 'sadaf.shaikh@udaan.com', 'workmail052020@gmail.com', Onboarding_SPOC ],
                        ) 
                        our_email.fail_silently = False
                        our_email.send()
                        
                        messages.success(request, "Candidate details mailed to vendor.")
                        return redirect("csp_app:pending_request")

                    

                if request.POST.get('o_status') != None:
                    selected_candidate.onboarding_status = approve_onboarding
                    selected_candidate.vendor_status = pending_vendor
                    selected_candidate.loi_status = loi_status.objects.get(pk=0)
                    selected_candidate.documentation_status = documentation_status.objects.get(pk=2)
                    selected_candidate.offer_letter_status = offer_letter_status.objects.get(pk=0)
                    selected_candidate.it_intimation_status = IT_intimation_status.objects.get(pk=0)
                    selected_candidate.joining_status = joining_status.objects.get(pk=0)
                    e = ecode_generation_status.objects.get(pk=0)
                    selected_candidate.ecode_status = e.status_name
                    if selected_candidate.E_Mail_ID_Creation == 'Yes':
                        selected_candidate.email_creation_status = email_creation_request_status.objects.get(pk=0)
                    if selected_candidate.Laptop_Allocation_id == 1:
                        selected_candidate.laptop_status = laptop_request_status.objects.get(pk=0)
                    if len(changes_list) > 0:
                        selected_candidate.onboarding_status = onboarding_status.objects.get(pk=4)
                    selected_candidate.save()
                    
                    limtemplate = render_to_string('emailtemplates/candidate_edited_by_onboarding_et.html', {'candidate_code':cid ,'user': request.user, 'vendor': vendor_fk.vendor_name })
                    our_email = EmailMessage(
                        'Candidate Edited .',
                        limtemplate,
                        settings.EMAIL_HOST_USER,
                        [ vendor_fk.vendor_email_id , 'sadaf.shaikh@udaan.com'],
                    ) 
                    our_email.fail_silently = False
                    our_email.send()
                    
                    alltemplate = render_to_string('emailtemplates/candidate_edited_by_onboarding_admin_et.html', {'candidate_code':cid ,'user': request.user, 'changes': changes_list})
                    our_email = EmailMessage(
                        'Candidate account edited.',
                        alltemplate,
                        settings.EMAIL_HOST_USER,
                        [ 'sadaf.shaikh@udaan.com', 'workmail052020@gmail.com', Onboarding_SPOC],
                    ) 
                    our_email.fail_silently = False
                    our_email.send()
                    
                    messages.success(request, "Candidate details mailed to vendor.")
                    return redirect("csp_app:pending_request")

                
                if request.POST.get('ve_status') != None:                   
                    print(changes_list)
                    print(len(changes_list))
                    if len(changes_list) > 0:
                        selected_candidate.vendor_status = vendor_status.objects.get(pk=4)
                        selected_candidate.onboarding_status = onboarding_status.objects.get(pk=2)
                        
                        selected_candidate.loi_status = loi_status.objects.get(pk=3)
                        selected_candidate.documentation_status = documentation_status.objects.get(pk=3)
                        selected_candidate.offer_letter_status = offer_letter_status.objects.get(pk=3)
                        selected_candidate.it_intimation_status = IT_intimation_status.objects.get(pk=3)
                        selected_candidate.joining_status = joining_status.objects.get(pk=3)
                        e = ecode_generation_status.objects.get(pk=3)
                        selected_candidate.ecode_status = e.status_name
                        if selected_candidate.E_Mail_ID_Creation == 'Yes':
                            selected_candidate.email_creation_status = email_creation_request_status.objects.get(pk=3)
                        if selected_candidate.Laptop_Allocation_id == 1:
                            selected_candidate.laptop_status = laptop_request_status.objects.get(pk=3)
                        selected_candidate.save()
                        #modified email
                        alltemplate = render_to_string('emailtemplates/candidate_edited_by_onboarding_admin_et.html', {'candidate_code':cid ,'user': request.user, 'changes': changes_list})
                        our_email = EmailMessage(
                            'Modified and approved',
                            alltemplate,
                            settings.EMAIL_HOST_USER,
                            [ 'sadaf.shaikh@udaan.com', 'workmail052020@gmail.com', Onboarding_SPOC],
                        ) 
                        our_email.fail_silently = False
                        our_email.send()
                        messages.success(request, "Candidate Details Sent To Onboarding For Approval.")
                        return redirect("csp_app:pending_request")
                    

                    else:
                        selected_candidate.vendor_status = approve_vendor
                        selected_candidate.loi_status = loi_status.objects.get(pk=0)
                        selected_candidate.documentation_status = documentation_status.objects.get(pk=2)
                        selected_candidate.offer_letter_status = offer_letter_status.objects.get(pk=0)
                        selected_candidate.it_intimation_status = IT_intimation_status.objects.get(pk=0)
                        selected_candidate.joining_status = joining_status.objects.get(pk=0)
                        e = ecode_generation_status.objects.get(pk=0)
                        selected_candidate.ecode_status = e.status_name
                        if selected_candidate.E_Mail_ID_Creation == 'Yes':
                            selected_candidate.email_creation_status = email_creation_request_status.objects.get(pk=0)
                        if selected_candidate.Laptop_Allocation_id == 1:
                            selected_candidate.laptop_status = laptop_request_status.objects.get(pk=0)
                        selected_candidate.candidate_status = candidate_status.objects.get(pk=1)
                        limtemplate = render_to_string('emailtemplates/candidate_edited_by_onboarding_et.html', {'candidate_code':cid ,'user': request.user, 'vendor': vendor_fk.vendor_name })
                        our_email = EmailMessage(
                            'Candidate Edited By Vendor.',
                            limtemplate,
                            settings.EMAIL_HOST_USER,
                            [ vendor_fk.vendor_email_id , 'sadaf.shaikh@udaan.com'],
                        ) 
                        our_email.fail_silently = False
                        our_email.send()
                        
                        alltemplate = render_to_string('emailtemplates/candidate_edited_by_onboarding_admin_et.html', {'candidate_code':cid ,'user': request.user, 'changes': changes_list})
                        our_email = EmailMessage(
                            'Candidate approved by vendor.',
                            alltemplate,
                            settings.EMAIL_HOST_USER,
                            [ 'sadaf.shaikh@udaan.com', 'workmail052020@gmail.com', Onboarding_SPOC],
                        ) 
                        our_email.fail_silently = False
                        our_email.send()
                        try:
                            IT_email = IT_Email_ID.objects.get(pk=1)
                            IT_email_id = IT_email.email_id
                        except ObjectDoesNotExist:
                            IT_email_id = 'rahul.gandhi@udaan.com'
                        alltemplate = render_to_string('emailtemplates/it_intimation.html')
                        our_email = EmailMessage(
                            'IT Intimation',
                            alltemplate,
                            settings.EMAIL_HOST_USER,
                            [ 'sadaf.shaikh@udaan.com', 'workmail052020@gmail.com', IT_email_id],
                        ) 
                        our_email.fail_silently = False
                        our_email.send()
                        

                        assign_group = Group.objects.get(name='Candidate')                     
                        user = User.objects.create_user(selected_candidate.pk)
                        password = User.objects.make_random_password()
                        user.password = password
                        user.set_password(user.password)
                        user.first_name = selected_candidate.First_Name
                        user.last_name = selected_candidate.Last_Name
                        user.email = selected_candidate.Personal_Email_Id
                        # if group == 'Candidate':
                        #     user.is_staff = False
                        assign_group.user_set.add(user)
                        user.save()
                        try:
                            u = User.objects.get(username= selected_candidate.Reporting_Manager_E_Mail_ID)
                            # new_reporting_manager_candidate_approve
                            subject, from_email, to = 'Candidate Approved', 'workmail052020@gmail.com', selected_candidate.Reporting_Manager_E_Mail_ID
   
                            html_content = render_to_string('emailtemplates/old_reporting_manager_candidate_approve.html',{'rm': selected_candidate.Reporting_Manager, 'cid': selected_candidate.pk, 'desg': selected_candidate.fk_designation_code})
                            text_content = strip_tags(html_content)
                            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
                        except ObjectDoesNotExist:
                            user = User.objects.create_user(selected_candidate.Reporting_Manager_E_Mail_ID)
                            password = User.objects.make_random_password()
                            user.password = password
                            user.set_password(user.password)
                            user.first_name = selected_candidate.Reporting_Manager
                            user.email = selected_candidate.Reporting_Manager_E_Mail_ID
                           
                            user.save()
                            subject, from_email, to = 'Candidate Approved', 'workmail052020@gmail.com', selected_candidate.Reporting_Manager_E_Mail_ID
   
                            html_content = render_to_string('emailtemplates/new_reporting_manager_candidate_approve.html',{'rm': selected_candidate.Reporting_Manager, 'cid': selected_candidate.pk, 'desg': selected_candidate.fk_designation_code, 'username': selected_candidate.Reporting_Manager_E_Mail_ID,'pwd': password})
                            text_content = strip_tags(html_content)
                            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
                        
                        template = render_to_string('emailtemplates/loi.html', {'candidate_name': selected_candidate.First_Name, 'id':selected_candidate.pk ,'pwd': password,'status': 'Approved' })
                        our_email = EmailMessage(
                            'LOI',
                            template,
                            settings.EMAIL_HOST_USER,
                            [ selected_candidate.Personal_Email_Id , 'sadaf.shaikh@udaan.com'],
                        ) 
                        our_email.fail_silently = False
                        selected_candidate.loi_status = loi_status.objects.get(pk=1)
                        selected_candidate.save()
                        our_email.send()
                        
                        try:
                            my_host = selected_candidate.fk_vendor_code.vendor_smtp
                            my_port = selected_candidate.fk_vendor_code.vendor_email_port.port
                            my_username = selected_candidate.fk_vendor_code.vendor_email_id
                            my_password = selected_candidate.fk_vendor_code.vendor_email_id_password
                            my_use_tls = selected_candidate.fk_vendor_code.vendor_email_port.tls
                            my_use_ssl = selected_candidate.fk_vendor_code.vendor_email_port.ssl
                            subject1 = 'LOI'
                            body1 = 'LOI'
                            from1 = my_username
                            with get_connection(
                            host=my_host, 
                            port=my_port, 
                            username=my_username, 
                            password=my_password, 
                            use_tls=my_use_tls,
                            use_ssl= my_use_ssl
                            ) as connection:
                                EmailMessage(subject1, body1, from1, [selected_candidate.Personal_Email_Id, 'sadaf.shaikh@udaan.com'],
                                            connection=connection).send()
                        except TimeoutError:
                            return HttpResponse("A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond")
                        # send_mail(subject, message, from_email= vendoremail, [selected_candidate.Personal_Email_Id], fail_silently=False, auth_user=vendoremail, auth_password=password)
    
                        messages.success(request, "Candidate approved LOI sent to candidate.")
                        return redirect("csp_app:pending_request")

        delay_joiners = master_candidate.objects.filter(candidate_status=candidate_status.objects.get(pk=7))
        dojcount = len(delay_joiners)
        return render(request, 'candidate/processrequests.html', {'selected_candidate': selected_candidate_data, 'dojcount':dojcount, 'count': count, 'allcandidates': all_active_candidates,'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
        'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
        'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
        'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
        'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

def check_for_changes(selected_candidate, firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, hiring, replacement, email, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, reporting_manager, reporting_manager_email, gender_fk, email_creation, onboarding_spoc, la_fk, salarytype_fk, salarytype, gross_salary):
    changes_list = {}
    if selected_candidate.First_Name != firstname:
        changes_list['First Name'] = [ selected_candidate.First_Name, firstname ]
    selected_candidate.First_Name=firstname 
    if selected_candidate.Middle_Name != middlename:
        changes_list['Middle Name'] = [ selected_candidate.Middle_Name, middlename ]
    selected_candidate.Middle_Name=middlename 
    if selected_candidate.Last_Name != lastname: 
        changes_list['Last Name'] = [ selected_candidate.Last_Name, lastname ]
    selected_candidate.Last_Name= lastname
    if selected_candidate.Date_of_Joining != doj:
        changes_list['Date Of Joining'] = [ selected_candidate.Date_of_Joining, doj ]
    selected_candidate.Date_of_Joining = doj
    if selected_candidate.Date_of_Birth != dob:
        changes_list['Date Of Birth'] = [ selected_candidate.Date_of_Birth, dob ]
    selected_candidate.Date_of_Birth= dob
    if selected_candidate.Father_Name != fathername:
        changes_list['Father Name'] = [ selected_candidate.Father_Name, fathername ]
    selected_candidate.Father_Name= fathername
    if selected_candidate.Mother_Name != mothername:
        changes_list['Mother Name'] = [ selected_candidate.Mother_Name, mothername ]
    selected_candidate.Mother_Name= mothername
    if selected_candidate.Aadhaar_Number != aadhaar:
        changes_list['Aadhaar Number'] = [ selected_candidate.Aadhaar_Number, aadhaar ]                    
    selected_candidate.Aadhaar_Number= aadhaar
    if selected_candidate.PAN_Number != Pan:
        changes_list['PAN Number'] = [ selected_candidate.PAN_Number, Pan ]

    selected_candidate.PAN_Number= Pan
    if selected_candidate.Contact_Number != contact_no:
        changes_list['Contact Number'] = [ selected_candidate.Contact_Number, contact_no ]

    selected_candidate.Contact_Number= contact_no
    if selected_candidate.Emergency_Contact_Number != emergency_no:
        changes_list['Emergency Contact Number'] = [ selected_candidate.Emergency_Contact_Number, emergency_no ]
    selected_candidate.Emergency_Contact_Number= emergency_no
    if selected_candidate.Type_of_Hiring != hiring_fk:
        changes_list['Type of Hiring'] = [ selected_candidate.Type_of_Hiring, hiring ]

    selected_candidate.Type_of_Hiring= hiring_fk
    if selected_candidate.Replacement != replacement:
        changes_list['Replacement'] = [ selected_candidate.Replacement, replacement ]                    
    selected_candidate.Replacement= replacement
    if selected_candidate.Personal_Email_Id != email:
        changes_list['Personal Email Id'] = [ selected_candidate.Personal_Email_Id, email ]  
    selected_candidate.Personal_Email_Id= email
    if selected_candidate.Sub_Source != subsource_fk:
        changes_list['Sub Source'] = [ selected_candidate.Sub_Source, subsource_fk ]
    selected_candidate.Sub_Source= subsource_fk
    if selected_candidate.Referral != referral:
        changes_list['Referral'] = [ selected_candidate.Referral, referral ]
    selected_candidate.Referral= referral
    if selected_candidate.fk_vendor_code != vendor_fk:
        changes_list['Vendor Code'] = [ selected_candidate.fk_vendor_code, vendor_fk ]
    selected_candidate.fk_vendor_code= vendor_fk
    if selected_candidate.fk_entity_code != entity_fk:
        changes_list['entity Code'] = [ selected_candidate.fk_entity_code, entity_fk ]
    selected_candidate.fk_entity_code= entity_fk
    if selected_candidate.fk_department_code != department_fk:
        changes_list['department Code'] = [ selected_candidate.fk_department_code, department_fk ]
    selected_candidate.fk_department_code= department_fk
    if selected_candidate.fk_function_code != function_fk:
        changes_list['function Code'] = [ selected_candidate.fk_function_code, function_fk ]
    selected_candidate.fk_function_code= function_fk
    if selected_candidate.fk_team_code != team_fk:
        changes_list['team Code'] = [ selected_candidate.fk_team_code, team_fk ]
    selected_candidate.fk_team_code= team_fk
    if selected_candidate.fk_subteam_code != sub_team_fk:
        changes_list['subteam Code'] = [ selected_candidate.fk_subteam_code, sub_team_fk ]
    selected_candidate.fk_subteam_code= sub_team_fk
    if selected_candidate.fk_designation_code != designation_fk:
        changes_list['designation Code'] = [ selected_candidate.fk_designation_code, designation_fk ]
    selected_candidate.fk_designation_code= designation_fk
    if selected_candidate.fk_region_code != region_fk:
        changes_list['region Code'] = [ selected_candidate.fk_region_code, region_fk ]
    selected_candidate.fk_region_code= region_fk
    if selected_candidate.fk_state_code != state_fk:
        changes_list['state Code'] = [ selected_candidate.fk_state_code, state_fk ]
    selected_candidate.fk_state_code= state_fk
    if selected_candidate.fk_city_code != city_fk:
        changes_list['City Code'] = [ selected_candidate.fk_city_code, city_fk ]
    selected_candidate.fk_city_code= city_fk
    if selected_candidate.fk_location_code != location_fk:
        changes_list['location Code'] = [ selected_candidate.fk_location_code, location_fk ]
    selected_candidate.fk_location_code= location_fk
    if selected_candidate.Reporting_Manager != reporting_manager:
        changes_list['Reporting Manager'] = [ selected_candidate.Reporting_Manager, reporting_manager ]
    selected_candidate.Reporting_Manager= reporting_manager
    if selected_candidate.Reporting_Manager_E_Mail_ID != reporting_manager_email:
        changes_list['Reporting Manager E Mail ID'] = [ selected_candidate.Reporting_Manager_E_Mail_ID, reporting_manager_email ]
    selected_candidate.Reporting_Manager_E_Mail_ID= reporting_manager_email
    if selected_candidate.Gender != gender_fk:
        changes_list['Gender'] = [ selected_candidate.Gender, gender_fk ]
    selected_candidate.Gender= gender_fk
    if selected_candidate.E_Mail_ID_Creation != email_creation:
        changes_list['E Mail ID Creation'] = [ selected_candidate.E_Mail_ID_Creation, email_creation ]
    selected_candidate.E_Mail_ID_Creation= email_creation

    if selected_candidate.Onboarding_Spoc_Email_Id != onboarding_spoc:
        changes_list['Onboarding Spoc Email Id'] = [ selected_candidate.Onboarding_Spoc_Email_Id, onboarding_spoc ]
    selected_candidate.Onboarding_Spoc_Email_Id= onboarding_spoc
    if selected_candidate.Laptop_Allocation != la_fk:
        changes_list['Laptop Allocation'] = [ selected_candidate.Laptop_Allocation, la_fk ]
    selected_candidate.Laptop_Allocation= la_fk
    if selected_candidate.Salary_Type != salarytype_fk:
        changes_list['Salary Type'] = [ selected_candidate.Salary_Type, salarytype ]
    selected_candidate.Salary_Type= salarytype_fk
  
    x = format(float(gross_salary), '.1f')
    y = format(float(selected_candidate.Gross_Salary_Amount), '.1f')
       
    if x != y:
        changes_list['Gross Salary Amount'] = [ selected_candidate.Gross_Salary_Amount, gross_salary ]
    selected_candidate.Gross_Salary_Amount= gross_salary
   
    return changes_list




@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Onboarding SPOC').exists() or u.groups.filter(name='Admin').exists())
def reject_candidate_onboarding(request, cid):
    try:
        
        selected_candidate = master_candidate.objects.get(pk = cid)
        selected_candidate.onboarding_status = reject_onboarding
        selected_candidate.vendor_status = vendor_status.objects.get(pk=3)
        selected_candidate.loi_status = loi_status.objects.get(pk=3)
        selected_candidate.documentation_status = documentation_status.objects.get(pk=3)
        selected_candidate.offer_letter_status = offer_letter_status.objects.get(pk=3)
        selected_candidate.it_intimation_status = IT_intimation_status.objects.get(pk=3)
        selected_candidate.joining_status = joining_status.objects.get(pk=3)
        e = ecode_generation_status.objects.get(pk=3)
        selected_candidate.ecode_status = e.status_name
        
        selected_candidate.email_creation_status = email_creation_request_status.objects.get(pk=3)
        selected_candidate.laptop_status = laptop_request_status.objects.get(pk=3)
        selected_candidate.candidate_status = candidate_status.objects.get(pk=0)
        selected_candidate.save()
        alltemplate = render_to_string('emailtemplates/candidate_edited_by_onboarding_admin_et.html', {'candidate_code':cid ,'user': request.user})
        our_email = EmailMessage(
            'Candidate Rejected.',
            alltemplate,
            settings.EMAIL_HOST_USER,
            [ 'sadaf.shaikh@udaan.com', 'workmail052020@gmail.com', Onboarding_SPOC],
        ) 
        our_email.fail_silently = False
        our_email.send()
        
        messages.success(request, "Candidate Rejected Mail Sent To Admin.")
        return redirect("csp_app:pending_request")

    except UnboundLocalError:
        return HttpResponse("No Data To Display.")


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Vendor').exists() or u.groups.filter(name='Admin').exists())
def reject_candidate_vendor(request, cid):
    try:
        selected_candidate = master_candidate.objects.get(pk = cid)
        for eachgroup in request.user.groups.all():
            if str(eachgroup) == 'Admin':
                selected_candidate.onboarding_status = reject_onboarding
                
                selected_candidate.loi_status = loi_status.objects.get(pk=3)
                selected_candidate.documentation_status = documentation_status.objects.get(pk=3)
                selected_candidate.offer_letter_status = offer_letter_status.objects.get(pk=3)
                selected_candidate.it_intimation_status = IT_intimation_status.objects.get(pk=3)
                selected_candidate.joining_status = joining_status.objects.get(pk=3)
                e = ecode_generation_status.objects.get(pk=3)
                selected_candidate.ecode_status = e.status_name
                
                selected_candidate.email_creation_status = email_creation_request_status.objects.get(pk=3)
                selected_candidate.laptop_status = laptop_request_status.objects.get(pk=3)
                selected_candidate.candidate_status = candidate_status.objects.get(pk=0)
                selected_candidate.save()
                alltemplate = render_to_string('emailtemplates/candidate_edited_by_vendor_admin_et.html', {'candidate_code':cid ,'user': request.user})
                our_email = EmailMessage(
                    'Candidate Rejected By Admin.',
                    alltemplate,
                    settings.EMAIL_HOST_USER,
                    [ 'sadaf.shaikh@udaan.com', 'workmail052020@gmail.com', Onboarding_SPOC],
                ) 
                our_email.fail_silently = False
                our_email.send()
                template = render_to_string('emailtemplates/candidate_edited_by_vendor_et.html', {'candidate_code':cid ,'user': request.user, 'vendor': selected_candidate.fk_vendor_code.vendor_name })
                our_email = EmailMessage(
                    'Candidate Rejected By Admin.',
                    template,
                    settings.EMAIL_HOST_USER,
                    [ 'sadaf.shaikh@udaan.com', selected_candidate.Onboarding_Spoc_Email_Id],
                ) 
                our_email.fail_silently = False
                our_email.send()
                
                messages.success(request, "Candidate Rejected .") 
                return redirect("csp_app:pending_request")
            elif str(eachgroup) == 'Onboarding SPOC':
                selected_candidate.onboarding_status = reject_onboarding
                selected_candidate.vendor_status = vendor_status.objects.get(pk=3)
                selected_candidate.loi_status = loi_status.objects.get(pk=3)
                selected_candidate.documentation_status = documentation_status.objects.get(pk=3)
                selected_candidate.offer_letter_status = offer_letter_status.objects.get(pk=3)
                selected_candidate.it_intimation_status = IT_intimation_status.objects.get(pk=3)
                selected_candidate.joining_status = joining_status.objects.get(pk=3)
                e = ecode_generation_status.objects.get(pk=3)
                selected_candidate.ecode_status = e.status_name
                selected_candidate.email_creation_status = email_creation_request_status.objects.get(pk=3)
                selected_candidate.laptop_status = laptop_request_status.objects.get(pk=3)
                selected_candidate.candidate_status = candidate_status.objects.get(pk=0)
                selected_candidate.save()
                alltemplate = render_to_string('emailtemplates/candidate_edited_by_onboarding_admin_et.html', {'candidate_code':cid ,'user': request.user})
                our_email = EmailMessage(
                    'Candidate Rejected.',
                    alltemplate,
                    settings.EMAIL_HOST_USER,
                    [ 'sadaf.shaikh@udaan.com', 'workmail052020@gmail.com', Onboarding_SPOC],
                ) 
                our_email.fail_silently = False
                our_email.send()
                messages.success(request, "Candidate Rejected Mail Sent To Admin.")
                return redirect("csp_app:pending_request")
            else:       
                
                selected_candidate.vendor_status = reject_vendor
                selected_candidate.loi_status = loi_status.objects.get(pk=3)
                selected_candidate.documentation_status = documentation_status.objects.get(pk=3)
                selected_candidate.offer_letter_status = offer_letter_status.objects.get(pk=3)
                selected_candidate.it_intimation_status = IT_intimation_status.objects.get(pk=3)
                selected_candidate.joining_status = joining_status.objects.get(pk=3)
                e = ecode_generation_status.objects.get(pk=3)
                selected_candidate.ecode_status = e.status_name
                selected_candidate.email_creation_status = email_creation_request_status.objects.get(pk=3)
                selected_candidate.laptop_status = laptop_request_status.objects.get(pk=3)
                selected_candidate.candidate_status = candidate_status.objects.get(pk=0)
                selected_candidate.save()
                alltemplate = render_to_string('emailtemplates/candidate_edited_by_vendor_admin_et.html', {'candidate_code':cid ,'user': request.user})
                our_email = EmailMessage(
                    'Candidate Rejected.',
                    alltemplate,
                    settings.EMAIL_HOST_USER,
                    [ 'sadaf.shaikh@udaan.com', 'workmail052020@gmail.com', Onboarding_SPOC],
                ) 
                our_email.fail_silently = False
                our_email.send()
                template = render_to_string('emailtemplates/candidate_edited_by_vendor_et.html', {'candidate_code':cid ,'user': request.user, 'vendor': selected_candidate.fk_vendor_code.vendor_name })
                our_email = EmailMessage(
                    'Candidate Rejected.',
                    template,
                    settings.EMAIL_HOST_USER,
                    [ 'sadaf.shaikh@udaan.com', selected_candidate.Onboarding_Spoc_Email_Id],
                ) 
                our_email.fail_silently = False
                our_email.send()
                
                messages.success(request, "Candidate Rejected Mail Sent To Admin.")
                return redirect("csp_app:pending_request")

    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Vendor').exists() or u.groups.filter(name='Onboarding SPOC').exists())
def pending_requests(request):   
    # count = 0 
    try:
        entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list = candidate_form_lists()

        for eachgroup in request.user.groups.all():
            if str(eachgroup) == 'Vendor':
                candidate_list = vendor_candidates(request.user)
                all_active_candidates = vendor_candidates(request.user)
                pending_candidate_list = vendor_pending_candidates(request.user)
                count = len(pending_candidate_list)
                delay_joiners = master_candidate.objects.filter(candidate_status=candidate_status.objects.get(pk=7))
                dojcount = len(delay_joiners)
            elif str(eachgroup) == 'Onboarding SPOC':
                candidate_list = onboarding_candidates(request.user)
                all_active_candidates = onboarding_candidates(request.user)
                pending_candidate_list = onboarding_pending_candidates(request.user)
                count = len(pending_candidate_list)
                delay_joiners = master_candidate.objects.filter(candidate_status=candidate_status.objects.get(pk=7))
                dojcount = len(delay_joiners)
            else:
                
                all_active_candidates = candidate_list = master_candidate.objects.filter(status=active_status)
                
                pending_candidate_list = master_candidate.objects.filter(onboarding_status= pending_onboarding,status=active_status ) 
                # | master_candidate.objects.filter(vendor_status= pending_vendor,status=active_status )
                count = len(pending_candidate_list)
                delay_joiners = master_candidate.objects.filter(candidate_status=candidate_status.objects.get(pk=7))
                dojcount = len(delay_joiners)
            
        return render(request, 'candidate/pendingrequests.html', {'dojcount':dojcount, 'count': count,'pending_candidate_list': pending_candidate_list, 'allcandidates': all_active_candidates,'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
        'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
        'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
        'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
        'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'candidate_list': candidate_list })
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Onboarding SPOC').exists())
def future_joining_requests(request):
    count = 0
    dojcount = 0
    all_active_candidates = master_candidate.objects.filter(status=active_status)
    candidate_list = master_candidate.objects.filter(status=active_status)
  
    for eachgroup in request.user.groups.all():
        if str(eachgroup) == 'Vendor':
            candidate_list = vendor_candidates(request.user)
            all_active_candidates = vendor_candidates(request.user)
            pending_candidate_list = vendor_pending_candidates(request.user)
            count = len(pending_candidate_list)
        elif str(eachgroup) == 'Onboarding SPOC':
            candidate_list = onboarding_candidates(request.user)
            all_active_candidates = onboarding_candidates(request.user)
            pending_candidate_list = onboarding_pending_candidates(request.user)
            count = len(pending_candidate_list)
            delay_joiners = master_candidate.objects.filter(candidate_status=candidate_status.objects.get(pk=7))
            dojcount = len(delay_joiners)
        else:
            delay_joiners = master_candidate.objects.filter(candidate_status=candidate_status.objects.get(pk=7))
            dojcount = len(delay_joiners)
            pending_candidate_list = master_candidate.objects.filter(onboarding_status= pending_onboarding,status=active_status ) 
            # | master_candidate.objects.filter(vendor_status= pending_vendor,status=active_status )
            count = len(pending_candidate_list)

    return render(request, 'candidate/futurejoiningrequest.html', {'dojcount': dojcount, 'future_requests': delay_joiners,'count': count})


@login_required(login_url='/notlogin/')
def candidate(request):
    
    count = 0
    dojcount = 0
    all_active_candidates = master_candidate.objects.filter(status=active_status)
    candidate_list = master_candidate.objects.filter(status=active_status)

    entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list = candidate_form_lists()
    c_status_list = candidate_status.objects.all()
    v_status_list = vendor_status.objects.all()
   
    for eachgroup in request.user.groups.all():
        if str(eachgroup) == 'Vendor':
            candidate_list = vendor_candidates(request.user)
            all_active_candidates = vendor_candidates(request.user)
            pending_candidate_list = vendor_pending_candidates(request.user)
            count = len(pending_candidate_list)
        elif str(eachgroup) == 'Onboarding SPOC':
            candidate_list = onboarding_candidates(request.user)
            all_active_candidates = onboarding_candidates(request.user)
            pending_candidate_list = onboarding_pending_candidates(request.user)
            count = len(pending_candidate_list)
            delay_joiners = master_candidate.objects.filter(candidate_status=candidate_status.objects.get(pk=7))
            dojcount = len(delay_joiners)
        else:
            delay_joiners = master_candidate.objects.filter(candidate_status=candidate_status.objects.get(pk=7))
            dojcount = len(delay_joiners)
            pending_candidate_list = master_candidate.objects.filter(onboarding_status= pending_onboarding,status=active_status ) 
            # | master_candidate.objects.filter(vendor_status= pending_vendor,status=active_status )
            count = len(pending_candidate_list)

    return render(request, 'candidate/candidates.html', {'dojcount':dojcount, 'count': count, 'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
    'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
    'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
    'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 'c_status_list': c_status_list,
    'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'candidate_list': candidate_list, 'v_status_list': v_status_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Recruiter').exists() or u.groups.filter(name='Onboarding SPOC').exists())
def new_candidate(request):    
    try:
        s_particulars = salary_structure_particulars.objects.all()
        e_particulars = employee_contributions_particulars.objects.all()
        er_particulars = employer_contributions_particulars.objects.all()
        entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list = candidate_form_lists()
        candidate_list = master_candidate.objects.all()
        minimum_wage = master_minimum_wages.objects.filter(status=active_status)
        return render(request, 'candidate/newcandidate.html', {'wages': minimum_wage, 's_particulars': s_particulars,'e_particulars': e_particulars,'er_particulars': er_particulars , 'allcandidates': all_active_candidates,'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
        'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
        'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
        'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
        'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'candidate_list': candidate_list })
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Vendor').exists() )
def view_edit_candidate(request): 
    try:
        if request.method == 'POST':
            candidate_id = request.POST.get("view_id")   
            entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list = candidate_form_lists()
            candidate_list = master_candidate.objects.filter(pk=candidate_id)
            
        return render(request, 'candidate/editcandidate.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'location_list': location_list, 
        'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
        'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
        'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
        'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'selected_candidate': candidate_list })
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Vendor').exists() or u.groups.filter(name='Onboarding SPOC').exists())
def edit_salary_structure_process(request, cid): 
    try:
        for eachgroup in request.user.groups.all():
            if str(eachgroup) == 'Vendor':
                candidate_list = vendor_candidates(request.user)
                all_active_candidates = vendor_candidates(request.user)
                pending_candidate_list = vendor_pending_candidates(request.user)
                count = len(pending_candidate_list)
            elif str(eachgroup) == 'Onboarding SPOC':
                candidate_list = onboarding_candidates(request.user)
                all_active_candidates = onboarding_candidates(request.user)
                pending_candidate_list = onboarding_pending_candidates(request.user)
                count = len(pending_candidate_list)
            else:
                
                all_active_candidates = candidate_list = master_candidate.objects.filter(status=active_status)
                
                pending_candidate_list = master_candidate.objects.filter(onboarding_status= pending_onboarding,status=active_status ) 
                # | master_candidate.objects.filter(vendor_status= pending_vendor,status=active_status )
                count = len(pending_candidate_list)
            if request.method == 'POST':
                candidate_id = request.POST.get("cid")   
                selected_candidate = master_candidate.objects.filter(pk=candidate_id)
                entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list = candidate_form_lists()
                candidate_list = master_candidate.objects.filter(pk=candidate_id)
                cid = request.POST.get('cid')
                firstname = request.POST.get("c_firstname").capitalize()
                middlename = request.POST.get("c_middlename").capitalize()
                lastname = request.POST.get("c_lastname").capitalize()
                dob = request.POST.get("c_dob")
                contact_no = request.POST.get("c_contact")
                emergency_no = request.POST.get("c_emergency")
                email = request.POST.get("c_email")
                c_gender = request.POST.get("c_gender")
                fathername = request.POST.get("c_fathername").capitalize()
                mothername = request.POST.get("c_mothername").capitalize()
                aadhaar = request.POST.get("c_aadhaar")
                Pan = request.POST.get("c_pan")
                hiring = request.POST.get("c_hiring_type")
                doj = request.POST.get("c_doj")        
                replacement = request.POST.get("c_replacement")
                    
                referral = request.POST.get("c_referral")
                    
                subsource = request.POST.get("c_sub_source")
                entity = request.POST.get("c_entity")
                vendor = request.POST.get("c_vendor")
                department = request.POST.get("c_dept")
                function = request.POST.get("c_function")
                team = request.POST.get("c_team")
                sub_team = request.POST.get("c_subteam")
                designation = request.POST.get("c_desg")
                region = request.POST.get("c_region")
                state = request.POST.get("c_state")
                city = request.POST.get("c_city")
                location = request.POST.get("c_location")

                ta_spoc = request.POST.get("c_ta_spoc") #check
                onboarding_spoc = Onboarding_SPOC #check
                reporting_manager = request.POST.get("c_reporting_manager")
                reporting_manager_email = request.POST.get("c_reporting_manager_email")
                email_creation = request.POST.get("c_email_creation")
                laptopallocation = request.POST.get("c_laptop_allocation")
                salarytype = request.POST.get("c_salary_type")
                gross_salary = request.POST.get("c_gross_salary")
                loc_code = request.POST.get("c_gross_salary")
                if hiring == None or hiring == '':
                    messages.warning(request, "Choose Hiring Type And Try Again")
                    return redirect("csp_app:candidate")
                hiring_fk = hiring_type.objects.get(pk= hiring)
                if sub_source == None or sub_source == '':
                    messages.warning(request, "Choose  Sub Source  And Try Again")
                    return redirect("csp_app:candidate")
                subsource_fk = sub_source.objects.get(pk= subsource)
                if c_gender == None or c_gender == '':
                    messages.warning(request, "Choose  Gender And Try Again")
                    return redirect("csp_app:candidate")
                gender_fk = gender.objects.get(pk= c_gender)
                if laptopallocation == None or laptopallocation == '':
                    messages.warning(request, "Choose  Laptop Allocation And Try Again")
                    return redirect("csp_app:candidate")
                la_fk = laptop_allocation.objects.get(pk= laptopallocation)
                if salarytype == None or salarytype == '':
                    messages.warning(request, "Choose  Salary Type And Try Again")
                    return redirect("csp_app:candidate")
                salarytype_fk = salary_type.objects.get(pk= salarytype)
                if entity == None or entity == '':
                    messages.warning(request, "Choose  Company  And Try Again")
                    return redirect("csp_app:candidate")
                entity_fk = master_entity.objects.get(pk= entity)
                if vendor == None or vendor == '':
                    messages.warning(request, "Choose  vendor  And Try Again")
                    return redirect("csp_app:candidate")
                vendor_fk = master_vendor.objects.get(pk= vendor)
                if department == None or department == '':
                    messages.warning(request, "Choose  Department  And Try Again")
                    return redirect("csp_app:candidate")
                department_fk = master_department.objects.get(pk= department)
                if function == None or function == '':
                    messages.warning(request, "Choose  Function  And Try Again")
                    return redirect("csp_app:candidate")
                function_fk = master_function.objects.get(pk= function)
                if team == None or team == '':
                    messages.warning(request, "Choose  Team  And Try Again")
                    return redirect("csp_app:candidate")
                team_fk = master_team.objects.get(pk= team)
                if sub_team == None or sub_team == '':
                    messages.warning(request, "Choose  Sub Team  And Try Again")
                    return redirect("csp_app:candidate")
                sub_team_fk = master_sub_team.objects.get(pk= sub_team)
                if designation == None or designation == '':
                    messages.warning(request, "Choose  Designation  And Try Again")
                    return redirect("csp_app:candidate")
                designation_fk = master_designation.objects.get(pk= designation)
                if region == None or region == '':
                    messages.warning(request, "Choose  Region  And Try Again")
                    return redirect("csp_app:candidate")
                region_fk = master_region.objects.get(pk= region)
                if state == None or state == '':
                    messages.warning(request, "Choose  State  And Try Again")
                    return redirect("csp_app:candidate")
                state_fk = master_state.objects.get(pk= state)
                if city == None or city == '':
                    messages.warning(request, "Choose  City  And Try Again")
                    return redirect("csp_app:candidate")
                city_fk = master_city.objects.get(pk= city)
                if location == None or location == '':
                    messages.warning(request, "Choose  Location  And Try Again")
                    return redirect("csp_app:candidate")
                location_fk = master_location.objects.get(pk= location)
                
                # ss_gross_salary, basic, annualbasic, house_rent_allowance, annualhouse_rent_allowance, statutory_bonus, annualstatutory_bonus, special_allowance, annualspecial_allowance, annualgross_salary, employee_pf, annualemployee_pf, employee_esic, annualemployer_esic, employee_total_contribution, annualemployee_total_contribution, employer_pf, annualemployer_pf, employer_pf_admin, annualemployer_pf_admin, employer_esic, group_personal_accident, annualgroup_personal_accident, group_mediclaim_insurance, annualgroup_mediclaim_insurance, employer_total_contribution, annualemployer_total_contribution, cost_to_company, annualcost_to_company, take_home_salary, annualtake_home_salary = salary_structure_post_values(request)
                
                try:                
                    dup_candidate_aadhaar = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Aadhaar_Number= aadhaar, status= active_status)
                    messages.error( request, "Aadhaar Number Already Exist")
                    return redirect("csp_app:candidate")
                except ObjectDoesNotExist:
                    pass
                try:
                    dup_candidate_pan = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(PAN_Number= Pan, status= active_status)
                    messages.error( request, "PAN  Already Exist")
                    return redirect("csp_app:candidate")
                except ObjectDoesNotExist:
                    pass
                try:
                    dup_candidate_contact = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Contact_Number= contact_no, status= active_status)
                    messages.error( request, "Contact Number Already Exist")
                    return redirect("csp_app:candidate")
                except ObjectDoesNotExist:
                    pass
                try:
                
                    dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                    messages.error( request, "Candidate Already Exist")
                    return redirect("csp_app:candidate")
                except ObjectDoesNotExist:
                    pass
                try:
                    dup_candidate_email = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Personal_Email_Id=email, status= active_status)
                    messages.error( request, "Candidate Email Already Exist")
                    return redirect("csp_app:candidate")
                except ObjectDoesNotExist:
                    pass
                try:
                    dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                    messages.error( request, "Same Candidate Exist with ID : " + dup_candidate_details.pk)
                    return redirect("csp_app:candidate")
                except ObjectDoesNotExist:
                    new_code = create_dummy(firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, email, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, ta_spoc, onboarding_spoc, la_fk, salarytype_fk, gross_salary, request)
                    dummy = dummy_candidate.objects.get(pk=new_code)
                    minimum_wage = ''
                                #monthly
                    try:
                        
                        minimum_wage = master_minimum_wages.objects.get(fk_skill_code = dummy.fk_designation_code.fk_skill_code.pk, fk_state_code= dummy.fk_state_code.state_name_id, status=active_status)
                        minimum_wage_list = master_minimum_wages.objects.filter(fk_state_code= dummy.fk_state_code.state_name_id, status=active_status)
                        
                        wage = minimum_wage.wages
                    except ObjectDoesNotExist:
                        wage = 0
                    gsa = dummy.Gross_Salary_Amount
                    state_name = dummy.fk_state_code.state_name
                    salary_pk = dummy.Salary_Type.pk
                    mwc = minimum_wage.wages
                    gsa_value = dummy.Gross_Salary_Amount
                    basic, hra, sb, sa, grossalary, annual_basic, annual_hra, annual_sb, annual_sa, annual_gs, annual_epf, annual_esic, annual_td, annual_ths, epf, esic, td, ths, erpf, erpf_admin, ersic, gpa, gmi, annual_eprf, annual_pfadmin, annual_ersic, annual_gpa, annual_gmi, tec, annual_tec, ctc, annual_ctc, var, annual_var, diff, gpi_2, fs, annual_fs = salary_structure_calculation(gsa, wage, state_name, salary_pk)
                    selected_candidate, ss_gross_salary = update_selected_dummy(dummy.pk_candidate_code, firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, onboarding_spoc, la_fk, salarytype_fk, request, email, gross_salary)
                    delay_joiners = master_candidate.objects.filter(candidate_status=candidate_status.objects.get(pk=7))
                    dojcount = len(delay_joiners)
                    return render(request, 'candidate/processeditsalarystructure.html', {'dojcount':dojcount, 'count': count, 'cid':candidate_id, 'mwc':convert_to_INR(mwc), 'gsa':convert_to_INR(gsa_value), 'eachcandidate': selected_candidate, 'dummy': dummy, 'basic': convert_to_INR(basic), 'hra': convert_to_INR(hra), 'sb': convert_to_INR(sb), 'sa': convert_to_INR(sa), 'gross_salary': convert_to_INR(grossalary), 'annualbasic': convert_to_INR(annual_basic), 'annualhra': convert_to_INR(annual_hra), 
                    'annualsb': convert_to_INR(annual_sb), 'annualsa': convert_to_INR(annual_sa), 'annualgs': convert_to_INR(annual_gs), 'annualepf': convert_to_INR(annual_epf), 'annualesic': convert_to_INR(annual_esic), 'annualtd': convert_to_INR(annual_td),
                    'annualths': convert_to_INR(annual_ths), 'epf': convert_to_INR(epf), 'esic': convert_to_INR(esic), 'td': convert_to_INR(td), 'ths': convert_to_INR(ths), 'erpf': convert_to_INR(erpf), 'erpf_admin': convert_to_INR(erpf_admin), 'ersic': convert_to_INR(ersic), 'gpa': convert_to_INR(gpa), 'gmi': convert_to_INR(gmi),
                    'annualerpf': convert_to_INR(annual_eprf), 'annualerpf_admin': convert_to_INR(annual_pfadmin), 'annualersic': convert_to_INR(annual_ersic), 'annualgpa': convert_to_INR(annual_gpa), 'annualgmi': convert_to_INR(annual_gmi), 'tec': convert_to_INR(tec), 'annual_tec': convert_to_INR(annual_tec), 'ctc': convert_to_INR(ctc), 'annual_ctc': convert_to_INR(annual_ctc),
                    'allcandidates': all_active_candidates,'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
                    'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
                    'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
                    'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
                    'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list,'variable': convert_to_INR(var), 'annual_var': convert_to_INR(annual_var), 'minimum_wage': minimum_wage, 'minimum_wage_list':minimum_wage_list, 'difference': convert_to_INR(diff), 'gpac': convert_to_INR(gpi_2), 'fs': convert_to_INR(fs), 'annual_fs': convert_to_INR(annual_fs)})

    
        # if request.method == 'POST':
        #     candidate_id = cid  
        #     print(candidate_id)
        #     selected_candidate = master_candidate.objects.filter(pk=candidate_id)
        #     entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list = candidate_form_lists()
        #     candidate_list = master_candidate.objects.filter(pk=candidate_id)
           
        #     cid = request.POST.get('c_id')
        #     firstname = request.POST.get("c_firstname").capitalize()
        #     middlename = request.POST.get("c_middlename").capitalize()
         
        #     lastname = request.POST.get("c_lastname").capitalize()
        #     dob = request.POST.get("c_dob")
        #     contact_no = request.POST.get("c_contact")
        #     emergency_no = request.POST.get("c_emergency")
        #     email = request.POST.get("c_email")
        #     c_gender = request.POST.get("c_gender")
        #     fathername = request.POST.get("c_fathername")
        #     mothername = request.POST.get("c_mothername").capitalize()
        #     aadhaar = request.POST.get("c_aadhaar")
        #     Pan = request.POST.get("c_pan")
        #     hiring = request.POST.get("c_hiring_type")
        #     doj = request.POST.get("c_doj")        
        #     replacement = request.POST.get("c_replacement")
                
        #     referral = request.POST.get("c_referral")
                
        #     subsource = request.POST.get("c_sub_source")
        #     entity = request.POST.get("c_entity")
        #     vendor = request.POST.get("c_vendor")
        #     department = request.POST.get("c_dept")
        #     function = request.POST.get("c_function")
        #     team = request.POST.get("c_team")
        #     sub_team = request.POST.get("c_subteam")
        #     designation = request.POST.get("c_desg")
        #     region = request.POST.get("c_region")
        #     state = request.POST.get("c_state")
        #     city = request.POST.get("c_city")
        #     location = request.POST.get("c_location")

        #     ta_spoc = request.POST.get("c_ta_spoc") #check
        #     onboarding_spoc = 'workmail052020@gmail.com' #check
        #     reporting_manager = request.POST.get("c_reporting_manager")
        #     reporting_manager_email = request.POST.get("c_reporting_manager_email")
        #     email_creation = request.POST.get("c_email_creation")
        #     laptopallocation = request.POST.get("c_laptop_allocation")
        #     salarytype = request.POST.get("c_salary_type")
        #     gross_salary = request.POST.get("c_gross_salary")
        #     loc_code = request.POST.get("c_gross_salary")
        #     if hiring == None or hiring == '':
        #         messages.warning(request, "Choose Hiring Type And Try Again")
        #         return redirect("csp_app:candidate")
        #     hiring_fk = hiring_type.objects.get(pk= hiring)
        #     if sub_source == None or sub_source == '':
        #         messages.warning(request, "Choose  Sub Source  And Try Again")
        #         return redirect("csp_app:candidate")
        #     subsource_fk = sub_source.objects.get(pk= subsource)
        #     if c_gender == None or c_gender == '':
        #         messages.warning(request, "Choose  Gender And Try Again")
        #         return redirect("csp_app:candidate")
        #     gender_fk = gender.objects.get(pk= c_gender)
        #     if laptopallocation == None or laptopallocation == '':
        #         messages.warning(request, "Choose  Laptop Allocation And Try Again")
        #         return redirect("csp_app:candidate")
        #     la_fk = laptop_allocation.objects.get(pk= laptopallocation)
        #     if salarytype == None or salarytype == '':
        #         messages.warning(request, "Choose  Salary Type And Try Again")
        #         return redirect("csp_app:candidate")
        #     salarytype_fk = salary_type.objects.get(pk= salarytype)
        #     if entity == None or entity == '':
        #         messages.warning(request, "Choose  Company  And Try Again")
        #         return redirect("csp_app:candidate")
        #     entity_fk = master_entity.objects.get(pk= entity)
        #     if vendor == None or vendor == '':
        #         messages.warning(request, "Choose  vendor  And Try Again")
        #         return redirect("csp_app:candidate")
        #     vendor_fk = master_vendor.objects.get(pk= vendor)
        #     if department == None or department == '':
        #         messages.warning(request, "Choose  Department  And Try Again")
        #         return redirect("csp_app:candidate")
        #     department_fk = master_department.objects.get(pk= department)
        #     if function == None or function == '':
        #         messages.warning(request, "Choose  Function  And Try Again")
        #         return redirect("csp_app:candidate")
        #     function_fk = master_function.objects.get(pk= function)
        #     if team == None or team == '':
        #         messages.warning(request, "Choose  Team  And Try Again")
        #         return redirect("csp_app:candidate")
        #     team_fk = master_team.objects.get(pk= team)
        #     if sub_team == None or sub_team == '':
        #         messages.warning(request, "Choose  Sub Team  And Try Again")
        #         return redirect("csp_app:candidate")
        #     sub_team_fk = master_sub_team.objects.get(pk= sub_team)
        #     if designation == None or designation == '':
        #         messages.warning(request, "Choose  Designation  And Try Again")
        #         return redirect("csp_app:candidate")
        #     designation_fk = master_designation.objects.get(pk= designation)
        #     if region == None or region == '':
        #         messages.warning(request, "Choose  Region  And Try Again")
        #         return redirect("csp_app:candidate")
        #     region_fk = master_region.objects.get(pk= region)
        #     if state == None or state == '':
        #         messages.warning(request, "Choose  State  And Try Again")
        #         return redirect("csp_app:candidate")
        #     state_fk = master_state.objects.get(pk= state)
        #     if city == None or city == '':
        #         messages.warning(request, "Choose  City  And Try Again")
        #         return redirect("csp_app:candidate")
        #     city_fk = master_city.objects.get(pk= city)
        #     if location == None or location == '':
        #         messages.warning(request, "Choose  Location  And Try Again")
        #         return redirect("csp_app:candidate")
        #     location_fk = master_location.objects.get(pk= location)
            
        #     # ss_gross_salary, basic, annualbasic, house_rent_allowance, annualhouse_rent_allowance, statutory_bonus, annualstatutory_bonus, special_allowance, annualspecial_allowance, annualgross_salary, employee_pf, annualemployee_pf, employee_esic, annualemployer_esic, employee_total_contribution, annualemployee_total_contribution, employer_pf, annualemployer_pf, employer_pf_admin, annualemployer_pf_admin, employer_esic, group_personal_accident, annualgroup_personal_accident, group_mediclaim_insurance, annualgroup_mediclaim_insurance, employer_total_contribution, annualemployer_total_contribution, cost_to_company, annualcost_to_company, take_home_salary, annualtake_home_salary = salary_structure_post_values(request)
            
        #     try:                
        #         dup_candidate_aadhaar = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Aadhaar_Number= aadhaar, status= active_status)
        #         messages.error( request, "Aadhaar Number Already Exist")
        #         return redirect("csp_app:candidate")
        #     except ObjectDoesNotExist:
        #         pass
        #     try:
        #         dup_candidate_pan = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(PAN_Number= Pan, status= active_status)
        #         messages.error( request, "PAN  Already Exist")
        #         return redirect("csp_app:candidate")
        #     except ObjectDoesNotExist:
        #         pass
        #     try:
        #         dup_candidate_contact = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Contact_Number= contact_no, status= active_status)
        #         messages.error( request, "Contact Number Already Exist")
        #         return redirect("csp_app:candidate")
        #     except ObjectDoesNotExist:
        #         pass
        #     try:
            
        #         dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
        #         messages.error( request, "Candidate Already Exist")
        #         return redirect("csp_app:candidate")
        #     except ObjectDoesNotExist:
        #         pass
        #     try:
        #         dup_candidate_email = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Personal_Email_Id=email, status= active_status)
        #         messages.error( request, "Candidate Email Already Exist")
        #         return redirect("csp_app:candidate")
        #     except ObjectDoesNotExist:
        #         pass
        #     try:
        #         dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
        #         messages.error( request, "Same Candidate Exist with ID : " + dup_candidate_details.pk)
        #         return redirect("csp_app:candidate")
        #     except ObjectDoesNotExist:
        #         new_code = create_dummy(firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, email, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, ta_spoc, onboarding_spoc, la_fk, salarytype_fk, gross_salary, request)
        #         dummy = dummy_candidate.objects.get(pk=new_code)
        #         minimum_wage = ''
        #                     #monthly
        #         try:
                    
        #             minimum_wage = master_minimum_wages.objects.get(fk_skill_code = dummy.fk_designation_code.fk_skill_code.pk, fk_state_code= dummy.fk_state_code.state_name_id, status=active_status)
        #             minimum_wage_list = master_minimum_wages.objects.filter(fk_state_code= dummy.fk_state_code.state_name_id, status=active_status)
                    
        #             wage = minimum_wage.wages
        #         except ObjectDoesNotExist:
        #             wage = 0
        #         gsa = dummy.Gross_Salary_Amount
        #         state_name = dummy.fk_state_code.state_name
        #         salary_pk = dummy.Salary_Type.pk
        #         mwc = minimum_wage.wages
        #         gsa_value = dummy.Gross_Salary_Amount
        #         basic, hra, sb, sa, grossalary, annual_basic, annual_hra, annual_sb, annual_sa, annual_gs, annual_epf, annual_esic, annual_td, annual_ths, epf, esic, td, ths, erpf, erpf_admin, ersic, gpa, gmi, annual_eprf, annual_pfadmin, annual_ersic, annual_gpa, annual_gmi, tec, annual_tec, ctc, annual_ctc, var, annual_var, diff, gpi_2, fs, annual_fs = salary_structure_calculation(gsa, wage, state_name, salary_pk)
        #         # selected_candidate, ss_gross_salary = update_selected_dummy(dummy.pk_candidate_code, firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, onboarding_spoc, la_fk, salarytype_fk, request, email, gross_salary)
                
        #         return render(request, 'candidate/processeditsalarystructure.html', {'cid':candidate_id,'count':count, 'mwc':convert_to_INR(mwc), 'gsa':convert_to_INR(gsa_value), 'selected_candidate': selected_candidate, 'dummy': dummy, 'basic': convert_to_INR(basic), 'hra': convert_to_INR(hra), 'sb': convert_to_INR(sb), 'sa': convert_to_INR(sa), 'gross_salary': convert_to_INR(grossalary), 'annualbasic': convert_to_INR(annual_basic), 'annualhra': convert_to_INR(annual_hra), 
        #         'annualsb': convert_to_INR(annual_sb), 'annualsa': convert_to_INR(annual_sa), 'annualgs': convert_to_INR(annual_gs), 'annualepf': convert_to_INR(annual_epf), 'annualesic': convert_to_INR(annual_esic), 'annualtd': convert_to_INR(annual_td),
        #         'annualths': convert_to_INR(annual_ths), 'epf': convert_to_INR(epf), 'esic': convert_to_INR(esic), 'td': convert_to_INR(td), 'ths': convert_to_INR(ths), 'erpf': convert_to_INR(erpf), 'erpf_admin': convert_to_INR(erpf_admin), 'ersic': convert_to_INR(ersic), 'gpa': convert_to_INR(gpa), 'gmi': convert_to_INR(gmi),
        #         'annualerpf': convert_to_INR(annual_eprf), 'annualerpf_admin': convert_to_INR(annual_pfadmin), 'annualersic': convert_to_INR(annual_ersic), 'annualgpa': convert_to_INR(annual_gpa), 'annualgmi': convert_to_INR(annual_gmi), 'tec': convert_to_INR(tec), 'annual_tec': convert_to_INR(annual_tec), 'ctc': convert_to_INR(ctc), 'annual_ctc': convert_to_INR(annual_ctc),
        #         'allcandidates': all_active_candidates,'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
        #         'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
        #         'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
        #         'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
        #         'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list,'variable': convert_to_INR(var), 'annual_var': convert_to_INR(annual_var), 'minimum_wage': minimum_wage, 'minimum_wage_list':minimum_wage_list, 'difference': convert_to_INR(diff), 'gpac': convert_to_INR(gpi_2), 'fs': convert_to_INR(fs), 'annual_fs': convert_to_INR(annual_fs)})

                 
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def edit_salary_structure(request): 
    
    try:
        if request.method == 'POST':
            candidate_id = request.POST.get("c_id")   
            selected_candidate = master_candidate.objects.filter(pk=candidate_id)
            entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list = candidate_form_lists()
            candidate_list = master_candidate.objects.filter(pk=candidate_id)
            cid = request.POST.get('c_id')
            firstname = request.POST.get("c_firstname").capitalize()
            middlename = request.POST.get("c_middlename").capitalize()
            lastname = request.POST.get("c_lastname").capitalize()
            dob = request.POST.get("c_dob")
            contact_no = request.POST.get("c_contact")
            emergency_no = request.POST.get("c_emergency")
            email = request.POST.get("c_email")
            c_gender = request.POST.get("c_gender")
            fathername = request.POST.get("c_fathername").capitalize()
            mothername = request.POST.get("c_mothername").capitalize()
            aadhaar = request.POST.get("c_aadhaar")
            Pan = request.POST.get("c_pan")
            hiring = request.POST.get("c_hiring_type")
            doj = request.POST.get("c_doj")        
            replacement = request.POST.get("c_replacement")
                
            referral = request.POST.get("c_referral")
                
            subsource = request.POST.get("c_sub_source")
            entity = request.POST.get("c_entity")
            vendor = request.POST.get("c_vendor")
            department = request.POST.get("c_dept")
            function = request.POST.get("c_function")
            team = request.POST.get("c_team")
            sub_team = request.POST.get("c_subteam")
            designation = request.POST.get("c_desg")
            region = request.POST.get("c_region")
            state = request.POST.get("c_state")
            city = request.POST.get("c_city")
            location = request.POST.get("c_location")

            ta_spoc = request.POST.get("c_ta_spoc") #check
            onboarding_spoc = Onboarding_SPOC #check
            reporting_manager = request.POST.get("c_reporting_manager")
            reporting_manager_email = request.POST.get("c_reporting_manager_email")
            email_creation = request.POST.get("c_email_creation")
            laptopallocation = request.POST.get("c_laptop_allocation")
            salarytype = request.POST.get("c_salary_type")
            gross_salary = request.POST.get("c_gross_salary")
            loc_code = request.POST.get("c_gross_salary")
            if hiring == None or hiring == '':
                messages.warning(request, "Choose Hiring Type And Try Again")
                return redirect("csp_app:candidate")
            hiring_fk = hiring_type.objects.get(pk= hiring)
            if sub_source == None or sub_source == '':
                messages.warning(request, "Choose  Sub Source  And Try Again")
                return redirect("csp_app:candidate")
            subsource_fk = sub_source.objects.get(pk= subsource)
            if c_gender == None or c_gender == '':
                messages.warning(request, "Choose  Gender And Try Again")
                return redirect("csp_app:candidate")
            gender_fk = gender.objects.get(pk= c_gender)
            if laptopallocation == None or laptopallocation == '':
                messages.warning(request, "Choose  Laptop Allocation And Try Again")
                return redirect("csp_app:candidate")
            la_fk = laptop_allocation.objects.get(pk= laptopallocation)
            if salarytype == None or salarytype == '':
                messages.warning(request, "Choose  Salary Type And Try Again")
                return redirect("csp_app:candidate")
            salarytype_fk = salary_type.objects.get(pk= salarytype)
            if entity == None or entity == '':
                messages.warning(request, "Choose  Company  And Try Again")
                return redirect("csp_app:candidate")
            entity_fk = master_entity.objects.get(pk= entity)
            if vendor == None or vendor == '':
                messages.warning(request, "Choose  vendor  And Try Again")
                return redirect("csp_app:candidate")
            vendor_fk = master_vendor.objects.get(pk= vendor)
            if department == None or department == '':
                messages.warning(request, "Choose  Department  And Try Again")
                return redirect("csp_app:candidate")
            department_fk = master_department.objects.get(pk= department)
            if function == None or function == '':
                messages.warning(request, "Choose  Function  And Try Again")
                return redirect("csp_app:candidate")
            function_fk = master_function.objects.get(pk= function)
            if team == None or team == '':
                messages.warning(request, "Choose  Team  And Try Again")
                return redirect("csp_app:candidate")
            team_fk = master_team.objects.get(pk= team)
            if sub_team == None or sub_team == '':
                messages.warning(request, "Choose  Sub Team  And Try Again")
                return redirect("csp_app:candidate")
            sub_team_fk = master_sub_team.objects.get(pk= sub_team)
            if designation == None or designation == '':
                messages.warning(request, "Choose  Designation  And Try Again")
                return redirect("csp_app:candidate")
            designation_fk = master_designation.objects.get(pk= designation)
            if region == None or region == '':
                messages.warning(request, "Choose  Region  And Try Again")
                return redirect("csp_app:candidate")
            region_fk = master_region.objects.get(pk= region)
            if state == None or state == '':
                messages.warning(request, "Choose  State  And Try Again")
                return redirect("csp_app:candidate")
            state_fk = master_state.objects.get(pk= state)
            if city == None or city == '':
                messages.warning(request, "Choose  City  And Try Again")
                return redirect("csp_app:candidate")
            city_fk = master_city.objects.get(pk= city)
            if location == None or location == '':
                messages.warning(request, "Choose  Location  And Try Again")
                return redirect("csp_app:candidate")
            location_fk = master_location.objects.get(pk= location)
            
            # ss_gross_salary, basic, annualbasic, house_rent_allowance, annualhouse_rent_allowance, statutory_bonus, annualstatutory_bonus, special_allowance, annualspecial_allowance, annualgross_salary, employee_pf, annualemployee_pf, employee_esic, annualemployer_esic, employee_total_contribution, annualemployee_total_contribution, employer_pf, annualemployer_pf, employer_pf_admin, annualemployer_pf_admin, employer_esic, group_personal_accident, annualgroup_personal_accident, group_mediclaim_insurance, annualgroup_mediclaim_insurance, employer_total_contribution, annualemployer_total_contribution, cost_to_company, annualcost_to_company, take_home_salary, annualtake_home_salary = salary_structure_post_values(request)
            
            try:                
                dup_candidate_aadhaar = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Aadhaar_Number= aadhaar, status= active_status)
                messages.error( request, "Aadhaar Number Already Exist")
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_pan = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(PAN_Number= Pan, status= active_status)
                messages.error( request, "PAN  Already Exist")
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_contact = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Contact_Number= contact_no, status= active_status)
                messages.error( request, "Contact Number Already Exist")
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                pass
            try:
            
                dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                messages.error( request, "Candidate Already Exist")
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_email = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Personal_Email_Id=email, status= active_status)
                messages.error( request, "Candidate Email Already Exist")
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                messages.error( request, "Same Candidate Exist with ID : " + dup_candidate_details.pk)
                return redirect("csp_app:candidate")
            except ObjectDoesNotExist:
                new_code = create_dummy(firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, email, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, ta_spoc, onboarding_spoc, la_fk, salarytype_fk, gross_salary, request)
                dummy = dummy_candidate.objects.get(pk=new_code)
                minimum_wage = ''
                            #monthly
                try:
                    
                    minimum_wage = master_minimum_wages.objects.get(fk_skill_code = dummy.fk_designation_code.fk_skill_code.pk, fk_state_code= dummy.fk_state_code.state_name_id, status=active_status)
                    minimum_wage_list = master_minimum_wages.objects.filter(fk_state_code= dummy.fk_state_code.state_name_id, status=active_status)
                    
                    wage = minimum_wage.wages
                except ObjectDoesNotExist:
                    wage = 0
                gsa = dummy.Gross_Salary_Amount
                state_name = dummy.fk_state_code.state_name
                salary_pk = dummy.Salary_Type.pk
                mwc = minimum_wage.wages
                gsa_value = dummy.Gross_Salary_Amount
                basic, hra, sb, sa, grossalary, annual_basic, annual_hra, annual_sb, annual_sa, annual_gs, annual_epf, annual_esic, annual_td, annual_ths, epf, esic, td, ths, erpf, erpf_admin, ersic, gpa, gmi, annual_eprf, annual_pfadmin, annual_ersic, annual_gpa, annual_gmi, tec, annual_tec, ctc, annual_ctc, var, annual_var, diff, gpi_2, fs, annual_fs = salary_structure_calculation(gsa, wage, state_name, salary_pk)
                selected_candidate, ss_gross_salary = update_selected_dummy(dummy.pk_candidate_code, firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, onboarding_spoc, la_fk, salarytype_fk, request, email, gross_salary)

                return render(request, 'candidate/editsalarystructure.html', {'cid':candidate_id, 'mwc':convert_to_INR(mwc), 'gsa':convert_to_INR(gsa_value), 'eachc': selected_candidate, 'dummy': dummy, 'basic': convert_to_INR(basic), 'hra': convert_to_INR(hra), 'sb': convert_to_INR(sb), 'sa': convert_to_INR(sa), 'gross_salary': convert_to_INR(grossalary), 'annualbasic': convert_to_INR(annual_basic), 'annualhra': convert_to_INR(annual_hra), 
                'annualsb': convert_to_INR(annual_sb), 'annualsa': convert_to_INR(annual_sa), 'annualgs': convert_to_INR(annual_gs), 'annualepf': convert_to_INR(annual_epf), 'annualesic': convert_to_INR(annual_esic), 'annualtd': convert_to_INR(annual_td),
                'annualths': convert_to_INR(annual_ths), 'epf': convert_to_INR(epf), 'esic': convert_to_INR(esic), 'td': convert_to_INR(td), 'ths': convert_to_INR(ths), 'erpf': convert_to_INR(erpf), 'erpf_admin': convert_to_INR(erpf_admin), 'ersic': convert_to_INR(ersic), 'gpa': convert_to_INR(gpa), 'gmi': convert_to_INR(gmi),
                'annualerpf': convert_to_INR(annual_eprf), 'annualerpf_admin': convert_to_INR(annual_pfadmin), 'annualersic': convert_to_INR(annual_ersic), 'annualgpa': convert_to_INR(annual_gpa), 'annualgmi': convert_to_INR(annual_gmi), 'tec': convert_to_INR(tec), 'annual_tec': convert_to_INR(annual_tec), 'ctc': convert_to_INR(ctc), 'annual_ctc': convert_to_INR(annual_ctc),
                'allcandidates': all_active_candidates,'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
                'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
                'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
                'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
                'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list,'variable': convert_to_INR(var), 'annual_var': convert_to_INR(annual_var), 'minimum_wage': minimum_wage, 'minimum_wage_list':minimum_wage_list, 'difference': convert_to_INR(diff), 'gpac': convert_to_INR(gpi_2), 'fs': convert_to_INR(fs), 'annual_fs': convert_to_INR(annual_fs)})

                    # selected_candidate = ''
                    # selected_candidate, ss_gross_salary = update_selected_candidate(cid, firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, onboarding_spoc, la_fk, salarytype_fk, request, email)
                    # candidate_id = selected_candidate.pk
                    # candidate_id = ''
                    # new_salary_structure = salary_structure(candidate_code= candidate_id, basic= INR_to_number(basic), annual_basic= INR_to_number(annualbasic), house_rent_allowance= INR_to_number(hra), annual_house_rent_allowance= INR_to_number(annual_hra), statutory_bonus=INR_to_number(sb), annual_statutory_bonus= INR_to_number(annual_sb),
                    #     special_allowance=INR_to_number(sa), annual_special_allowance=INR_to_number(annual_sa),gross_salary=INR_to_number(grossalary), annual_gross_salary=INR_to_number(annual_gs), employee_pf= INR_to_number(epf), annual_employee_pf= INR_to_number(annual_epf),
                    #     employee_esic= INR_to_number(employee_esic), annual_employee_esic= INR_to_number(annualemployer_esic), employee_total_contribution= INR_to_number(employee_total_contribution), annual_employee_total_contribution= INR_to_number(annualemployee_total_contribution), employer_pf= INR_to_number(employer_pf), annual_employer_pf= INR_to_number(annualemployer_pf),
                    #     employer_pf_admin=INR_to_number(employer_pf_admin), annual_employer_pf_admin= INR_to_number(annualemployer_pf_admin), employer_esic= INR_to_number(employer_esic), annual_employer_esic= INR_to_number(annualemployer_esic), group_personal_accident= INR_to_number(group_personal_accident), annual_group_personal_accident= INR_to_number(annualgroup_personal_accident),
                    #     group_mediclaim_insurance= INR_to_number(group_mediclaim_insurance), annual_group_mediclaim_insurance = INR_to_number(annualgroup_mediclaim_insurance), employer_total_contribution= INR_to_number(employer_total_contribution), annual_employer_total_contribution= INR_to_number(annualemployer_total_contribution), cost_to_company=INR_to_number(cost_to_company),
                    #     annual_cost_to_company= INR_to_number(annualcost_to_company), take_home_salary= INR_to_number(take_home_salary), annual_take_home_salary= INR_to_number(annualtake_home_salary))
                    # new_salary_structure.save()
                    # alltemplate = render_to_string('emailtemplates/candidate_edited_et.html', {'candidate_code':cid ,'user': request.user})
                    # our_email = EmailMessage(
                    #     'Candidate Account Updated.',
                    #     alltemplate,
                    #     settings.EMAIL_HOST_USER,
                    #     [ selected_candidate.TA_Spoc_Email_Id, onboarding_spoc, 'sadaf.shaikh@udaan.com'],
                    # ) 
                    # our_email.fail_silently = False
                    # our_email.send()
                    # limtemplate = render_to_string('emailtemplates/candidate_edited_et_limited.html', {'candidate_code':cid ,'user': request.user})
                    # our_email = EmailMessage(
                    #     'Candidate Account Updated.',
                    #     limtemplate,
                    #     settings.EMAIL_HOST_USER,
                    #     [ reporting_manager_email, 'sadaf.shaikh@udaan.com'],
                    # ) 
                    # our_email.fail_silently = False
                    # our_email.send()
                    
                    # messages.success(request, "Candidate Updated Successfully")
                    # return redirect("csp_app:candidate")
    
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

def update_selected_dummy(cid, firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, onboarding_spoc, la_fk, salarytype_fk, request, email, gs):
    
    selected_candidate = dummy_candidate.objects.get(pk = cid)
    selected_candidate.First_Name=firstname
    selected_candidate.Middle_Name=middlename
    selected_candidate.Last_Name= lastname
    selected_candidate.Date_of_Joining= doj
    selected_candidate.Date_of_Birth= dob
    selected_candidate.Father_Name= fathername
    selected_candidate.Mother_Name= mothername
    selected_candidate.Aadhaar_Number= aadhaar
    selected_candidate.PAN_Number= Pan
    selected_candidate.Contact_Number= contact_no
    selected_candidate.Emergency_Contact_Number= emergency_no
    selected_candidate.Type_of_Hiring= hiring_fk
    selected_candidate.Replacement= replacement
    selected_candidate.Sub_Source= subsource_fk
    selected_candidate.Referral= referral
    selected_candidate.fk_vendor_code= vendor_fk
    selected_candidate.fk_entity_code= entity_fk
    selected_candidate.fk_department_code= department_fk
    selected_candidate.fk_function_code= function_fk
    selected_candidate.fk_team_code= team_fk
    selected_candidate.fk_subteam_code= sub_team_fk
    selected_candidate.fk_designation_code= designation_fk
    selected_candidate.fk_region_code= region_fk
    selected_candidate.fk_state_code= state_fk
    selected_candidate.fk_city_code= city_fk
    selected_candidate.fk_location_code= location_fk
    
    selected_candidate.Gross_Salary_Entered= loc_code
    selected_candidate.Reporting_Manager= reporting_manager
    selected_candidate.Reporting_Manager_E_Mail_ID= reporting_manager_email
    selected_candidate.Gender= gender_fk 
    selected_candidate.E_Mail_ID_Creation= email_creation
    selected_candidate.Onboarding_Spoc_Email_Id= onboarding_spoc
    selected_candidate.Laptop_Allocation= la_fk
    selected_candidate.Salary_Type= salarytype_fk
    ss_gross_salary = gs
    if ss_gross_salary == None:
        ss_gross_salary = request.POST.get('gsv')
    
    selected_candidate.Gross_Salary_Amount= float(ss_gross_salary)
    
    selected_candidate.Personal_Email_Id = email
    selected_candidate.modified_by = str(request.user)
    selected_candidate.modified_date_time= datetime.now()
    selected_candidate.save()
    return selected_candidate, ss_gross_salary



def update_selected_candidate(cid, firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, onboarding_spoc, la_fk, salarytype_fk, request, email, gs):
    selected_candidate = master_candidate.objects.get(pk = cid)
    selected_candidate.First_Name=firstname
    selected_candidate.Middle_Name=middlename
    selected_candidate.Last_Name= lastname
    selected_candidate.Date_of_Joining= doj
    selected_candidate.Date_of_Birth= dob
    selected_candidate.Father_Name= fathername
    selected_candidate.Mother_Name= mothername
    selected_candidate.Aadhaar_Number= aadhaar
    selected_candidate.PAN_Number= Pan
    selected_candidate.Contact_Number= contact_no
    selected_candidate.Emergency_Contact_Number= emergency_no
    selected_candidate.Type_of_Hiring= hiring_fk
    selected_candidate.Replacement= replacement
    selected_candidate.Sub_Source= subsource_fk
    selected_candidate.Referral= referral
    selected_candidate.fk_vendor_code= vendor_fk
    selected_candidate.fk_entity_code= entity_fk
    selected_candidate.fk_department_code= department_fk
    selected_candidate.fk_function_code= function_fk
    selected_candidate.fk_team_code= team_fk
    selected_candidate.fk_subteam_code= sub_team_fk
    selected_candidate.fk_designation_code= designation_fk
    selected_candidate.fk_region_code= region_fk
    selected_candidate.fk_state_code= state_fk
    selected_candidate.fk_city_code= city_fk
    selected_candidate.fk_location_code= location_fk
    
    selected_candidate.Gross_Salary_Entered= loc_code
    selected_candidate.Reporting_Manager= reporting_manager
    selected_candidate.Reporting_Manager_E_Mail_ID= reporting_manager_email
    selected_candidate.Gender= gender_fk 
    selected_candidate.E_Mail_ID_Creation= email_creation
    selected_candidate.Onboarding_Spoc_Email_Id= onboarding_spoc
    selected_candidate.Laptop_Allocation= la_fk
    selected_candidate.Salary_Type= salarytype_fk
    ss_gross_salary = gs
    if ss_gross_salary == None:
        ss_gross_salary = request.POST.get('gsv')
    selected_candidate.Gross_Salary_Amount= INR_to_number(ss_gross_salary)
    selected_candidate.Personal_Email_Id = email
    selected_candidate.modified_by = str(request.user)
    selected_candidate.modified_date_time= datetime.now()
    selected_candidate.save()
    return selected_candidate, ss_gross_salary

def salary_structure_post_values(request):
    basic = request.POST.get("basic")
    if basic == None:
        basic = 0
    annualbasic = request.POST.get("annualbasic")
    if annualbasic == None:
        annualbasic = 0
    house_rent_allowance = request.POST.get("hra")
    if house_rent_allowance == None:
        house_rent_allowance = 0
    annualhouse_rent_allowance = request.POST.get("annualhra")
    if annualhouse_rent_allowance == None:
        annualhouse_rent_allowance = 0
    statutory_bonus = request.POST.get("sb")
    if statutory_bonus == None:
        statutory_bonus = 0
    annualstatutory_bonus = request.POST.get("annualsb")
    if annualstatutory_bonus == None:
        annualstatutory_bonus = 0
    special_allowance = request.POST.get("sa")
    if special_allowance == None:
        special_allowance = 0
    annualspecial_allowance = request.POST.get("annualsa")
    if annualspecial_allowance == None:
        annualspecial_allowance = 0
    ss_gross_salary = request.POST.get("gs")
    if ss_gross_salary == None:
        ss_gross_salary = 0
    annualgross_salary = request.POST.get("annualgs")
    if annualgross_salary == None:
        annualgross_salary = 0
    employee_pf = request.POST.get("epf")
    if employee_pf == None:
        employee_pf = 0
    annualemployee_pf = request.POST.get("annualepf")
    if annualemployee_pf == None:
        annualemployee_pf = 0
    employee_esic = request.POST.get("esic")
    if employee_esic == None:
        employee_esic = 0
    annualemployee_esic = request.POST.get("annualesic")
    if annualemployee_esic == None:
        annualemployee_esic = 0
    employee_total_contribution = request.POST.get("tc")
    if employee_total_contribution == None:
        employee_total_contribution = 0
    annualemployee_total_contribution = request.POST.get("annualtc")
    if annualemployee_total_contribution == None:
        annualemployee_total_contribution = 0
    employer_pf = request.POST.get("erpf")
    if employee_pf == None:
        employee_pf = 0
    annualemployer_pf = request.POST.get("annualerpf")
    if annualemployee_pf == None:
        annualemployee_pf = 0
    employer_pf_admin = request.POST.get("erpfadmin")
    if employer_pf_admin == None:
        employer_pf_admin = 0
    annualemployer_pf_admin = request.POST.get("annualerpfadmin")
    if annualemployer_pf_admin  == None:
        annualemployer_pf_admin  = 0
    employer_esic = request.POST.get("ersic")
    if employer_esic  == None:
        employer_esic  = 0
    annualemployer_esic = request.POST.get("annualersic")
    if annualemployer_esic  == None:
        annualemployer_esic  = 0
    group_personal_accident = request.POST.get("gpa")
    if group_personal_accident  == None:
        group_personal_accident  = 0
    annualgroup_personal_accident = request.POST.get("annualgpa")
    if annualgroup_personal_accident  == None:
        annualgroup_personal_accident  = 0
    group_mediclaim_insurance = request.POST.get("gmi")
    if group_mediclaim_insurance == None:
        group_mediclaim_insurance  = 0
    annualgroup_mediclaim_insurance = request.POST.get("annualgmi")
    if annualgroup_mediclaim_insurance  == None:
        annualgroup_mediclaim_insurance  = 0
    employer_total_contribution = request.POST.get("tec")
    if employer_total_contribution  == None:
        employer_total_contribution  = 0
    annualemployer_total_contribution = request.POST.get("annualtec")
    if annualemployer_total_contribution  == None:
        annualemployer_total_contribution  = 0
    take_home_salary = request.POST.get("ths")
    if take_home_salary  == None:
        take_home_salary  = 0
    annualtake_home_salary = request.POST.get("annualths")
    if annualtake_home_salary  == None:
        annualtake_home_salary  = 0
    variable = request.POST.get('var')
    if variable  == None:
        variable  = 0
    annualvariable = request.POST.get("annualvar")
    if annualvariable  == None:
        annualvariable  = 0
    fixedsalary = request.POST.get('fs')
    if fixedsalary  == None:
        fixedsalary  = 0
    annualfixedsalary = request.POST.get("annualfs")
    if annualfixedsalary  == None:
        annualfixedsalary  = 0
    cost_to_company = request.POST.get("ctc")
    if cost_to_company  == None:
        cost_to_company  = 0
    annualcost_to_company = request.POST.get("annualctc")
    if annualcost_to_company  == None:
        annualcost_to_company  = 0
    return ss_gross_salary, basic, annualbasic, house_rent_allowance, annualhouse_rent_allowance, statutory_bonus, annualstatutory_bonus, special_allowance, annualspecial_allowance, annualgross_salary, employee_pf, annualemployee_pf, employee_esic, annualemployer_esic, employee_total_contribution, annualemployee_total_contribution, employer_pf, annualemployer_pf, employer_pf_admin, annualemployer_pf_admin, employer_esic, group_personal_accident, annualgroup_personal_accident, group_mediclaim_insurance, annualgroup_mediclaim_insurance, employer_total_contribution, annualemployer_total_contribution, cost_to_company, annualcost_to_company, take_home_salary, annualtake_home_salary

def create_dummy(firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, email, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, ta_spoc, onboarding_spoc, la_fk, salarytype_fk, gross_salary, request):
    last_code_query = dummy_candidate_code.objects.latest('candidate_code')                
    last_code_str = last_code_query.candidate_code
    next_code_int = int(last_code_str[1:]) + 1
    new_code = 'D' + str(next_code_int).zfill(9) #pk_candidate_code
    loc_code = remove_specials(loc_code)
    new_dummy_candidate = dummy_candidate(pk_candidate_code=new_code, First_Name=firstname , Middle_Name=middlename , Last_Name= lastname , Date_of_Joining= doj, Date_of_Birth= dob, Father_Name= fathername, Mother_Name= mothername,
    Aadhaar_Number= aadhaar, PAN_Number= Pan, Contact_Number= contact_no, Emergency_Contact_Number= emergency_no, Type_of_Hiring= hiring_fk, Replacement= replacement , Personal_Email_Id= email,
    Sub_Source= subsource_fk, Referral= referral , fk_vendor_code= vendor_fk, fk_entity_code= entity_fk, fk_department_code= department_fk, fk_function_code= function_fk, 
    fk_team_code= team_fk, fk_subteam_code= sub_team_fk, fk_designation_code= designation_fk, fk_region_code= region_fk, fk_state_code= state_fk, fk_city_code= city_fk, fk_location_code= location_fk, Gross_Salary_Entered= loc_code,
    Reporting_Manager= reporting_manager , Reporting_Manager_E_Mail_ID= reporting_manager_email, Gender= gender_fk, E_Mail_ID_Creation= email_creation, TA_Spoc_Email_Id= ta_spoc, Onboarding_Spoc_Email_Id= onboarding_spoc,
    Laptop_Allocation= la_fk, Salary_Type= salarytype_fk, Gross_Salary_Amount= float(gross_salary), created_by = str(request.user), candidate_status=pending_status, created_date_time= datetime.now())
    new_dummy_candidate.save()

    save_new_code = dummy_candidate_code(candidate_code= new_code)
    save_new_code.save()
    return new_code


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Vendor').exists())
def edit_candidate(request): 
    try:
        if request.method == 'POST':
            candidate_id = request.POST.get("c_id")   
            entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list = candidate_form_lists()
            candidate_list = master_candidate.objects.filter(pk=candidate_id)
            # if request.POST.get('c_id') != '':
            cid = request.POST.get('c_id')
            firstname = request.POST.get("c_firstname").capitalize()
            middlename = request.POST.get("c_middlename").capitalize()
            # print(middlename)
            lastname = request.POST.get("c_lastname").capitalize()
            dob = request.POST.get("c_dob")
            contact_no = request.POST.get("c_contact")
            emergency_no = request.POST.get("c_emergency")
            email = request.POST.get("c_email")
            c_gender = request.POST.get("c_gender")
            fathername = request.POST.get("c_fathername").capitalize()
            mothername = request.POST.get("c_mothername").capitalize()
            aadhaar = request.POST.get("c_aadhaar")
            Pan = request.POST.get("c_pan")
            hiring = request.POST.get("c_hiring_type")
            doj = request.POST.get("c_doj")        
            replacement = request.POST.get("c_replacement")
             
            referral = request.POST.get("c_referral")
             
            subsource = request.POST.get("c_sub_source")
            entity = request.POST.get("c_entity")
            vendor = request.POST.get("c_vendor")
            department = request.POST.get("c_dept")
            function = request.POST.get("c_function")
            team = request.POST.get("c_team")
            sub_team = request.POST.get("c_subteam")
            designation = request.POST.get("c_desg")
            region = request.POST.get("c_region")
            state = request.POST.get("c_state")
            city = request.POST.get("c_city")
            location = request.POST.get("c_location")
            # loc_code = request.POST.get("c_location_code") #check
             #check

            ta_spoc = request.POST.get("c_ta_spoc") #check
            onboarding_spoc = Onboarding_SPOC #check
            reporting_manager = request.POST.get("c_reporting_manager")
            reporting_manager_email = request.POST.get("c_reporting_manager_email")
            email_creation = request.POST.get("c_email_creation")
            laptopallocation = request.POST.get("c_laptop_allocation")
            salarytype = request.POST.get("c_salary_type")
            gross_salary = request.POST.get("c_gross_salary")
            loc_code = request.POST.get("c_gross_salary")
            
            if hiring == None or hiring == '':
                messages.warning(request, "Choose Hiring Type And Try Again")
                return redirect("csp_app:candidate")
            hiring_fk = hiring_type.objects.get(pk= hiring)
            if sub_source == None or sub_source == '':
                messages.warning(request, "Choose  Sub Source  And Try Again")
                return redirect("csp_app:candidate")
            subsource_fk = sub_source.objects.get(pk= subsource)
            if c_gender == None or c_gender == '':
                messages.warning(request, "Choose  Gender And Try Again")
                return redirect("csp_app:candidate")
            gender_fk = gender.objects.get(pk= c_gender)
            if laptopallocation == None or laptopallocation == '':
                messages.warning(request, "Choose  Laptop Allocation And Try Again")
                return redirect("csp_app:candidate")
            la_fk = laptop_allocation.objects.get(pk= laptopallocation)
            if salarytype == None or salarytype == '':
                messages.warning(request, "Choose  Salary Type And Try Again")
                return redirect("csp_app:candidate")
            salarytype_fk = salary_type.objects.get(pk= salarytype)
            if entity == None or entity == '':
                messages.warning(request, "Choose  Company  And Try Again")
                return redirect("csp_app:candidate")
            entity_fk = master_entity.objects.get(pk= entity)
            if vendor == None or vendor == '':
                messages.warning(request, "Choose  vendor  And Try Again")
                return redirect("csp_app:candidate")
            vendor_fk = master_vendor.objects.get(pk= vendor)
            if department == None or department == '':
                messages.warning(request, "Choose  Department  And Try Again")
                return redirect("csp_app:candidate")
            department_fk = master_department.objects.get(pk= department)
            if function == None or function == '':
                messages.warning(request, "Choose  Function  And Try Again")
                return redirect("csp_app:candidate")
            function_fk = master_function.objects.get(pk= function)
            if team == None or team == '':
                messages.warning(request, "Choose  Team  And Try Again")
                return redirect("csp_app:candidate")
            team_fk = master_team.objects.get(pk= team)
            if sub_team == None or sub_team == '':
                messages.warning(request, "Choose  Sub Team  And Try Again")
                return redirect("csp_app:candidate")
            sub_team_fk = master_sub_team.objects.get(pk= sub_team)
            if designation == None or designation == '':
                messages.warning(request, "Choose  Designation  And Try Again")
                return redirect("csp_app:candidate")
            designation_fk = master_designation.objects.get(pk= designation)
            if region == None or region == '':
                messages.warning(request, "Choose  Region  And Try Again")
                return redirect("csp_app:candidate")
            region_fk = master_region.objects.get(pk= region)
            if state == None or state == '':
                messages.warning(request, "Choose  State  And Try Again")
                return redirect("csp_app:candidate")
            state_fk = master_state.objects.get(pk= state)
            if city == None or city == '':
                messages.warning(request, "Choose  City  And Try Again")
                return redirect("csp_app:candidate")
            city_fk = master_city.objects.get(pk= city)
            if location == None or location == '':
                messages.warning(request, "Choose  Location  And Try Again")
                return redirect("csp_app:candidate")
            location_fk = master_location.objects.get(pk= location)
            # ss_gross_salary, basic, annualbasic, house_rent_allowance, annualhouse_rent_allowance, statutory_bonus, annualstatutory_bonus, special_allowance, annualspecial_allowance, annualgross_salary, employee_pf, annualemployee_pf, employee_esic, annualemployer_esic, employee_total_contribution, annualemployee_total_contribution, employer_pf, annualemployer_pf, employer_pf_admin, annualemployer_pf_admin, employer_esic, group_personal_accident, annualgroup_personal_accident, group_mediclaim_insurance, annualgroup_mediclaim_insurance, employer_total_contribution, annualemployer_total_contribution, cost_to_company, annualcost_to_company, take_home_salary, annualtake_home_salary = salary_structure_post_values(request)
            basic = request.POST.get("basic")
            if basic == None:
                basic = 0
            annualbasic = request.POST.get("annualbasic")
            if annualbasic == None:
                annualbasic = 0
            house_rent_allowance = request.POST.get("hra")
            if house_rent_allowance == None:
                house_rent_allowance = 0
            annualhouse_rent_allowance = request.POST.get("annualhra")
            if annualhouse_rent_allowance == None:
                annualhouse_rent_allowance = 0
            statutory_bonus = request.POST.get("sb")
            if statutory_bonus == None:
                statutory_bonus = 0
            annualstatutory_bonus = request.POST.get("annualsb")
            if annualstatutory_bonus == None:
                annualstatutory_bonus = 0
            special_allowance = request.POST.get("sa")
            if special_allowance == None:
                special_allowance = 0
            annualspecial_allowance = request.POST.get("annualsa")
            if annualspecial_allowance == None:
                annualspecial_allowance = 0
            ss_gross_salary = request.POST.get("gs")
            if ss_gross_salary == None:
                ss_gross_salary = 0
            annualgross_salary = request.POST.get("annualgs")
            if annualgross_salary == None:
                annualgross_salary = 0
            employee_pf = request.POST.get("epf")
            if employee_pf == None:
                employee_pf = 0
            annualemployee_pf = request.POST.get("annualepf")
            if annualemployee_pf == None:
                annualemployee_pf = 0
            employee_esic = request.POST.get("esic")
            if employee_esic == None:
                employee_esic = 0
            annualemployee_esic = request.POST.get("annualesic")
            if annualemployee_esic == None:
                annualemployee_esic = 0
            employee_total_contribution = request.POST.get("tc")
            if employee_total_contribution == None:
                employee_total_contribution = 0
            annualemployee_total_contribution = request.POST.get("annualtc")
            if annualemployee_total_contribution == None:
                annualemployee_total_contribution = 0
            employer_pf = request.POST.get("erpf")
            if employee_pf == None:
                employee_pf = 0
            annualemployer_pf = request.POST.get("annualerpf")
            if annualemployee_pf == None:
                annualemployee_pf = 0
            employer_pf_admin = request.POST.get("erpfadmin")
            if employer_pf_admin == None:
                employer_pf_admin = 0
            annualemployer_pf_admin = request.POST.get("annualerpfadmin")
            if annualemployer_pf_admin  == None:
                annualemployer_pf_admin  = 0
            employer_esic = request.POST.get("ersic")
            if employer_esic  == None:
                employer_esic  = 0
            annualemployer_esic = request.POST.get("annualersic")
            if annualemployer_esic  == None:
                annualemployer_esic  = 0
            group_personal_accident = request.POST.get("gpa")
            if group_personal_accident  == None:
                group_personal_accident  = 0
            annualgroup_personal_accident = request.POST.get("annualgpa")
            if annualgroup_personal_accident  == None:
                annualgroup_personal_accident  = 0
            group_mediclaim_insurance = request.POST.get("gmi")
            if group_mediclaim_insurance == None:
                group_mediclaim_insurance  = 0
            annualgroup_mediclaim_insurance = request.POST.get("annualgmi")
            if annualgroup_mediclaim_insurance  == None:
                annualgroup_mediclaim_insurance  = 0
            employer_total_contribution = request.POST.get("tec")
            if employer_total_contribution  == None:
                employer_total_contribution  = 0
            annualemployer_total_contribution = request.POST.get("annualtec")
            if annualemployer_total_contribution  == None:
                annualemployer_total_contribution  = 0
            take_home_salary = request.POST.get("ths")
            if take_home_salary  == None:
                take_home_salary  = 0
            annualtake_home_salary = request.POST.get("annualths")
            if annualtake_home_salary  == None:
                annualtake_home_salary  = 0
            variable = request.POST.get("var")
            if variable  == None:
                variable  = 0
            annualvariable = request.POST.get("annualvar")
            if annualvariable  == None:
                annualvariable  = 0
            fixedsalary = request.POST.get('fs')
            if fixedsalary  == None:
                fixedsalary  = 0
            annualfixedsalary = request.POST.get("annualfs")
            if annualfixedsalary  == None:
                annualfixedsalary  = 0
            cost_to_company = request.POST.get("ctc")
            if cost_to_company  == None:
                cost_to_company  = 0
            annualcost_to_company = request.POST.get("annualctc")
            if annualcost_to_company  == None:
                annualcost_to_company  = 0
            try:                
                dup_candidate_aadhaar = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Aadhaar_Number= aadhaar, status= active_status)
                messages.error( request, "Aadhaar Number Already Exist")
                return redirect("csp_app:candidate")
                
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_pan = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(PAN_Number= Pan, status= active_status)
                messages.error( request, "PAN  Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_contact = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Contact_Number= contact_no, status= active_status)
                messages.error( request, "Contact Number Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
            
                dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                messages.error( request, "Candidate Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_email = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Personal_Email_Id=email, status= active_status)
                messages.error( request, "Candidate Email Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_details = master_candidate.objects.exclude(pk_candidate_code=candidate_id).get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                messages.error( request, "Same Candidate Exist with ID : " + dup_candidate_details.pk)
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
           
                new_code = create_dummy(firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, email, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, ta_spoc, onboarding_spoc, la_fk, salarytype_fk, gross_salary, request)
                dummy = dummy_candidate.objects.get(pk=new_code)
                
                loc_code = remove_specials(loc_code)
              
                selected_candidate, ss_gross_salary = update_selected_candidate(candidate_id, firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, onboarding_spoc, la_fk, salarytype_fk, request, email, ss_gross_salary)
                changes_list = check_for_changes(selected_candidate, firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, hiring, replacement, email, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, reporting_manager, reporting_manager_email, gender_fk, email_creation, onboarding_spoc, la_fk, salarytype_fk, salarytype, gross_salary)
                
                

                new_salary_structure = salary_structure(candidate_code= selected_candidate.pk, basic= INR_to_number(basic), annual_basic= INR_to_number(annualbasic), house_rent_allowance= INR_to_number(house_rent_allowance), annual_house_rent_allowance= INR_to_number(annualhouse_rent_allowance), statutory_bonus=INR_to_number(statutory_bonus), annual_statutory_bonus= INR_to_number(annualstatutory_bonus),
                    special_allowance=INR_to_number(special_allowance), annual_special_allowance=INR_to_number(annualspecial_allowance),gross_salary=INR_to_number(ss_gross_salary), annual_gross_salary=INR_to_number(annualgross_salary), employee_pf= INR_to_number(employee_pf), annual_employee_pf= INR_to_number(annualemployee_pf),
                    employee_esic= INR_to_number(employee_esic), annual_employee_esic= INR_to_number(annualemployer_esic), employee_total_contribution= INR_to_number(employee_total_contribution), annual_employee_total_contribution= INR_to_number(annualemployee_total_contribution), employer_pf= INR_to_number(employer_pf), annual_employer_pf= INR_to_number(annualemployer_pf),
                    employer_pf_admin=INR_to_number(employer_pf_admin), annual_employer_pf_admin= INR_to_number(annualemployer_pf_admin), employer_esic= INR_to_number(employer_esic), annual_employer_esic= INR_to_number(annualemployer_esic), group_personal_accident= INR_to_number(group_personal_accident), annual_group_personal_accident= INR_to_number(annualgroup_personal_accident),
                    group_mediclaim_insurance= INR_to_number(group_mediclaim_insurance), annual_group_mediclaim_insurance = INR_to_number(annualgroup_mediclaim_insurance), employer_total_contribution= INR_to_number(employer_total_contribution), annual_employer_total_contribution= INR_to_number(annualemployer_total_contribution), cost_to_company=INR_to_number(cost_to_company),
                    annual_cost_to_company= INR_to_number(annualcost_to_company), take_home_salary= INR_to_number(take_home_salary), annual_take_home_salary= INR_to_number(annualtake_home_salary), variable= INR_to_number(variable), annual_var= INR_to_number(annualvariable), fixed_salary= INR_to_number(fixedsalary), annual_fixed_salary= INR_to_number(annualfixedsalary))
                new_salary_structure.save()
                alltemplate = render_to_string('emailtemplates/candidate_edited_et.html', {'candidate_code':cid ,'user': request.user})
                our_email = EmailMessage(
                    'Candidate Account Updated.',
                    alltemplate,
                    settings.EMAIL_HOST_USER,
                    [ selected_candidate.TA_Spoc_Email_Id, onboarding_spoc, 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()
                limtemplate = render_to_string('emailtemplates/candidate_edited_et_limited.html', {'candidate_code':cid ,'user': request.user})
                our_email = EmailMessage(
                    'Candidate Account Updated.',
                    limtemplate,
                    settings.EMAIL_HOST_USER,
                    [ reporting_manager_email, 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()
                
                messages.success(request, "Candidate Updated Successfully")
                return redirect("csp_app:candidate")

        return render(request, 'candidate/editcandidate.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'location_list': location_list, 
        'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
        'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
        'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
        'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'selected_candidate': candidate_list })
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

def candidate_form_lists():
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    vendor_list = master_vendor.objects.filter(status = active_status).order_by('vendor_name')
    dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
    function_list = master_function.objects.filter(status = active_status).order_by('function_name')
    team_list = master_team.objects.filter(status = active_status).order_by('team_name')
    subteam_list = master_sub_team.objects.filter(status = active_status).order_by('sub_team_name')
    desg_list = master_designation.objects.filter(status = active_status).order_by('designation_name')
    region_list = master_region.objects.filter(status = active_status).order_by('region_name')
    state_list = master_state.objects.filter(status = active_status).order_by('state_name')
    city_list = master_city.objects.filter(status= active_status).order_by('city_name')
    location_list = master_location.objects.filter(status= active_status).order_by('location_name')
    hiring_type_list = hiring_type.objects.filter(status= active_status).order_by('hiring_type_name')
    sub_source_list = sub_source.objects.filter(status= active_status).order_by('sub_source_name')
    salary_type_list = salary_type.objects.filter(status= active_status).order_by('salary_type_name')
    gender_list = gender.objects.filter(status= active_status)
    laptop_allocation_list = laptop_allocation.objects.filter(status= active_status)
    return entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Recruiter').exists() or u.groups.filter(name='Onboarding SPOC').exists())
def create_candidate(request):
    entity_list, location_list, city_list, state_list, region_list, dept_list, function_list, team_list, subteam_list, desg_list, hiring_type_list, sub_source_list, salary_type_list, gender_list, laptop_allocation_list, vendor_list = candidate_form_lists()
    
    try:
        if request.method == 'POST':
            firstname = request.POST.get("c_firstname").capitalize()
            middlename = request.POST.get("c_middlename").capitalize()
            lastname = request.POST.get("c_lastname").capitalize()
            dob = request.POST.get("c_dob")
            contact_no = request.POST.get("c_contact")
            emergency_no = request.POST.get("c_emergency")
            email = request.POST.get("c_email")
            c_gender = request.POST.get("c_gender")
            fathername = request.POST.get("c_fathername").capitalize()
            mothername = request.POST.get("c_mothername").capitalize()
            aadhaar = request.POST.get("c_aadhaar")
            Pan = request.POST.get("c_pan")
            hiring = request.POST.get("c_hiring_type")
            doj = request.POST.get("c_doj")        
            replacement = request.POST.get("c_replacement")
             
            referral = request.POST.get("c_referral")
             
            subsource = request.POST.get("c_sub_source")
            entity = request.POST.get("c_entity")
            vendor = request.POST.get("c_vendor")
            department = request.POST.get("c_dept")
            function = request.POST.get("c_function")
            team = request.POST.get("c_team")
            sub_team = request.POST.get("c_subteam")
            designation = request.POST.get("c_desg")
            region = request.POST.get("c_region")
            state = request.POST.get("c_state")
            city = request.POST.get("c_city")
            location = request.POST.get("c_location")

            ta_spoc = request.user.email #check
            onboarding_spoc = Onboarding_SPOC #check
            reporting_manager = request.POST.get("c_reporting_manager")
            reporting_manager_email = request.POST.get("c_reporting_manager_email")
            email_creation = request.POST.get("c_email_creation")
            laptopallocation = request.POST.get("c_laptop_allocation")
            salarytype = request.POST.get("c_salary_type")
            gross_salary = request.POST.get("c_gross_salary")
            loc_code = request.POST.get("c_gross_salary")
            if hiring == None or hiring == '':
                messages.warning(request, "Choose Hiring Type And Try Again")
                return redirect("csp_app:new_candidate")
            hiring_fk = hiring_type.objects.get(pk= hiring)
            if sub_source == None or sub_source == '':
                messages.warning(request, "Choose  Sub Source  And Try Again")
                return redirect("csp_app:new_candidate")
            subsource_fk = sub_source.objects.get(pk= subsource)
            if c_gender == None or c_gender == '':
                messages.warning(request, "Choose  Gender And Try Again")
                return redirect("csp_app:new_candidate")
            gender_fk = gender.objects.get(pk= c_gender)
            if laptopallocation == None or laptopallocation == '':
                messages.warning(request, "Choose  Laptop Allocation And Try Again")
                return redirect("csp_app:new_candidate")
            la_fk = laptop_allocation.objects.get(pk= laptopallocation)
            if salarytype == None or salarytype == '':
                messages.warning(request, "Choose  Salary Type And Try Again")
                return redirect("csp_app:new_candidate")
            salarytype_fk = salary_type.objects.get(pk= salarytype)
            if entity == None or entity == '':
                messages.warning(request, "Choose  Company  And Try Again")
                return redirect("csp_app:new_candidate")
            entity_fk = master_entity.objects.get(pk= entity)
            if vendor == None or vendor == '':
                messages.warning(request, "Choose  vendor And Try Again")
                return redirect("csp_app:new_candidate")
            vendor_fk = master_vendor.objects.get(pk= vendor)
            if department == None or department == '':
                messages.warning(request, "Choose  Department  And Try Again")
                return redirect("csp_app:new_candidate")
            department_fk = master_department.objects.get(pk= department)
            if function == None or function == '':
                messages.warning(request, "Choose  Function  And Try Again")
                return redirect("csp_app:new_candidate")
            function_fk = master_function.objects.get(pk= function)
            if team == None or team == '':
                messages.warning(request, "Choose  Team  And Try Again")
                return redirect("csp_app:new_candidate")
            team_fk = master_team.objects.get(pk= team)
            if sub_team == None or sub_team == '':
                messages.warning(request, "Choose  Sub Team  And Try Again")
                return redirect("csp_app:new_candidate")
            sub_team_fk = master_sub_team.objects.get(pk= sub_team)
            if designation == None or designation == '':
                messages.warning(request, "Choose  Designation  And Try Again")
                return redirect("csp_app:new_candidate")
            designation_fk = master_designation.objects.get(pk= designation)
            if region == None or region == '':
                messages.warning(request, "Choose  Region  And Try Again")
                return redirect("csp_app:new_candidate")
            region_fk = master_region.objects.get(pk= region)
            if state == None or state == '':
                messages.warning(request, "Choose  State  And Try Again")
                return redirect("csp_app:new_candidate")
            state_fk = master_state.objects.get(pk= state)
            if city == None or city == '':
                messages.warning(request, "Choose  City  And Try Again")
                return redirect("csp_app:new_candidate")
            city_fk = master_city.objects.get(pk= city)
            if location == None or location == '':
                messages.warning(request, "Choose  Location  And Try Again")
                return redirect("csp_app:new_candidate")
            location_fk = master_location.objects.get(pk= location)
               
            try:                
                dup_candidate_aadhaar = master_candidate.objects.get(Aadhaar_Number= aadhaar, status= active_status)
                messages.error( request, "Aadhaar Number Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_pan = master_candidate.objects.get(PAN_Number= Pan, status= active_status)
                messages.error( request, "PAN  Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_contact = master_candidate.objects.get(Contact_Number= contact_no, status= active_status)
                messages.error( request, "Contact Number Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
            
                dup_candidate_details = master_candidate.objects.get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                messages.error( request, "Candidate Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_email = master_candidate.objects.get(Personal_Email_Id=email, status= active_status)
                messages.error( request, "Candidate Email Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_details = master_candidate.objects.get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                messages.error( request, "Same Candidate Exist with ID : " + dup_candidate_details.pk)
                return redirect("csp_app:new_candidate")
            
            except ObjectDoesNotExist:
                new_code = create_dummy(firstname, middlename, lastname, doj, dob, fathername, mothername, aadhaar, Pan, contact_no, emergency_no, hiring_fk, replacement, email, subsource_fk, referral, vendor_fk, entity_fk, department_fk, function_fk, team_fk, sub_team_fk, designation_fk, region_fk, state_fk, city_fk, location_fk, loc_code, reporting_manager, reporting_manager_email, gender_fk, email_creation, ta_spoc, onboarding_spoc, la_fk, salarytype_fk, gross_salary, request)
                dummy = dummy_candidate.objects.get(pk=new_code)
                minimum_wage = ''
                                #monthly
                try:
                    
                    minimum_wage = master_minimum_wages.objects.get(fk_skill_code = dummy.fk_designation_code.fk_skill_code.pk, fk_state_code= dummy.fk_state_code.state_name_id, status=active_status)
                    minimum_wage_list = master_minimum_wages.objects.filter(fk_state_code= dummy.fk_state_code.state_name_id, status=active_status)
                    
                    wage = minimum_wage.wages
                except ObjectDoesNotExist:
                    wage = 0
                gsa = dummy.Gross_Salary_Amount
                state_name = dummy.fk_state_code.state_name
                salary_pk = dummy.Salary_Type.pk
                mwc =minimum_wage.wages
                gsa_value = dummy.Gross_Salary_Amount
                basic, hra, sb, sa, grossalary, annual_basic, annual_hra, annual_sb, annual_sa, annual_gs, annual_epf, annual_esic, annual_td, annual_ths, epf, esic, td, ths, erpf, erpf_admin, ersic, gpa, gmi, annual_eprf, annual_pfadmin, annual_ersic, annual_gpa, annual_gmi, tec, annual_tec, ctc, annual_ctc, var, annual_var, diff, gpi_2, fs , annual_fs= salary_structure_calculation(gsa, wage, state_name, salary_pk)
                # print(diff)
                return render(request, 'candidate/salary_structure.html', {'mwc':convert_to_INR(mwc), 'gsa':convert_to_INR(gsa_value),'dummy': dummy, 'basic': convert_to_INR(basic), 'hra': convert_to_INR(hra), 'sb': convert_to_INR(sb), 'sa': convert_to_INR(sa), 'gross_salary': convert_to_INR(grossalary), 'annualbasic': convert_to_INR(annual_basic), 'annualhra': convert_to_INR(annual_hra), 
                'annualsb': convert_to_INR(annual_sb), 'annualsa': convert_to_INR(annual_sa), 'annualgs': convert_to_INR(annual_gs), 'annualepf': convert_to_INR(annual_epf), 'annualesic': convert_to_INR(annual_esic), 'annualtd': convert_to_INR(annual_td),
                'annualths': convert_to_INR(annual_ths), 'epf': convert_to_INR(epf), 'esic': convert_to_INR(esic), 'td': convert_to_INR(td), 'ths': convert_to_INR(ths), 'erpf': convert_to_INR(erpf), 'erpf_admin': convert_to_INR(erpf_admin), 'ersic': convert_to_INR(ersic), 'gpa': convert_to_INR(gpa), 'gmi': convert_to_INR(gmi),
                'annualerpf': convert_to_INR(annual_eprf), 'annualerpf_admin': convert_to_INR(annual_pfadmin), 'annualersic': convert_to_INR(annual_ersic), 'annualgpa': convert_to_INR(annual_gpa), 'annualgmi': convert_to_INR(annual_gmi), 'tec': convert_to_INR(tec), 'annual_tec': convert_to_INR(annual_tec), 'ctc': convert_to_INR(ctc), 'annual_ctc': convert_to_INR(annual_ctc),
                'allcandidates': all_active_candidates,'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
                'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
                'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
                'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
                'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list,'variable': convert_to_INR(var), 'annual_var': convert_to_INR(annual_var), 'minimum_wage': minimum_wage, 'minimum_wage_list':minimum_wage_list, 'difference': convert_to_INR(diff), 'gpac': convert_to_INR(gpi_2), 'fs': convert_to_INR(fs), 'annual_fs': convert_to_INR(annual_fs)})
                

            return render(request, 'candidate/candidates.html', {'allcandidates': all_active_candidates,})

    except IndexError:
        return HttpResponse("No Data To Display.")

def convert_to_INR(x):
    from babel.numbers import format_currency
    return format_currency(x, 'INR', locale='en_IN')

def INR_to_number(x):  
    x = str(x)
    y = x.replace('₹','')
    z = y.replace(',','')  
    return z


def salary_structure_calculation(gsa, wage, state_name, salary_type):
    import numpy
    if salary_type == 1:
        fixed_salary = gsa
    elif salary_type == 2:
        fixed_salary = gsa * 0.80
    else:
        fixed_salary = gsa * 0.75
    basic = numpy.maximum(wage, fixed_salary * 0.50)
    if state_name == 'Maharashtra' or state_name == 'West Bengal':
        hra = basic * 0.05
    else:
        hra = 0 
    stat_bonus = numpy.ceil(numpy.maximum(wage / 12, 7000 / 12))
    if state_name == 'Kerala':
        special_allowance = 200
    else:
        special_allowance = 0
    special_allowance = numpy.ceil(numpy.maximum(special_allowance, fixed_salary-(basic + hra + stat_bonus)))
    fixed_salary = (basic + hra + stat_bonus + special_allowance)

    if salary_type == 1:
        variable_p = 0
        percent = 0
    elif salary_type == 2:
        variable_p = gsa * 0.20
        percent = 0.20
    else:
        variable_p = gsa * 0.25
        percent = 0.25

    variable = numpy.ceil((fixed_salary/(1-percent))-fixed_salary)
    # variable = numpy.maximum(variable_p, 0)

    gross_salary = fixed_salary + variable

    pf_gross = numpy.minimum(basic + special_allowance, 15000)
    epf = round(pf_gross * 0.12)
    epf_admin = round(epf / 12)
    if fixed_salary <= 21000:
        employer_esic = numpy.ceil(fixed_salary * 0.0325)
        employee_esic = numpy.ceil(fixed_salary * 0.0075)
        mediclaim = 0
    else:
        employer_esic = 0
        employee_esic = 0
        mediclaim = 91.66
    
    gpa_coverage = numpy.maximum(gross_salary * 24 , 500000)
    gpa_premium = gpa_coverage / 1000 * 0.2 / 12    

    t_employee_contribution = epf + employee_esic
  
    t_employer_contribution = epf + epf_admin + employer_esic + mediclaim + gpa_premium
    ctc = gross_salary + t_employer_contribution

    take_home = fixed_salary - t_employee_contribution

    annual_basic = basic * 12
    annual_hra = hra * 12
    annual_sb = numpy.ceil(stat_bonus * 12)
    annual_sa = numpy.ceil(special_allowance * 12)
    annual_gs = numpy.ceil(gross_salary * 12)
    annual_epf = epf * 12
    annual_esic = employee_esic * 12
    annual_td = t_employee_contribution * 12
    annual_ths = take_home * 12
    annual_eprf = epf * 12
    annual_ersic = employer_esic * 12
    annual_pfadmin = epf_admin * 12
    annual_gpa = round(mediclaim * 12,2)
    annual_gmi = round(gpa_premium * 12,2)
    annual_tec = numpy.ceil(t_employer_contribution * 12)
    annual_ctc = numpy.ceil(ctc * 12)
    annual_fs = numpy.ceil(fixed_salary * 12)
    annual_var = numpy.ceil(variable * 12)
    diff = gsa - gross_salary
    if salary_type == 1:
        fixed_salary = 0
        variable = 0
    return basic, hra, stat_bonus, special_allowance, gross_salary, annual_basic, annual_hra, annual_sb, annual_sa, annual_gs, annual_epf, annual_esic, annual_td, annual_ths, epf, employee_esic, t_employee_contribution, take_home, epf, epf_admin, employer_esic,  gpa_premium, mediclaim, annual_eprf, annual_pfadmin, annual_ersic, annual_gmi, annual_gpa, t_employer_contribution, annual_tec, ctc, annual_ctc, variable, annual_var, diff, gpa_coverage, fixed_salary, annual_fs



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='Recruiter').exists() or u.groups.filter(name='Onboarding SPOC').exists())
def save_new_candidate(request):
    try:
        if request.method == 'POST':
            firstname = request.POST.get("c_firstname").capitalize()
            middlename = request.POST.get("c_middlename").capitalize()
            lastname = request.POST.get("c_lastname").capitalize()
            dob = request.POST.get("c_dob")
            contact_no = request.POST.get("c_contact")
            emergency_no = request.POST.get("c_emergency")
            email = request.POST.get("c_email")
            c_gender = request.POST.get("c_gender")
            fathername = request.POST.get("c_fathername").capitalize()
            mothername = request.POST.get("c_mothername").capitalize()
            aadhaar = request.POST.get("c_aadhaar")
            Pan = request.POST.get("c_pan")
            hiring = request.POST.get("c_hiring_type")
            doj = request.POST.get("c_doj")        
            replacement = request.POST.get("c_replacement")
             
            referral = request.POST.get("c_referral")
             
            subsource = request.POST.get("c_sub_source")
            entity = request.POST.get("c_entity")
            vendor = request.POST.get("c_vendor")
            department = request.POST.get("c_dept")
            function = request.POST.get("c_function")
            team = request.POST.get("c_team")
            sub_team = request.POST.get("c_subteam")
            designation = request.POST.get("c_desg")
            region = request.POST.get("c_region")
            state = request.POST.get("c_state")
            city = request.POST.get("c_city")
            location = request.POST.get("c_location")

            ta_spoc = request.user.email #check
            onboarding_spoc = Onboarding_SPOC #check
            reporting_manager = request.POST.get("c_reporting_manager")
            reporting_manager_email = request.POST.get("c_reporting_manager_email")
            email_creation = request.POST.get("c_email_creation")
            laptopallocation = request.POST.get("c_laptop_allocation")
            salarytype = request.POST.get("c_salary_type")
            gross_salary = request.POST.get("c_gross_salary")
            loc_code = request.POST.get("c_gross_salary")
            basic = request.POST.get("basic")
            if basic == None:
                basic = 0
            annualbasic = request.POST.get("annualbasic")
            if annualbasic == None:
                annualbasic = 0
            house_rent_allowance = request.POST.get("hra")
            if house_rent_allowance == None:
                house_rent_allowance = 0
            annualhouse_rent_allowance = request.POST.get("annualhra")
            if annualhouse_rent_allowance == None:
                annualhouse_rent_allowance = 0
            statutory_bonus = request.POST.get("sb")
            if statutory_bonus == None:
                statutory_bonus = 0
            annualstatutory_bonus = request.POST.get("annualsb")
            if annualstatutory_bonus == None:
                annualstatutory_bonus = 0
            special_allowance = request.POST.get("sa")
            if special_allowance == None:
                special_allowance = 0
            annualspecial_allowance = request.POST.get("annualsa")
            if annualspecial_allowance == None:
                annualspecial_allowance = 0
            ss_gross_salary = request.POST.get("gs")
            if ss_gross_salary == None:
                ss_gross_salary = 0
            annualgross_salary = request.POST.get("annualgs")
            if annualgross_salary == None:
                annualgross_salary = 0
            employee_pf = request.POST.get("epf")
            if employee_pf == None:
                employee_pf = 0
            annualemployee_pf = request.POST.get("annualepf")
            if annualemployee_pf == None:
                annualemployee_pf = 0
            employee_esic = request.POST.get("esic")
            if employee_esic == None:
                employee_esic = 0
            annualemployee_esic = request.POST.get("annualesic")
            if annualemployee_esic == None:
                annualemployee_esic = 0
            employee_total_contribution = request.POST.get("tc")
            if employee_total_contribution == None:
                employee_total_contribution = 0
            annualemployee_total_contribution = request.POST.get("annualtc")
            if annualemployee_total_contribution == None:
                annualemployee_total_contribution = 0
            employer_pf = request.POST.get("erpf")
            if employee_pf == None:
                employee_pf = 0
            annualemployer_pf = request.POST.get("annualerpf")
            if annualemployee_pf == None:
                annualemployee_pf = 0
            employer_pf_admin = request.POST.get("erpfadmin")
            if employer_pf_admin == None:
                employer_pf_admin = 0
            annualemployer_pf_admin = request.POST.get("annualerpfadmin")
            if annualemployer_pf_admin  == None:
                annualemployer_pf_admin  = 0
            employer_esic = request.POST.get("ersic")
            if employer_esic  == None:
                employer_esic  = 0
            annualemployer_esic = request.POST.get("annualersic")
            if annualemployer_esic  == None:
                annualemployer_esic  = 0
            group_personal_accident = request.POST.get("gpa")
            if group_personal_accident  == None:
                group_personal_accident  = 0
            annualgroup_personal_accident = request.POST.get("annualgpa")
            if annualgroup_personal_accident  == None:
                annualgroup_personal_accident  = 0
            group_mediclaim_insurance = request.POST.get("gmi")
            if group_mediclaim_insurance == None:
                group_mediclaim_insurance  = 0
            annualgroup_mediclaim_insurance = request.POST.get("annualgmi")
            if annualgroup_mediclaim_insurance  == None:
                annualgroup_mediclaim_insurance  = 0
            employer_total_contribution = request.POST.get("tec")
            if employer_total_contribution  == None:
                employer_total_contribution  = 0
            annualemployer_total_contribution = request.POST.get("annualtec")
            if annualemployer_total_contribution  == None:
                annualemployer_total_contribution  = 0
            take_home_salary = request.POST.get("ths")
            if take_home_salary  == None:
                take_home_salary  = 0
            annualtake_home_salary = request.POST.get("annualths")
            if annualtake_home_salary  == None:
                annualtake_home_salary  = 0
            variable = request.POST.get("var")  
            if variable  == None:
                variable  = 0
            annualvariable = request.POST.get("annualvar")
            if annualvariable  == None:
                annualvariable  = 0
            fixedsalary = request.POST.get('fs')
            if fixedsalary  == None:
                fixedsalary  = 0
            annualfixedsalary = request.POST.get("annualfs")
            if annualfixedsalary  == None:
                annualfixedsalary  = 0
            cost_to_company = request.POST.get("ctc")
            if cost_to_company  == None:
                cost_to_company  = 0
            annualcost_to_company = request.POST.get("annualctc")
            if annualcost_to_company  == None:
                annualcost_to_company  = 0
            if hiring == None or hiring == '':
                messages.warning(request, "Choose Hiring Type And Try Again")
                return redirect("csp_app:new_candidate")
            hiring_fk = hiring_type.objects.get(pk= hiring)
            if sub_source == None or sub_source == '':
                messages.warning(request, "Choose  Sub Source  And Try Again")
                return redirect("csp_app:new_candidate")
            subsource_fk = sub_source.objects.get(pk= subsource)
            if c_gender == None or c_gender == '':
                messages.warning(request, "Choose  Gender And Try Again")
                return redirect("csp_app:new_candidate")
            gender_fk = gender.objects.get(pk= c_gender)
            if laptopallocation == None or laptopallocation == '':
                messages.warning(request, "Choose  Laptop Allocation And Try Again")
                return redirect("csp_app:new_candidate")
            

            
            la_fk = laptop_allocation.objects.get(pk= laptopallocation)
            if salarytype == None or salarytype == '':
                messages.warning(request, "Choose  Salary Type And Try Again")
                return redirect("csp_app:new_candidate")
            salarytype_fk = salary_type.objects.get(pk= salarytype)
            if entity == None or entity == '':
                messages.warning(request, "Choose  Company  And Try Again")
                return redirect("csp_app:new_candidate")
            entity_fk = master_entity.objects.get(pk= entity)
            if vendor == None or vendor == '':
                messages.warning(request, "Choose  vendor And Try Again")
                return redirect("csp_app:new_candidate")
            vendor_fk = master_vendor.objects.get(pk= vendor)
            if department == None or department == '':
                messages.warning(request, "Choose  Department  And Try Again")
                return redirect("csp_app:new_candidate")
            department_fk = master_department.objects.get(pk= department)
            if function == None or function == '':
                messages.warning(request, "Choose  Function  And Try Again")
                return redirect("csp_app:new_candidate")
            function_fk = master_function.objects.get(pk= function)
            if team == None or team == '':
                messages.warning(request, "Choose  Team  And Try Again")
                return redirect("csp_app:new_candidate")
            team_fk = master_team.objects.get(pk= team)
            if sub_team == None or sub_team == '':
                messages.warning(request, "Choose  Sub Team  And Try Again")
                return redirect("csp_app:new_candidate")
            sub_team_fk = master_sub_team.objects.get(pk= sub_team)
            if designation == None or designation == '':
                messages.warning(request, "Choose  Designation  And Try Again")
                return redirect("csp_app:new_candidate")
            designation_fk = master_designation.objects.get(pk= designation)
            if region == None or region == '':
                messages.warning(request, "Choose  Region  And Try Again")
                return redirect("csp_app:new_candidate")
            region_fk = master_region.objects.get(pk= region)
            if state == None or state == '':
                messages.warning(request, "Choose  State  And Try Again")
                return redirect("csp_app:new_candidate")
            state_fk = master_state.objects.get(pk= state)
            if city == None or city == '':
                messages.warning(request, "Choose  City  And Try Again")
                return redirect("csp_app:new_candidate")
            city_fk = master_city.objects.get(pk= city)
            if location == None or location == '':
                messages.warning(request, "Choose  Location  And Try Again")
                return redirect("csp_app:new_candidate")
            location_fk = master_location.objects.get(pk= location)
            try:
                # a = master_candidate.objects.get(pk = 1)
                dup_candidate_aadhaar = master_candidate.objects.get(Aadhaar_Number= aadhaar, status= active_status)
                messages.error( request, "Candidate Aadhaar Number Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_pan = master_candidate.objects.get(PAN_Number= Pan, status= active_status)
                messages.error( request, "Candidate PAN Number Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_contact = master_candidate.objects.get(Contact_Number= contact_no, status= active_status)
                messages.error( request, "Candidate Contact Number Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_details = master_candidate.objects.get(Father_Name= fathername, First_Name= firstname, Date_of_Birth=dob, status= active_status)
                messages.error( request, "Same Candidate Exist with ID : " + dup_candidate_details.pk)
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                pass
            try:
                dup_candidate_email = master_candidate.objects.get(Personal_Email_Id=email, status= active_status)
                messages.error( request, "Candidate Email Already Exist")
                return redirect("csp_app:new_candidate")
            
            except ObjectDoesNotExist:
                
                last_code_query = csp_candidate_code.objects.latest('candidate_code')                
                last_code_str = last_code_query.candidate_code
                next_code_int = int(last_code_str[1:]) + 1
                new_code = 'C' + str(next_code_int).zfill(9) 
                # loc_code = remove_specials(loc_code)
                laptop_request = laptop_request_status.objects.get(pk=3)          
                
                email_request = email_creation_request_status.objects.get(pk=3)
                new_candidate = master_candidate(pk_candidate_code=new_code, First_Name=firstname , Middle_Name=middlename , Last_Name= lastname , Date_of_Joining= doj, Date_of_Birth= dob, Father_Name= fathername, Mother_Name= mothername,
                Aadhaar_Number= aadhaar, PAN_Number= Pan, Contact_Number= contact_no, Emergency_Contact_Number= emergency_no, Type_of_Hiring= hiring_fk, Replacement= replacement , Personal_Email_Id= email,
                Sub_Source= subsource_fk, Referral= referral , fk_vendor_code= vendor_fk, fk_entity_code= entity_fk, fk_department_code= department_fk, fk_function_code= function_fk, 
                fk_team_code= team_fk, fk_subteam_code= sub_team_fk, fk_designation_code= designation_fk, fk_region_code= region_fk, fk_state_code= state_fk, fk_city_code= city_fk, fk_location_code= location_fk, Gross_Salary_Entered= loc_code,
                Reporting_Manager= reporting_manager , Reporting_Manager_E_Mail_ID= reporting_manager_email, Gender= gender_fk, E_Mail_ID_Creation= email_creation, TA_Spoc_Email_Id= ta_spoc, Onboarding_Spoc_Email_Id= onboarding_spoc,
                Laptop_Allocation= la_fk, Salary_Type= salarytype_fk, Gross_Salary_Amount= INR_to_number(ss_gross_salary), created_by = str(request.user), candidate_status=pending_status, created_date_time= datetime.now(), laptop_status= laptop_request, email_creation_status= email_request)
                new_candidate.save()
                
                save_new_code = csp_candidate_code(candidate_code= new_code)
                save_new_code.save()
                new_salary_structure = salary_structure(candidate_code= new_code, basic= INR_to_number(basic), annual_basic= INR_to_number(annualbasic), house_rent_allowance= INR_to_number(house_rent_allowance), annual_house_rent_allowance= INR_to_number(annualhouse_rent_allowance), statutory_bonus=INR_to_number(statutory_bonus), annual_statutory_bonus= INR_to_number(annualstatutory_bonus),
                special_allowance=INR_to_number(special_allowance), annual_special_allowance=INR_to_number(annualspecial_allowance),gross_salary=INR_to_number(ss_gross_salary), annual_gross_salary=INR_to_number(annualgross_salary), employee_pf= INR_to_number(employee_pf), annual_employee_pf= INR_to_number(annualemployee_pf),
                employee_esic= INR_to_number(employee_esic), annual_employee_esic= INR_to_number(annualemployer_esic), employee_total_contribution= INR_to_number(employee_total_contribution), annual_employee_total_contribution= INR_to_number(annualemployee_total_contribution), employer_pf= INR_to_number(employer_pf), annual_employer_pf= INR_to_number(annualemployer_pf),
                employer_pf_admin=INR_to_number(employer_pf_admin), annual_employer_pf_admin= INR_to_number(annualemployer_pf_admin), employer_esic= INR_to_number(employer_esic), annual_employer_esic= INR_to_number(annualemployer_esic), group_personal_accident= INR_to_number(group_personal_accident), annual_group_personal_accident= INR_to_number(annualgroup_personal_accident),
                group_mediclaim_insurance= INR_to_number(group_mediclaim_insurance), annual_group_mediclaim_insurance = INR_to_number(annualgroup_mediclaim_insurance), employer_total_contribution= INR_to_number(employer_total_contribution), annual_employer_total_contribution= INR_to_number(annualemployer_total_contribution), cost_to_company=INR_to_number(cost_to_company),
                annual_cost_to_company= INR_to_number(annualcost_to_company), take_home_salary= INR_to_number(take_home_salary), annual_take_home_salary= INR_to_number(annualtake_home_salary), variable= INR_to_number(variable), annual_var= INR_to_number(annualvariable), fixed_salary= INR_to_number(fixedsalary), annual_fixed_salary= INR_to_number(annualfixedsalary))
                new_salary_structure.save()
                limtemplate = render_to_string('emailtemplates/candidate_saved_et_limited.html', {'candidate_code':new_code ,'user': request.user})
                our_email = EmailMessage(
                    'Candidate account created action required.',
                    limtemplate,
                    settings.EMAIL_HOST_USER,
                    [ reporting_manager_email, 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()
                alltemplate = render_to_string('emailtemplates/candidate_saved_et_all.html', {'candidate_code':new_code ,'user': request.user})
                our_email = EmailMessage(
                    'Candidate account created action required.',
                    alltemplate,
                    settings.EMAIL_HOST_USER,
                    [ ta_spoc, onboarding_spoc, 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()
                
                messages.success(request, "Candidate Saved Successfully")
                return redirect("csp_app:candidate")

            return render(request, 'candidate/candidates.html', {'allcandidates': all_active_candidates,})

    except IndexError:
        return HttpResponse("No Data To Display.")

def remove_specials(a):
    a = a.replace('(','')
    a = a.replace(')','')
    a = a.replace(',','')
    a = a.replace("'",'')
    return a



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Recruiter').exists() or u.groups.filter(name='Onboarding SPOC').exists() or u.groups.filter(name='Admin').exists() or u.groups.filter(name='Vendor').exists()  )
def view_candidate(request):
    candidate_list = master_candidate.objects.filter(status = active_status)
    try:
        if request.method == 'POST':
            candidate_id = request.POST.get("view_id")
            view_candidate_list = master_candidate.objects.get(pk = candidate_id)
        return render(request, 'candidate/viewcandidate.html', {'allcandidates': all_active_candidates,'me': view_candidate_list, 'candidate_list': candidate_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def change_candidate_status(request):
    candidate_list = master_candidate.objects.filter(status = active_status)
    try:
        if request.method == 'POST':
            candidate_id = request.POST.get("c_id")
            status_id = request.POST.get("change_id")
            if status_id == None or status_id == '':
                messages.warning(request, "Please Change Status And Try Again")
                return redirect('csp_app:candidate')
            status = candidate_status.objects.get(pk = status_id)
            if candidate_id == None or candidate_id == '':
                messages.warning(request, "Candidate Not Found")
                return redirect('csp_app:candidate')
            candidate = master_candidate.objects.get(pk = candidate_id)
            prev_status = status.status_name
            vendor_id = candidate.fk_vendor_code_id
            vendor = master_vendor.objects.get(pk=vendor_id)
            candidate_vendor_mailid = vendor.vendor_email_id
            print(status.status_name)
            if str(status.status_name) == 'Hold':
                candidate.status = deactive_status
                candidate.candidate_status = status
                candidate.save()
                template = render_to_string('emailtemplates/hold_status_change_et.html', {'allcandidates': all_active_candidates, 'candidatecode':candidate.pk ,'prev_status':prev_status, 'newstatus':status.status_name , 'user': request.user})
                our_email = EmailMessage(
                    'Candidate Status Updated',
                    template,
                    settings.EMAIL_HOST_USER,
                    [ candidate_vendor_mailid, 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()            
                messages.success(request, "Candidate Status Updated")
                return redirect('csp_app:candidate')
            candidate.candidate_status = status
            candidate.save()
            template = render_to_string('emailtemplates/status_change_email_temlate.html', {'allcandidates': all_active_candidates, 'candidatecode':candidate.pk ,'prev_status':prev_status, 'newstatus':status.status_name , 'user': request.user})
            our_email = EmailMessage(
                'Candidate Status Updated',
                template,
                settings.EMAIL_HOST_USER,
                [ candidate_vendor_mailid, 'sadaf.shaikh@udaan.com'],
            ) 
            our_email.fail_silently = False
            our_email.send()            
            messages.success(request, "Candidate Status Updated")
            return redirect('csp_app:candidate')
        return render(request, 'candidate/candidates.html', {'allcandidates': all_active_candidates,'candidate_list': candidate_list })        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Vendor').exists() or u.groups.filter(name='Admin').exists() or u.groups.filter(name='Candidate').exists())
def candidate_document_upload(request, candidate_id):
    try:
        try:
            is_valid_candidate = User.objects.get(username= request.user, groups__name='Candidate')
            print(is_valid_candidate)
            
            if candidate_id != str(request.user):
                return HttpResponse("No Data To Display....")
        except ObjectDoesNotExist:
            pass
        
        document_id = request.POST.get("delete_id")
        if document_id == None:
            candidate = master_candidate.objects.filter(pk = candidate_id)
            candidate_fk = master_candidate.objects.get(pk = candidate_id)
            flag, document_count = check_for_mandatory_documents_upload(candidate_id)
            if flag == 1:
                document_list = candidate_document.objects.filter(fk_candidate_code= candidate_fk, status=active_status)
                candidate_fk.documentation_status = documentation_status.objects.get(pk=1)
                candidate_fk.save()
            else:
                is_vendor = User.objects.filter(username= request.user, groups__name='Vendor')
                if len(is_vendor) > 0:
                    mandatory_list = mandatory_documents.objects.all()
                    document_list = candidate_document.objects.filter(fk_candidate_code= candidate_fk, status=active_status)
                else:
                    mandatory_list = mandatory_documents.objects.all().exclude(pk=1)
                    document_list = candidate_document.objects.filter(fk_candidate_code= candidate_fk, status=active_status).exclude(document_catagory_id=1)
                if document_count > 0:
                    candidate_fk.documentation_status = documentation_status.objects.get(pk=4)
                    candidate_fk.save()
                else:
                    candidate_fk.documentation_status = documentation_status.objects.get(pk=2)
                    candidate_fk.save()
                


            
        if request.POST.get("delete_id") != None or request.POST.get("delete_id") != '':
            
                 
            try:
                selected_document = candidate_document.objects.get(pk = document_id)     
                cid = selected_document.fk_candidate_code.pk    
                candidate = master_candidate.objects.get(pk = cid)  
                if selected_document.document_catagory_id == 1:
                    candidate.offer_letter_status = offer_letter_status.objects.get(pk = 0)
                    candidate.save()
                if selected_document.document_catagory_id != 0:
                    candidate.documentation_status = documentation_status.objects.get(pk = 2)
                    candidate.save()
                selected_document.delete()
                messages.success(request, "Document Deleted Successfully")
                return redirect('csp_app:document_upload', cid)
            except ObjectDoesNotExist:
                pass
            
        
        
        
        if request.method == 'POST':
            candidate_fk = master_candidate.objects.get(pk = candidate_id)

            f_catogory = request.POST.get("c_catogory")
          
            file_name_entered = request.POST.get("c_filename")
           
            c_file = request.FILES['file']
            
            if c_file == None or c_file == '' :
                messages.warning(request, "Choose File")
                return redirect('csp_app:document_upload')
            file_name = c_file.name
           
            if file_name.endswith('.pdf') or file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.JPG') or file_name.endswith('.PNG'):                
                fs = FileSystemStorage()
                filename = fs.save(file_name, c_file)
                file_url = fs.url(filename)   
            else:
                messages.error(request, "File Format Not Supported")
                return redirect('csp_app:document_upload', candidate_id = candidate_id )    
            catogory_fk = mandatory_documents.objects.get(pk = f_catogory)
          
            try:
                if f_catogory != '0':
                    
                    duplicate_catogory = candidate_document.objects.get(document_catagory= catogory_fk, fk_candidate_code= candidate_id, status= active_status)
                    messages.error(request, "File Already Exist Delete Existing File To Save New One")
                    return redirect('csp_app:document_upload', candidate_id = candidate_id )
                duplicate_doc = candidate_document.objects.get(file_name=file_name_entered, fk_candidate_code= candidate_fk, status = active_status)
                messages.error(request, "Duplicate Document Name")
                return redirect('csp_app:document_upload', candidate_id = candidate_id )
                
            except ObjectDoesNotExist:
                if file_name_entered == None or file_name_entered == '':
                    file_name_entered = file_name
                new_document = candidate_document(fk_candidate_code= candidate_fk, document_catagory= catogory_fk , file_name= file_name_entered, file_upload = file_url, created_by= str(request.user), created_date_time= datetime.now())
                new_document.save()
                if catogory_fk.pk == 1:
                    candidate_fk.offer_letter_status = offer_letter_status.objects.get(pk = 1)
                    candidate_fk.save()
                messages.success(request, "Document Saved Successfully")
                return redirect('csp_app:document_upload', candidate_id = candidate_id)
        all_active_candidates = vendor_candidates(request.user)
        return render(request, 'candidate/candidatedocuments.html', {'allcandidates': all_active_candidates, 'view_candidate': candidate, 'mandatory_list': mandatory_list, 'document_list': document_list })        

    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

def check_for_mandatory_documents_upload(candidate_id):
    selected_candidate = master_candidate.objects.get(pk_candidate_code=candidate_id, status=active_status)
    mandatory_list = mandatory_documents.objects.all().exclude(pk=0)
    candidate_document_list = candidate_document.objects.filter(fk_candidate_code = selected_candidate).exclude(document_catagory_id=0)
    mandatory_document_len = len(mandatory_list)
    candidate_document_len = len(candidate_document_list)
    if mandatory_document_len == candidate_document_len:
        return 1, candidate_document_len
    else:
        return -1, candidate_document_len


# @login_required(login_url='/notlogin/')
# @user_passes_test(lambda u: u.groups.filter(name='Vendor').exists() or u.groups.filter(name='Admin').exists() or u.groups.filter(name='Candidate').exists())
# def candidate_delete_document(request):
#     try:
#         if request.method == 'POST':
#             document_id = request.POST.get("delete_id")          
#             selected_document = candidate_document.objects.get(pk = document_id, status= active_status)            
#             selected_document.delete()
#             messages.success(request, "Document Deleted Successfully")
#             return redirect('csp_app:entity')
        
#         return render(request, 'csp_app/candidatedocuments.html', {})        
#     except UnboundLocalError:
#         return HttpResponse("No Data To Display.")


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Vendor').exists())
def change_candidate_status_vendor(request):
    try:
        if request.method == 'POST':
            candidate_id = request.POST.get("v_c_id")
            status_id = request.POST.get("v_change_id")
            if status_id == None or status_id == '':
                messages.warning(request, "Please Change Status And Try Again")
                return redirect('csp_app:candidate')
            status = vendor_status.objects.get(pk = status_id)
            if candidate_id == None or candidate_id == '':
                messages.warning(request, "Candidate Not Found")
                return redirect('csp_app:candidate')
            candidate = master_candidate.objects.get(pk = candidate_id)
            prev_status = candidate.candidate_status
            candidate_vendor_mailid = candidate.fk_vendor_code.vendor_email_id
            # vendor = master_vendor.objects.get(pk=vendor_id)
            # candidate_vendor_mailid = vendor.vendor_email_id
      
            candidate.vendor_status = status
            candidate.save()
            template = render_to_string('emailtemplates/vendor_status_change_et.html', {'candidate_code':candidate.pk ,'prev':prev_status, 'current':status.status_name , 'user': request.user})
            our_email = EmailMessage(
                'Candidate Status Updated By Vendor',
                template,
                settings.EMAIL_HOST_USER,
                [ candidate_vendor_mailid, 'sadaf.shaikh@udaan.com'],
            ) 
            our_email.fail_silently = False
            our_email.send()
            if str(status_id) == '0':
                template = render_to_string('emailtemplates/loi.html', {'candidate_name': candidate.First_Name, 'candidate_code':candidate.pk ,'status':status.status_name })
                our_email = EmailMessage(
                    'LOI',
                    template,
                    settings.EMAIL_HOST_USER,
                    [ candidate.Personal_Email_Id , 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                candidate.loi_status = loi_status.objects.get(pk=1)
                candidate.save()
                our_email.send()
                all_active_candidates = vendor_candidates(request.user)
                candidate = master_candidate.objects.filter(pk = candidate_id)
                messages.success(request, "Candidate Status Updated")
                return render(request, 'csp_app/candidatedocuments.html', {'allcandidates': all_active_candidates, 'view_candidate': candidate })        

            # msg = 'Candidate status for '+ str(candidate.First_Name) +' updated to' + str(status.status_name) +' from ' + str(prev_status) + ' with candidate code " ' + str(candidate.pk) + ' by ' + str(request.user) + ' .'
            # send_mail('Candidate Status Updated', msg,'workmail052020@gmail.com',[ candidate_vendor_mailid, 'sadaf.shaikh@udaan.com'],fail_silently=False)
      
            messages.success(request, "Candidate Status Updated")
            return redirect('csp_app:candidate')
        all_active_candidates = vendor_candidates(request.user)
        return render(request, 'candidate/candidates.html', {'allcandidates': all_active_candidates,'candidate_list': candidate_list })        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
  
@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Vendor').exists())
def change_candidate_status_vendor(request):
    try:
        if request.method == 'POST':
            candidate_id = request.POST.get("v_c_id")
            status_id = request.POST.get("v_change_id")
            if status_id == None or status_id == '':
                messages.warning(request, "Please Change Status And Try Again")
                return redirect('csp_app:candidate')
            status = vendor_status.objects.get(pk = status_id)
            if candidate_id == None or candidate_id == '':
                messages.warning(request, "Candidate Not Found")
                return redirect('csp_app:candidate')
            candidate = master_candidate.objects.get(pk = candidate_id)
            prev_status = candidate.candidate_status
            candidate_vendor_mailid = candidate.fk_vendor_code.vendor_email_id
            # vendor = master_vendor.objects.get(pk=vendor_id)
            # candidate_vendor_mailid = vendor.vendor_email_id
      
            candidate.vendor_status = status
            candidate.save()
            template = render_to_string('emailtemplates/vendor_status_change_et.html', {'candidate_code':candidate.pk ,'prev':prev_status, 'current':status.status_name , 'user': request.user})
            our_email = EmailMessage(
                'Candidate Status Updated By Vendor',
                template,
                settings.EMAIL_HOST_USER,
                [ candidate_vendor_mailid, 'sadaf.shaikh@udaan.com'],
            ) 
            our_email.fail_silently = False
            our_email.send()
            print(status_id)
            if str(status_id) == '0':
                print("here")
                template = render_to_string('emailtemplates/loi.html', {'candidate_name': candidate.First_Name, 'candidate_code':candidate.pk ,'status':status.status_name })
                our_email = EmailMessage(
                    'LOI',
                    template,
                    settings.EMAIL_HOST_USER,
                    [ candidate.Personal_Email_Id , 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                candidate.loi_status = loi_status.objects.get(pk=1)
                candidate.save()
                our_email.send()
            # msg = 'Candidate status for '+ str(candidate.First_Name) +' updated to' + str(status.status_name) +' from ' + str(prev_status) + ' with candidate code " ' + str(candidate.pk) + ' by ' + str(request.user) + ' .'
            # send_mail('Candidate Status Updated', msg,'workmail052020@gmail.com',[ candidate_vendor_mailid, 'sadaf.shaikh@udaan.com'],fail_silently=False)
      
            messages.success(request, "Candidate Status Updated")
            return redirect('csp_app:candidate')
        return render(request, 'candidate/candidates.html', {'allcandidates': all_active_candidates,'candidate_list': candidate_list })        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def entity(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('modified_date_time')
    
    
    return render(request, 'csp_app/entity.html', {'e_list': created_by_entities(),'allcandidates': all_active_candidates,'entity_list': entity_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_entity(request):
    try:
        if request.method == 'POST':
            entity_id = request.POST.get("delete_id")
            entity_a = master_vendor.objects.filter(fk_entity_code=entity_id, status=active_status)
            entity_d = master_department.objects.filter(fk_entity_code=entity_id, status=active_status)
            entity_c = master_candidate.objects.filter(fk_entity_code=entity_id, status=active_status)
            if len(entity_a) >= 1 or len(entity_d) >= 1 or len(entity_c) >= 1:
                messages.error(request, "Company Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:entity')
            else:
                selected_entity = master_entity.objects.get(pk = entity_id, status= active_status)
                selected_entity.modified_by = str(request.user)
                selected_entity.modified_date_time = datetime.now()
                selected_entity.status = deactive_status
                selected_entity.save()
                messages.success(request, "Company Deleted Successfully")
                return redirect('csp_app:entity')
        return render(request, 'csp_app/entity.html', {'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_entity(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    
    try:
        if request.method == 'POST':
            entity_id = request.POST.get("view_id")
            view_entity_list = master_entity.objects.filter(pk = entity_id)
        return render(request, 'csp_app/viewentity.html', {'e_list': created_by_entities(),'allcandidates': all_active_candidates,'view_entity_list': view_entity_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_entity(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    
    try:
        if request.method == 'POST':
            entity_id = request.POST.get("view_id")
            selected_entity = master_entity.objects.filter(pk = entity_id)         
           
        return render(request, 'csp_app/editentity.html', {'e_list': created_by_entities(),'allcandidates': all_active_candidates,'view_entity_list': selected_entity, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

def created_by_entities():
    e_list = master_entity.objects.filter(status = active_status).order_by('-created_date_time')
    return e_list

def created_by_vendors():
    v_list = master_vendor.objects.filter(status = active_status).order_by('-created_date_time')
    return v_list

def created_by_departments():
    d_list = master_department.objects.filter(status = active_status).order_by('-created_date_time')
    return d_list

def created_by_functions():
    f_list = master_function.objects.filter(status = active_status).order_by('-created_date_time')
    return f_list

def created_by_teams():
    t_list = master_team.objects.filter(status = active_status).order_by('-created_date_time')
    return t_list

def created_by_subteams():
    st_list = master_sub_team.objects.filter(status = active_status).order_by('-created_date_time')
    return st_list

def created_by_designations():
    desg_list = master_designation.objects.filter(status = active_status).order_by('-created_date_time')
    return desg_list

def created_by_region():
    e_list = master_region.objects.filter(status = active_status).order_by('-created_date_time')
    return e_list

def created_by_state():
    v_list = master_state.objects.filter(status = active_status).order_by('-created_date_time')
    return v_list

def created_by_city():
    d_list = master_city.objects.filter(status = active_status).order_by('-created_date_time')
    return d_list

def created_by_location():
    f_list = master_location.objects.filter(status = active_status).order_by('-created_date_time')
    return f_list

def created_by_wages():
    t_list = master_minimum_wages.objects.filter(status = active_status).order_by('-created_date_time')
    return t_list

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_entity(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                entity = master_entity.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_entity_name") != None:
                    name = request.POST.get("e_entity_name")
                    try:
                        if entity.entity_name == name :
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:entity')
                        a = master_entity.objects.get(entity_name= name , status= active_status)
                        messages.error(request, "Company Already Exist")
                        return redirect('csp_app:entity')
                    except ObjectDoesNotExist:
                        entity.entity_name = name 
                        entity.modified_by = str(request.user)
                        entity.modified_date_time = datetime.now()
                        entity.save()
                        messages.success(request, "Company Updated Successfully")
                        return redirect('csp_app:entity')
                else:
                    messages.warning(request, "Company Name Cannot Be Blank")
                    return redirect('csp_app:entity')         
           
        return render(request, 'csp_app/editentity.html', {'e_list': created_by_entities(), 'allcandidates': all_active_candidates,'view_entity_list': entity, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def create_entity(request):
    if request.method == 'POST':
        entity_name = request.POST.get("entity_name")
        if entity_name == None or entity_name == ' ':
            messages.warning(request, "Company Name Expected")
            return redirect('csp_app:entity')
        try:
            duplicate_entity = master_entity.objects.get(entity_name=entity_name , status = active_status)
            messages.error(request, "Company Already Exist")
            return redirect('csp_app:entity')
        except ObjectDoesNotExist:
            new_entity = master_entity(entity_name= entity_name , created_by = str(request.user),created_date_time= datetime.now() )
            new_entity.save()
            messages.success(request, "Company Created Successfully")
            return redirect('csp_app:entity')
    return render(request, 'csp_app/entity.html', {'allcandidates': all_active_candidates,})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def vendor(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name').order_by('entity_name')
    vendor_list = master_vendor.objects.filter(status = active_status).order_by('-created_date_time')
    ports = port_list.objects.all()
    return render(request, 'csp_app/vendor.html', {'v_list': created_by_vendors(), 'allcandidates': all_active_candidates,'entity_list': entity_list, 'vendor_list': vendor_list, 'port_list': ports})

@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def new_vendor(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name').order_by('entity_name')
    vendor_list = master_vendor.objects.filter(status = active_status).order_by('vendor_name')
    ports = port_list.objects.all()
    return render(request, 'csp_app/new_vendor.html', {'v_list': created_by_vendors(),'allcandidates': all_active_candidates,'entity_list': entity_list, 'vendor_list': vendor_list, 'port_list': ports})




@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_vendor(request):
    vendor_list = master_vendor.objects.filter(status = active_status).order_by('vendor_name')
    try:
        if request.method == 'POST':
            vendor_id = request.POST.get("view_id")
            view_vendor_list = master_vendor.objects.filter(pk = vendor_id)
        return render(request, 'csp_app/viewvendor.html', {'v_list': created_by_vendors(),'allcandidates': all_active_candidates,'view_vendor_list': view_vendor_list, 'vendor_list': vendor_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_vendor(request):
    try:
        if request.method == 'POST':
            vendor_id = request.POST.get("delete_id")
            vendor_c = master_candidate.objects.filter(fk_vendor_code=vendor_id, status=active_status)
            if len(vendor_c) >= 1:
                messages.error(request, "Vendor Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:vendor')
            else:
                selected_vendor = master_vendor.objects.get(pk = vendor_id)
                # try:
                a = str(selected_vendor.vendor_email_id)
                print(a)
                selected_user = User.objects.get(email= a)
                selected_user.is_active = False
                selected_user.save()
                selected_vendor.modified_by = str(request.user)
                selected_vendor.modified_date_time = datetime.now()
                selected_vendor.status = deactive_status
                selected_vendor.save()
                # except ObjectDoesNotExist:
                #     messages.error(request, "Vendor Account Not Found")
                #     return redirect('csp_app:vendor')
                msg = 'Vendor account disabled for '+ str(selected_vendor.vendor_name) +' with Username " ' + str(selected_vendor.vendor_email_id) + ' by ' + str(request.user) + ' .'
                send_mail('Vendor Account Disabled', msg,'workmail052020@gmail.com' ,[ selected_vendor.vendor_email_id, 'sadaf.shaikh@udaan.com'],fail_silently=False)
      
                messages.success(request, "Vendor Deleted Successfully")
                return redirect('csp_app:vendor')
        return render(request, 'csp_app/vendor.html', {'v_list': created_by_vendors(),'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_vendor(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')

    vendor_list = master_vendor.objects.filter(status = active_status).order_by('vendor_name')
    try:
        if request.method == 'POST':
            vendor_id = request.POST.get("view_id")
            selected_vendor = master_vendor.objects.filter(pk = vendor_id)         
           
        return render(request, 'csp_app/editvendor.html', {'v_list': created_by_vendors(),'allcandidates': all_active_candidates,'view_vendor_list': selected_vendor,'entity_list':entity_list, 'vendor_list': vendor_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_vendor(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                vendor = master_vendor.objects.get(pk = request.POST.get("e_id"))
                vendor_name = request.POST.get("e_vendor_name")
                vendor_spoc = request.POST.get("e_vendor_spoc")
                vendor_spoc_email = request.POST.get("e_vendor_spoc_email")
                vendor_phone = request.POST.get("e_vendor_phone")
                vendor_email = request.POST.get("e_vendor_email")
                vendor_smtp = request.POST.get("smtp_name")
                port = request.POST.get("mail_port")

                vendor_email_pwd = request.POST.get("e_vendor_email_pwd")
                entity = request.POST.get("e_vendor_entity")
                if entity == None or entity == '':
                    messages.warning(request, "Choose Company and Try Again")
                    return redirect('csp_app:vendor')
                entity_fk = master_entity.objects.get(pk = entity)
                if port == None or port == '':
                    messages.warning(request, "Choose Port and Try Again")
                    return redirect('csp_app:vendor')
                port_fk = port_list.objects.get(pk = port)
                try:
                    a = master_vendor.objects.get(vendor_name= vendor_name, vendor_email_id= vendor_email, fk_entity_code= entity_fk, status= active_status,
                    vendor_email_port=port_fk, spoc_name=spoc_name, spoc_email_id=spoc_email_id)                    
                    messages.error(request, "Vendor Already Exist")
                    return redirect('csp_app:vendor')
                except ObjectDoesNotExist:
                    selected_user = User.objects.get(email=vendor_spoc_email)
                    selected_user.email = vendor_spoc_email
                    selected_user.first_name = vendor_name 
                    
                    selected_user.save()
                    vendor.vendor_name = vendor_name 
                    vendor.spoc_name = vendor_spoc
                    vendor.fk_entity_code = entity_fk
                    vendor.spoc_email_id = vendor_spoc_email
                    vendor.vendor_email_id = vendor_email
                    vendor.vendor_email_port = port_fk
                    vendor.vendor_smtp = vendor_smtp
                    vendor.vendor_email_id_password = vendor_email_pwd
                    vendor.modified_by = str(request.user)
                    vendor.modified_date_time = datetime.now()
                    
                    vendor.save()
                    msg = 'Vendor '+ str(vendor.vendor_name) +' with Username " ' + str(vendor.vendor_email_id) + ' Updated by ' + str(request.user) + ' .'
                    send_mail('Vendor Account Updated', msg,'workmail052020@gmail.com',[ vendor.vendor_email_id, 'sadaf.shaikh@udaan.com'],fail_silently=False)
      
                    messages.success(request, "Vendor Updated Successfully")
                    return redirect('csp_app:vendor')
               
           
        return render(request, 'csp_app/editvendor.html', {'v_list': created_by_vendors(),'allcandidates': all_active_candidates,'view_vendor_list': vendor, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def create_vendor(request):    
    if request.method == 'POST':
        vendor_name = request.POST.get("vendor_name")
        vendor_spoc = request.POST.get("vendor_spoc")
        vendor_spoc_email = request.POST.get("vendor_spoc_email")
        vendor_phone = request.POST.get("vendor_phone")
        vendor_email = request.POST.get("vendor_email")
        vendor_email_pwd = request.POST.get("vendor_email_pwd")
        entity = request.POST.getlist("vendor_entity")
        smtp = request.POST.get("smtp_name")
        port = request.POST.get("mail_port")
        if entity == None or entity == '':
            messages.warning(request, "Choose Company And Try Again")
            return redirect('csp_app:vendor')
        if port == None or port == '':
            messages.warning(request, "Choose Port And Try Again")
            return redirect('csp_app:vendor')
        port_fk = port_list.objects.get(pk=port)
        for i in entity:
            entity_fk = master_entity.objects.get(pk=i)
        
            try:
                duplicate_vendor_entity_spoc = master_vendor.objects.filter(vendor_email_id= vendor_email , fk_entity_code= entity_fk, spoc_email_id=vendor_spoc_email, status = active_status)
                if duplicate_vendor_entity_spoc:
                    messages.error(request, "Vendor Already Exist")
                    return redirect('csp_app:vendor')
            
            except ObjectDoesNotExist:
                print(2)
            try:
                duplicate_vendor_email = master_vendor.objects.filter( vendor_email_id= vendor_email, fk_entity_code= entity_fk, status = active_status)
                if duplicate_vendor_email:
                    messages.error(request, "Vendor Email ID Already Exist")
                    return redirect('csp_app:vendor')
                print(3)
            except ObjectDoesNotExist:
                print(4)
            try:
                duplicate_vendor_entity = master_vendor.objects.filter( vendor_name=vendor_name , fk_entity_code= entity_fk, status = active_status)
                if duplicate_vendor_entity:                
                    messages.error(request, "Vendor Already Exist")
                    return redirect('csp_app:vendor')
                print(5)
            except ObjectDoesNotExist:   
                print('here') 
            try:      
                
                assign_group = Group.objects.get(name='Vendor')         
                user = User.objects.create_user(vendor_spoc_email)
                password = User.objects.make_random_password()
                user.password = password
                user.set_password(user.password)
                user.first_name = vendor_name 
                user.email = vendor_spoc_email
                assign_group.user_set.add(user)     
                user.save()
                newtemplate = render_to_string('emailtemplates/new_vendor_account_success_et.html', {'vendor':vendor_name, 'username': vendor_email, 'password': password})
                our_email = EmailMessage(
                    'CSP_APP: New vendor account created.',
                    newtemplate,
                    settings.EMAIL_HOST_USER,
                    [ vendor_email, vendor_spoc_email, 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()
            except IntegrityError:
                template = render_to_string('emailtemplates/use_old_password_vendor_et.html', {'vendor':vendor_name, 'entity': entity_fk, 'mail': vendor_spoc_email})
                our_email = EmailMessage(
                    'CSP_APP',
                    template,
                    settings.EMAIL_HOST_USER,
                    [ vendor_email, vendor_spoc_email, 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()  
            new_vendor = master_vendor(vendor_name= vendor_name , spoc_name= vendor_spoc,spoc_email_id= vendor_spoc_email, vendor_phone_number= vendor_phone, vendor_email_id= vendor_email, vendor_email_id_password= vendor_email_pwd, fk_entity_code= entity_fk, vendor_smtp = smtp, vendor_email_port = port_fk, created_by = str(request.user), created_date_time= datetime.now())
            new_vendor.save()
        
            newadmintemplate = render_to_string('emailtemplates/new_vendor_account_success_admin_et.html', {'vendor_name':vendor_name, 'entity': entity_fk, 'vendor_email': vendor_email, 'vendor_spoc': vendor_spoc, 'vendor_spoc_email': vendor_spoc_email, 'admin': str(request.user)})
            our_email = EmailMessage(
                'CSP_APP: New vendor account created.',
                newadmintemplate,
                settings.EMAIL_HOST_USER,
                [ request.user.email, 'sadaf.shaikh@udaan.com' ],
            ) 
            our_email.fail_silently = False
            our_email.send() 
            newadmintemplate = render_to_string('emailtemplates/new_vendor_account_success_vendor_et.html', {'vendor':vendor_name, 'entity': entity_fk.entity_name , 'user': str(request.user)})
            our_email = EmailMessage(
                'CSP_APP: New vendor account created.',
                newadmintemplate,
                settings.EMAIL_HOST_USER,
                [ request.user.email, 'sadaf.shaikh@udaan.com' ],
            ) 
            our_email.fail_silently = False
            our_email.send() 
            
            
        messages.success(request, "Vendor Account Created. Check Mail For Credentials")            
        return redirect('csp_app:vendor')
                
                
        
    return render(request, 'csp_app/vendor.html', {'v_list': created_by_vendors(),'allcandidates': all_active_candidates})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  department(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
    return render(request, 'csp_app/department.html', {'d_list': created_by_departments(),'allcandidates': all_active_candidates,'entity_list': entity_list, 'department_list': dept_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_department(request):
    try:
        if request.method == 'POST':
            department_id = request.POST.get("delete_id")
            department_f = master_function.objects.filter(fk_department_code=department_id, status=active_status)
            department_c = master_candidate.objects.filter(fk_department_code=department_id, status=active_status)
            if len(department_f) >= 1 or len(department_c) >= 1:
                messages.error(request, "Department Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:department')
            else:
                selected_department = master_department.objects.get(pk = department_id, status= active_status)
                selected_department.status = deactive_status
                selected_department.modified_by = str(request.user)
                selected_department.modified_date_time = datetime.now()
                selected_department.save()
                messages.success(request, "Department Deleted Successfully")
                return redirect('csp_app:department')
        return render(request, 'csp_app/department.html', {'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_department(request):
    
    if request.method == 'POST':
        dept_name = request.POST.get("dept_name")
        if dept_name == None or dept_name == ' ':
            messages.warning(request, "Department Name Cannot Be Blank")
            return redirect('csp_app:department')
        entity = request.POST.get("dept_entity")
        if entity == None or entity == '':
            messages.warning(request, "Choose Company And Try Again")
            return redirect('csp_app:department')
        entity_fk = master_entity.objects.get(pk=entity)
        try:
            duplicate_dept = master_department.objects.get(department_name=dept_name , fk_entity_code= entity_fk, status = active_status)
            messages.error(request, "Department Already Exist")
            return redirect('csp_app:department')
        except ObjectDoesNotExist:
            new_department = master_department(department_name= dept_name , fk_entity_code= entity_fk, created_by = str(request.user), created_date_time= datetime.now())
            new_department.save()
            return redirect('csp_app:department')
    return render(request, 'csp_app/department.html', {'allcandidates': all_active_candidates,})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_department(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    try:
        if request.method == 'POST':
            department_id = request.POST.get("view_id")
            view_dept_list = master_department.objects.filter(pk = department_id)
            d = master_department.objects.get(pk = department_id)
            print(d.created_date_time)
        return render(request, 'csp_app/viewdepartment.html', {'d_list': created_by_departments(),'allcandidates': all_active_candidates,'view_dept_list': view_dept_list,'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_department(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)

    try:
        if request.method == 'POST':
            department_id = request.POST.get("view_id")
            selected = master_department.objects.filter(pk = department_id)        
        return render(request, 'csp_app/editdepartment.html', {'d_list': created_by_departments(),'allcandidates': all_active_candidates,'view_dept_list': selected,'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_department(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_department.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_dept_name") != None:
                    name = request.POST.get("e_dept_name")
                    entity = request.POST.get("e_dept_entity")
                    if entity == None or entity == '':
                        messages.warning(request, "Choose Company and Try Again")
                        return redirect('csp_app:department')
                    entity_fk = master_entity.objects.get(pk = entity)
                    try:
                        if selected.department_name == name  and selected.fk_entity_code == entity_fk:
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:department')
                        a = master_department.objects.get(department_name= name , fk_entity_code= entity_fk, status= active_status)
                        messages.error(request, "Department Already Exist")
                        return redirect('csp_app:department')
                    except ObjectDoesNotExist:
                        selected.department_name = name 
                        selected.fk_entity_code = entity_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "Department Updated Successfully")
                        return redirect('csp_app:department')
                else:
                    messages.warning(request, "Department Name Cannot Be Blank")
                    return redirect('csp_app:department')         
           
        return render(request, 'csp_app/editdepartment.html', {'d_list': created_by_departments(),'allcandidates': all_active_candidates,'view_department_list': department, 'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  function(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
    function_list = master_function.objects.filter(status = active_status).order_by('function_name')
    return render(request, 'csp_app/function.html', {'f_list': created_by_functions(),'allcandidates': all_active_candidates,'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_function(request):
    if request.method == 'POST':
        function_name = request.POST.get("function_name")
        function_dept = request.POST.get("function_dept")
        if function_name == None or function_name == '':
            messages.warning(request, "Function Name Cannot Be Blank")
            return redirect('csp_app:function')
        if function_dept == None or function_dept == '':
            messages.warning(request, "Choose Department And Try Again")
            return redirect('csp_app:function')
        department_fk = master_department.objects.get(pk=function_dept)
        try:
            duplicate_function = master_function.objects.get(function_name=function_name , fk_department_code= department_fk, status = active_status)
            messages.error(request, "Function Already Exist")
            return redirect('csp_app:function')
        except ObjectDoesNotExist:            
            new_function = master_function( function_name= function_name , fk_department_code= department_fk, created_by = str(request.user), created_date_time= datetime.now())
            new_function.save()
            messages.success(request, "Function Saved Successfully")
            return redirect('csp_app:function')
    return render(request, 'csp_app/function.html', {'f_list': created_by_functions(),'allcandidates': all_active_candidates,})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_function(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    try:
        if request.method == 'POST':
            function_id = request.POST.get("view_id")
            view_function_list = master_function.objects.filter(pk = function_id)
        return render(request, 'csp_app/viewfunction.html', {'f_list': created_by_functions(),'allcandidates': all_active_candidates,'view_function_list': view_function_list,'function_list': function_list, 'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_function(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    try:
        if request.method == 'POST':
            function_id = request.POST.get("view_id")
            selected = master_function.objects.filter(pk = function_id)        
        return render(request, 'csp_app/editfunction.html', {'f_list': created_by_functions(),'allcandidates': all_active_candidates,'view_function_list': selected, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_function(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_function.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_function_name") != None:
                    name = request.POST.get("e_function_name")
                    department = request.POST.get("e_function_dept")
                    # entity = request.POST.get("e_function_entity")
                    print(department)
                    if department == None or department == '':
                        messages.warning(request, "Choose Department and Try Again")
                        return redirect('csp_app:function')
                    department_fk = master_department.objects.get(pk = department)
                    try:
                        if selected.function_name == name  and selected.fk_department_code == department_fk:
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:function')
                        a = master_function.objects.get(function_name= name , fk_department_code= department_fk, status= active_status)
                        messages.error(request, "function Already Exist")
                        return redirect('csp_app:function')
                    except ObjectDoesNotExist:
                        selected.function_name = name 
                        selected.fk_department_code = department_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "Function Updated Successfully")
                        return redirect('csp_app:function')
                else:
                    messages.warning(request, "Department Name Cannot Be Blank")
                    return redirect('csp_app:department')         
           
        return render(request, 'csp_app/editfunction.html', {'f_list': created_by_functions(),'allcandidates': all_active_candidates,'view_department_list': department, 'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_function(request):
    try:
        if request.method == 'POST':
            function_id = request.POST.get("delete_id")
            function_t = master_team.objects.filter(fk_function_code=function_id, status=active_status)
            function_c = master_candidate.objects.filter(fk_function_code=function_id, status=active_status)
            if len(function_t) >= 1 or len(function_c) >= 1:
                messages.error(request, "Function Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:function')
            else:
                selected = master_function.objects.get(pk = function_id, status= active_status)
                selected.status = deactive_status
                selected.modified_by = str(request.user)
                selected.modified_date_time = datetime.now()
                selected.save()
                messages.success(request, "Function Deleted Successfully")
                return redirect('csp_app:function')
        return render(request, 'csp_app/function.html', {'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  team(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
    function_list = master_function.objects.filter(status = active_status).order_by('function_name')
    team_list = master_team.objects.filter(status = active_status).order_by('team_name').order_by('created_date_time')

    return render(request, 'csp_app/team.html', {'t_list': created_by_teams(),'allcandidates': all_active_candidates,'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get("team_name")
        team_function = request.POST.get("team_function")
        if team_name == None or team_name == '':
            messages.warning(request, "Team Name Cannot Be Blank")
            return redirect('csp_app:team')
        if team_function == None or team_function == '':
            messages.warning(request, "Choose Function And Try Again")
            return redirect('csp_app:team')
        function_fk = master_function.objects.get(pk=team_function)
       
        try:
            duplicate_team = master_team.objects.get( team_name= team_name , fk_function_code=function_fk, status= active_status)
            messages.error(request, "Team Already Exist")
            return redirect('csp_app:team')
        except ObjectDoesNotExist: 
            new_team = master_team( team_name= team_name , fk_function_code=function_fk, created_by = str(request.user), created_date_time= datetime.now())
            new_team.save()
            messages.success(request, "Team Saved Successfully")
            return redirect('csp_app:team')
    return render(request, 'csp_app/team.html', {'t_list': created_by_teams(),'allcandidates': all_active_candidates,})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_team(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    team_list = master_team.objects.filter(status=active_status)

    try:
        if request.method == 'POST':
            team_id = request.POST.get("view_id")
            view_team_list = master_team.objects.filter(pk = team_id)
        return render(request, 'csp_app/viewteam.html', {'t_list': created_by_teams(),'allcandidates': all_active_candidates,'view_team_list': view_team_list,'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_team(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    team_list = master_team.objects.filter(status=active_status)

    try:
        if request.method == 'POST':
            team_id = request.POST.get("view_id")
            selected = master_team.objects.filter(pk = team_id)        
        return render(request, 'csp_app/editteam.html', {'t_list': created_by_teams(),'allcandidates': all_active_candidates,'view_team_list': selected,'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_team(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    team_list = master_team.objects.filter(status=active_status)
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_team.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_team_name") != None:
                    name = request.POST.get("e_team_name")
                    function = request.POST.get("e_team_function")
                    # entity = request.POST.get("e_function_entity")
                    # print(department)
                    if function == None or function == '':
                        messages.warning(request, "Choose Function and Try Again")
                        return redirect('csp_app:team')
                    function_fk = master_function.objects.get(pk = function)
                    try:
                        if selected.team_name == name  and selected.fk_function_code == function_fk:
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:team')
                        a = master_team.objects.get(team_name= name , fk_function_code= function_fk, status= active_status)
                        messages.error(request, "Team Already Exist")
                        return redirect('csp_app:team')
                    except ObjectDoesNotExist:
                        selected.team_name = name 
                        selected.fk_function_code = function_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "Team Updated Successfully")
                        return redirect('csp_app:team')
                else:
                    messages.warning(request, "Function Name Cannot Be Blank")
                    return redirect('csp_app:team')         
           
        return render(request, 'csp_app/editteam.html', {'t_list': created_by_teams(),'allcandidates': all_active_candidates,'view_team_list': selected,'function_list': function_list, 'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_team(request):
    try:
        if request.method == 'POST':
            team_id = request.POST.get("delete_id")
            team_t = master_sub_team.objects.filter(fk_team_code=team_id, status=active_status)
            team_c = master_candidate.objects.filter(fk_team_code=team_id, status=active_status)
            if len(team_t) >= 1 or len(team_c) >= 1:
                messages.error(request, "Team Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:team')
            else:
                selected = master_team.objects.get(pk = team_id, status= active_status)
                selected.status = deactive_status
                selected.modified_by = str(request.user)
                selected.modified_date_time = datetime.now()
                selected.save()
                messages.success(request, "Team Deleted Successfully")
                return redirect('csp_app:team')
        return render(request, 'csp_app/team.html', {'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")




@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  subteam(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
    function_list = master_function.objects.filter(status = active_status).order_by('function_name')
    team_list = master_team.objects.filter(status = active_status).order_by('team_name')
    subteam_list = master_sub_team.objects.filter(status = active_status).order_by('sub_team_name')
    return render(request, 'csp_app/subteam.html', {'t_list': created_by_subteams(),'allcandidates': all_active_candidates,'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'subteam_list': subteam_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_subteam(request):

    if request.method == 'POST':
        subteam_name = request.POST.get("subteam_name")
        team = request.POST.get("subteam_team")
        if subteam_name == None or subteam_name == '':
            messages.warning(request, "Sub Team Name Cannot Be Blank")
            return redirect('csp_app:subteam')
        if team == None or team == '':
            messages.warning(request, "Choose Team And Try Again")
            return redirect('csp_app:subteam')
        team_fk = master_team.objects.get(pk= team)
        try:
            duplicate_subteam = master_sub_team.objects.get( sub_team_name= subteam_name , fk_team_code=team_fk, status = active_status)
            messages.error(request, "Sub Team Already Exist")
            return redirect('csp_app:subteam')
        except ObjectDoesNotExist: 
            new_subteam = master_sub_team( sub_team_name= subteam_name , fk_team_code=team_fk, created_by = str(request.user), created_date_time= datetime.now())
            new_subteam.save()
            messages.success(request, "Sub Team Saved Successfully")
            return redirect('csp_app:subteam')
    return render(request, 'csp_app/subteam.html', {'allcandidates': all_active_candidates,})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_subteam(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    team_list = master_team.objects.filter(status=active_status)
    subteam_list = master_sub_team.objects.filter(status=active_status)

    try:
        if request.method == 'POST':
            subteam_id = request.POST.get("view_id")
            view_subteam_list = master_sub_team.objects.filter(pk = subteam_id)
        return render(request, 'csp_app/viewsubteam.html', {'t_list': created_by_subteams(),'allcandidates': all_active_candidates,'view_subteam_list': view_subteam_list,'subteam_list': subteam_list, 'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_subteam(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    team_list = master_team.objects.filter(status=active_status)
    subteam_list = master_sub_team.objects.filter(status=active_status)

    try:
        if request.method == 'POST':
            subteam_id = request.POST.get("view_id")
            selected = master_sub_team.objects.filter(pk = subteam_id)        
        return render(request, 'csp_app/editsubteam.html', {'t_list': created_by_subteams(),'allcandidates': all_active_candidates,'view_subteam_list': selected,'subteam_list': subteam_list, 'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_subteam(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    team_list = master_team.objects.filter(status=active_status)
    subteam_list = master_sub_team.objects.filter(status=active_status)

    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_sub_team.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_subteam_name") != None:
                    name = request.POST.get("e_subteam_name")
                    team = request.POST.get("e_subteam_team")
                    # entity = request.POST.get("e_function_entity")
                    # print(department)
                    if team == None or team == '':
                        messages.warning(request, "Choose Team and Try Again")
                        return redirect('csp_app:subteam')
                    team_fk = master_team.objects.get(pk = team)
                    try:
                        if selected.sub_team_name == name  and selected.fk_team_code == team_fk:
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:team')
                        a = master_sub_team.objects.get(sub_team_name= name , fk_team_code= team_fk, status= active_status)
                        messages.error(request, "Team Already Exist")
                        return redirect('csp_app:team')
                    except ObjectDoesNotExist:
                        selected.sub_team_name = name 
                        selected.fk_team_code = team_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "Sub Team Updated Successfully")
                        return redirect('csp_app:subteam')
                else:
                    messages.warning(request, "Sub Function Name Cannot Be Blank")
                    return redirect('csp_app:subteam')         
           
        return render(request, 'csp_app/editsubteam.html', {'t_list': created_by_subteams(),'allcandidates': all_active_candidates,'view_subteam_list': selected,'team_list': team_list, 'function_list': function_list, 'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_subteam(request):
    try:
        if request.method == 'POST':
            team_id = request.POST.get("delete_id")
            team_t = master_sub_team.objects.filter(fk_team_code=team_id, status=active_status)
            team_c = master_candidate.objects.filter(fk_team_code=team_id, status=active_status)
            if len(team_t) >= 1 or len(team_c) >= 1:
                messages.error(request, "Team Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:team')
            else:
                selected = master_sub_team.objects.get(pk = team_id, status= active_status)
                selected.status = deactive_status
                selected.modified_by = str(request.user)
                selected.modified_date_time = datetime.now()
                selected.save()
                messages.success(request, "Sub Team Deleted Successfully")
                return redirect('csp_app:subteam')
        return render(request, 'csp_app/subteam.html', {'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")




@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  designation(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
    function_list = master_function.objects.filter(status = active_status).order_by('function_name')
    team_list = master_team.objects.filter(status = active_status).order_by('team_name')
    subteam_list = master_sub_team.objects.filter(status = active_status).order_by('sub_team_name')
    desg_list = master_designation.objects.filter(status = active_status).order_by('designation_name')
    skill_list = skill_type.objects.all().order_by('-skill_name')
    return render(request, 'csp_app/designation.html', {'d_list': created_by_designations(),'allcandidates': all_active_candidates,'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list, 'skill_list': skill_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_designation(request):
    if request.method == 'POST':
        designation_name = request.POST.get("desg_name")
        subteam = request.POST.get("desg_subteam")
        skill = request.POST.get("skill")
        if subteam == None or subteam == '':
            messages.warning(request, "Choose Sub Team And Try Again")
            return redirect('csp_app:designation')
        if designation_name == None or designation_name == '':
            messages.warning(request, "Designation Cannot Be Blank")
            return redirect('csp_app:designation')
        subteam_fk = master_sub_team.objects.get(pk=subteam)
        if skill_type == None or skill_type == '':
            messages.warning(request, "Choose Skill Type And Try Again")
            return redirect('csp_app:designation')
        skill_fk = skill_type.objects.get(pk=skill)
        try:
            dup_designation = master_designation.objects.get( designation_name= designation_name , fk_sub_team_code=subteam_fk, fk_skill_code= skill_fk, status = active_status)
           
            messages.error(request, "Designation Already Exist")
            return redirect('csp_app:subteam')
        except ObjectDoesNotExist: 

            new_designation = master_designation( designation_name= designation_name , fk_sub_team_code=subteam_fk, fk_skill_code= skill_fk, created_by = str(request.user), created_date_time= datetime.now())
            new_designation.save()
            messages.success(request, "Designation Saved Successfully")
            return redirect('csp_app:designation')
    return render(request, 'csp_app/designation.html', {'allcandidates': all_active_candidates,})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_designation(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    team_list = master_team.objects.filter(status=active_status)
    subteam_list = master_sub_team.objects.filter(status=active_status)
    designation_list = master_designation.objects.filter(status=active_status)
    try:
        if request.method == 'POST':
            designation_id = request.POST.get("view_id")
            view_designation_list = master_designation.objects.filter(pk = designation_id)
        return render(request, 'csp_app/viewdesignation.html', {'d_list': created_by_designations(),'allcandidates': all_active_candidates,'view_designation_list': view_designation_list,'designation_list': designation_list,  'subteam_list': subteam_list, 'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_designation(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    team_list = master_team.objects.filter(status=active_status)
    subteam_list = master_sub_team.objects.filter(status=active_status)
    designation_list = master_designation.objects.filter(status=active_status)
    skill_list = skill_type.objects.all().order_by('-skill_name')
    try:
        if request.method == 'POST':
            designation_id = request.POST.get("view_id")
            selected = master_designation.objects.filter(pk = designation_id)        
        return render(request, 'csp_app/editdesignation.html', {'d_list': created_by_designations(),'allcandidates': all_active_candidates,'view_designation_list': selected, 'designation_list':designation_list, 'subteam_list': subteam_list, 'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list,'skill_list': skill_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_designation(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    department_list = master_department.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    team_list = master_team.objects.filter(status=active_status)
    subteam_list = master_sub_team.objects.filter(status=active_status)
    designation_list = master_designation.objects.filter(status=active_status)
    skill_list = skill_type.objects.all().order_by('-skill_name')

    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_designation.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_designation_name") != None:
                    name = request.POST.get("e_designation_name")
                    subteam = request.POST.get("e_designation_subteam")
                    skill = request.POST.get("skill")
                    if subteam == None or subteam == '':
                        messages.warning(request, "Choose Sub Team and Try Again")
                        return redirect('csp_app:designation')
                    subteam_fk = master_sub_team.objects.get(pk = subteam)
                    if skill_type == None or skill_type == '':
                        messages.warning(request, "Choose Skill Type And Try Again")
                        return redirect('csp_app:designation')
                    skill_fk = skill_type.objects.get(pk=skill)
                    try:
                        if selected.designation_name == name  and selected.fk_sub_team_code == subteam_fk and selected.fk_skill_code == skill_fk :
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:designation')
                        a = master_designation.objects.get(designation_name= name , fk_sub_team_code= subteam_fk, fk_skill_code= skill_fk, status= active_status)
                        messages.error(request, "Designation Already Exist")
                        return redirect('csp_app:designation')
                    except ObjectDoesNotExist:
                        selected.designation_name = name 
                        selected.fk_sub_team_code = subteam_fk
                        selected.fk_skill_code = skill_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "Designation Updated Successfully")
                        return redirect('csp_app:designation')
                else:
                    messages.warning(request, "Sub Team Name Cannot Be Blank")
                    return redirect('csp_app:designation')         
           
        return render(request, 'csp_app/editdesignation.html', {'d_list': created_by_designations(),'allcandidates': all_active_candidates,'view_designation_list': selected,'subteam_list':subteam_list, 'team_list': team_list, 'function_list': function_list, 'department_list': department_list, 'entity_list': entity_list, 'skill_list': skill_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_designation(request):
    try:
        if request.method == 'POST':
            desg_id = request.POST.get("delete_id")
            desg_c = master_candidate.objects.filter(fk_designation_code=desg_id, status=active_status)
            if len(desg_c) >= 1:
                messages.error(request, "Designation Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:designation')
            else:
                selected = master_designation.objects.get(pk = desg_id, status= active_status)
                selected.status = deactive_status
                selected.modified_by = str(request.user)
                selected.modified_date_time = datetime.now()
                selected.save()
                messages.success(request, "Designation Deleted Successfully")
                return redirect('csp_app:designation')
        return render(request, 'csp_app/designation.html', {'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")




@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def region(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status = active_status).order_by('region_name')
    zone_list = zones.objects.all()
    return render(request, 'csp_app/region.html', {'r_list': created_by_region(),'zone_list':zone_list, 'allcandidates': all_active_candidates,'entity_list': entity_list,'region_list': region_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def create_region(request):
    if request.method == 'POST':
        region_pk = request.POST.get("region_name")
        entity = request.POST.get("region_entity")
        if entity == None or entity == '':
            messages.warning(request, "Choose Company And Try Again")
            return redirect('csp_app:region')
        if region_pk == None or region_pk== '':
            messages.warning(request, "Region Cannot Be Blank")
            return redirect('csp_app:region')
        entity_fk = master_entity.objects.get(pk=entity)
        region_name = zones.objects.get(pk= region_pk)
        try:
            dup_region = master_region.objects.get( region_name= region_name , fk_entity_code =entity_fk, status = active_status)

            messages.error(request, "Region Already Exist")
            return redirect('csp_app:region')
        except ObjectDoesNotExist: 
            new_region = master_region( region_name= region_name , fk_entity_code =entity_fk, created_by = str(request.user), created_date_time= datetime.now())
            new_region.save()
            
            messages.success(request, "Region Saved Succesfully")
            return redirect('csp_app:region')
    return render(request, 'csp_app/region.html', {'allcandidates': all_active_candidates,})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_region(request):
    try:
        if request.method == 'POST':
            region_id = request.POST.get("delete_id")
            region_s = master_state.objects.filter(fk_region_code=region_id, status=active_status)
            region_c = master_candidate.objects.filter(fk_region_code=region_id, status=active_status)
            if len(region_s) >= 1 or len(region_c) >= 1:
                messages.error(request, "region Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:region')
            else:
                selected = master_region.objects.get(pk = region_id, status= active_status)
                selected.status = deactive_status
                selected.modified_by = str(request.user)
                selected.modified_date_time = datetime.now()
                selected.save()
                messages.success(request, "region Deleted Successfully")
                return redirect('csp_app:region')
        return render(request, 'csp_app/region.html', {'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_region(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    try:
        if request.method == 'POST':
            region_id = request.POST.get("view_id")
            view_region_list = master_region.objects.filter(pk = region_id)
        return render(request, 'csp_app/viewregion.html', {'r_list': created_by_region(),'allcandidates': all_active_candidates,'view_region_list': view_region_list,'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_region(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    zone_list = zones.objects.all()
    try:
        if request.method == 'POST':
            region_id = request.POST.get("view_id")
            selected = master_region.objects.filter(pk = region_id)        
        return render(request, 'csp_app/editregion.html', {'r_list': created_by_region(),'zone_list': zone_list, 'allcandidates': all_active_candidates,'view_region_list': selected,'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_region(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    zone_list = zones.objects.all()

    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_region.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_region_name") != None:
                    name_pk = request.POST.get("e_region_name")
                    entity = request.POST.get("e_region_entity")
                    if entity == None or entity == '':
                        messages.warning(request, "Choose Company and Try Again")
                        return redirect('csp_app:region')
                    entity_fk = master_entity.objects.get(pk = entity)
                    name = zones.objects.get(pk = name_pk)

                    try:
                        if selected.region_name == name  and selected.fk_entity_code == entity_fk:
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:region')
                        a = master_region.objects.get(region_name= name , fk_entity_code= entity_fk, status= active_status)
                        messages.error(request, "region Already Exist")
                        return redirect('csp_app:region')
                    except ObjectDoesNotExist:
                        selected.region_name = name 
                        selected.fk_entity_code =entity_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "Region Updated Successfully")
                        return redirect('csp_app:region')
                else:
                    messages.warning(request, "Region Name Cannot Be Blank")
                    return redirect('csp_app:region')         
           
        return render(request, 'csp_app/editregion.html', {'r_list': created_by_region(),'zone_list': zone_list, 'allcandidates': all_active_candidates,'view_region_list': region, 'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  




@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def state(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
    function_list = master_function.objects.filter(status = active_status).order_by('function_name')
    team_list = master_team.objects.filter(status = active_status).order_by('team_name')
    subteam_list = master_sub_team.objects.filter(status = active_status).order_by('sub_team_name')
    desg_list = master_designation.objects.filter(status = active_status).order_by('designation_name')
    region_list = master_region.objects.filter(status = active_status).order_by('region_name')
    state_list = master_state.objects.filter(status = active_status).order_by('state_name')
    dbstates = states.objects.all()
    return render(request, 'csp_app/state.html', { 's_list': created_by_state(),'states': dbstates, 'allcandidates': all_active_candidates,'entity_list': entity_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_state(request):
    if request.method == 'POST':
        
        state_pk = request.POST.get("state_name")
        region = request.POST.get("state_region")
        if region == None or region == '':
            messages.warning(request, "Choose Region And Try Again")
            return redirect('csp_app:state')
        if state_pk == None or state_pk == '':
            messages.warning(request, "State Cannot Be Blank")
            return redirect('csp_app:state')
        entity = request.POST.get("state_entity")
        if entity == None or entity == '':
            messages.warning(request, "Company Cannot Be Blank")
            return redirect('csp_app:state')
        entity_fk = master_entity.objects.get(pk=entity)
        zone_fk = zones.objects.get(zone_name= region)
        region_fk = master_region.objects.get(region_name = zone_fk.pk, fk_entity_code= entity_fk, status=active_status)
        state_name = states.objects.get(pk = state_pk)
        try:
            dup_region = master_state.objects.get( state_name= state_name , fk_region_code =region_fk,status = active_status)

            messages.error(request, "State Already Exist")
            return redirect('csp_app:state')
        except ObjectDoesNotExist: 
            new_state = master_state( state_name= state_name , fk_region_code =region_fk, created_by = str(request.user), created_date_time= datetime.now())
            new_state.save()
            messages.success(request, "State Saved Successfully")
            return redirect('csp_app:state')
    return render(request, 'csp_app/state.html', {'s_list': created_by_state(),'allcandidates': all_active_candidates,})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_state(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    state_list = master_state.objects.filter(status=active_status)
    dbstates = states.objects.all()
    try:
        if request.method == 'POST':
            state_id = request.POST.get("view_id")
            view_state_list = master_state.objects.filter(pk = state_id)
        return render(request, 'csp_app/viewstate.html', {'s_list': created_by_state(), 'states':dbstates, 'allcandidates': all_active_candidates,'view_state_list': view_state_list,'state_list': state_list, 'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_state(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    state_list = master_state.objects.filter(status=active_status)
    dbstates = states.objects.all()
    
    try:
        if request.method == 'POST':
            state_id = request.POST.get("view_id")
            selected = master_state.objects.filter(pk = state_id)        
        return render(request, 'csp_app/editstate.html', {'s_list': created_by_state(), 'states':dbstates, 'allcandidates': all_active_candidates,'view_state_list': selected, 'state_list': state_list,'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_state(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    state_list = master_state.objects.filter(status=active_status)
    dbstates = states.objects.all()
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_state.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_state_name") != None:
                    name_pk = request.POST.get("e_state_name")
                    region = request.POST.get("e_state_dept")
                    # entity = request.POST.get("e_state_entity")
                    if region == None or region == '':
                        messages.warning(request, "Choose region and Try Again")
                        return redirect('csp_app:state')
                    entity = request.POST.get("e_state_entity")
                    if entity == None or entity == '':
                        messages.warning(request, "Company Cannot Be Blank")
                        return redirect('csp_app:state')
                    entity_fk = master_entity.objects.get(pk=entity)
                    zone_fk = zones.objects.get(zone_name= region)
                    region_fk = master_region.objects.get(region_name = zone_fk.pk, fk_entity_code= entity_fk, status=active_status)
      
                    name = states.objects.get(pk = name_pk)

                    try:
                        if selected.state_name == name  and selected.fk_region_code == region_fk:
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:state')
                        a = master_state.objects.get(state_name= name , fk_region_code= region_fk, status= active_status)
                        messages.error(request, "state Already Exist")
                        return redirect('csp_app:state')
                    except ObjectDoesNotExist:
                        selected.state_name = name 
                        selected.fk_region_code = region_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "state Updated Successfully")
                        return redirect('csp_app:state')
                else:
                    messages.warning(request, "region Name Cannot Be Blank")
                    return redirect('csp_app:region')         
           
        return render(request, 'csp_app/editstate.html', {'s_list': created_by_state(),'states':dbstates, 'allcandidates': all_active_candidates,'view_region_list': region, 'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_state(request):
    try:
        if request.method == 'POST':
            state_id = request.POST.get("delete_id")
            state_t = master_city.objects.filter(fk_state_code=state_id, status=active_status)
            state_c = master_candidate.objects.filter(fk_state_code=state_id, status=active_status)
            if len(state_t) >= 1 or len(state_c) >= 1:
                messages.error(request, "state Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:state')
            else:
                selected = master_state.objects.get(pk = state_id, status= active_status)
                selected.status = deactive_status
                selected.modified_by = str(request.user)
                selected.modified_date_time = datetime.now()
                selected.save()
                messages.success(request, "state Deleted Successfully")
                return redirect('csp_app:state')
        return render(request, 'csp_app/state.html', {'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")





@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  city(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status = active_status).order_by('region_name')
    state_list = master_state.objects.filter(status = active_status).order_by('state_name')
    city_list = master_city.objects.filter(status= active_status).order_by('city_name')
    return render(request, 'csp_app/city.html', {'c_list': created_by_city(),'allcandidates': all_active_candidates,'entity_list': entity_list, 'city_list': city_list, 'state_list':state_list, 'region_list': region_list})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_city(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    city_list = master_city.objects.filter(status=active_status)

    try:
        if request.method == 'POST':
            city_id = request.POST.get("view_id")
            view_city_list = master_city.objects.filter(pk = city_id)
        return render(request, 'csp_app/viewcity.html', {'c_list': created_by_city(),'allcandidates': all_active_candidates,'view_city_list': view_city_list,'city_list': city_list, 'function_list': function_list,'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_city(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    function_list = master_function.objects.filter(status=active_status)
    city_list = master_city.objects.filter(status=active_status)

    try:
        if request.method == 'POST':
            city_id = request.POST.get("view_id")
            selected = master_city.objects.filter(pk = city_id)        
        return render(request, 'csp_app/editcity.html', {'c_list': created_by_city(),'allcandidates': all_active_candidates,'view_city_list': selected,'city_list': city_list, 'function_list': function_list,'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_city(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    state_list = master_state.objects.filter(status=active_status)
    city_list = master_city.objects.filter(status=active_status)
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_city.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_city_name") != None:
                    name = request.POST.get("e_city_name")
                    function = request.POST.get("e_city_state")
                    # entity = request.POST.get("e_function_entity")
                    # print(region)
                    if function == None or function == '':
                        messages.warning(request, "Choose State and Try Again")
                        return redirect('csp_app:city')
                    state_fk = master_state.objects.get(pk = function)
                    try:
                        if selected.city_name == name  and selected.fk_state_code == state_fk:
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:city')
                        a = master_city.objects.get(city_name= name , fk_state_code= state_fk, status= active_status)
                        messages.error(request, "city Already Exist")
                        return redirect('csp_app:city')
                    except ObjectDoesNotExist:
                        selected.city_name = name 
                        selected.fk_state_code = state_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "city Updated Successfully")
                        return redirect('csp_app:city')
                else:
                    messages.warning(request, "City Name Cannot Be Blank")
                    return redirect('csp_app:city')         
           
        return render(request, 'csp_app/editcity.html', {'c_list': created_by_city(),'allcandidates': all_active_candidates,'view_city_list': selected,'state_list': state_list, 'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_city(request):
    try:
        if request.method == 'POST':
            city_id = request.POST.get("delete_id")
            city_t = master_location.objects.filter(fk_city_code=city_id, status=active_status)
            city_c = master_candidate.objects.filter(fk_city_code=city_id, status=active_status)
            if len(city_t) >= 1 or len(city_c) >= 1:
                messages.error(request, "city Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:city')
            else:
                selected = master_city.objects.get(pk = city_id, status= active_status)
                selected.status = deactive_status
                selected.modified_by = str(request.user)
                selected.modified_date_time = datetime.now()
                selected.save()
                messages.success(request, "city Deleted Successfully")
                return redirect('csp_app:city')
        return render(request, 'csp_app/city.html', {'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_city(request):
    if request.method == 'POST':
        city_name = request.POST.get("city_name")
        state = request.POST.get("city_state")
        if state == None or state == '':
            messages.warning(request, "Choose State And Try Again")
            return redirect('csp_app:city')
        if city_name == None or city_name == '':
            messages.warning(request, "City Cannot Be Blank")
            return redirect('csp_app:city')
        state_fk = master_state.objects.get(pk=state)
        try:
            dup_city = master_city.objects.get( city_name= city_name , fk_state_code =state_fk,status = active_status)

            messages.error(request, "City Already Exist")
            return redirect('csp_app:city')
        except ObjectDoesNotExist: 
            new_city = master_city( city_name= city_name , fk_state_code =state_fk, created_by = str(request.user), created_date_time= datetime.now())
            new_city.save()
            messages.success(request, "City Saved Successfully")
            return redirect('csp_app:city')
    return render(request, 'csp_app/city.html', {'c_list': created_by_city(),'allcandidates': all_active_candidates,})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  location(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status = active_status).order_by('region_name')
    state_list = master_state.objects.filter(status = active_status).order_by('state_name')
    city_list = master_city.objects.filter(status= active_status).order_by('city_name')
    location_list = master_location.objects.filter(status= active_status).order_by('location_name')
    return render(request, 'csp_app/location.html', {'l_list': created_by_location(),'allcandidates': all_active_candidates,'entity_list': entity_list, 'location_list': location_list, 'city_list': city_list, 'state_list':state_list, 'region_list': region_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_location(request):
    if request.method == 'POST':
        location_name = request.POST.get("location_name")
        code = request.POST.get("location_code")

        city = request.POST.get("location_city")
        if city == None or city == '':
            messages.warning(request, "Choose City And Try Again")
            return redirect('csp_app:location')
        if location_name == None or location_name == '':
            messages.warning(request, "Location Name Cannot Be Blank")
            return redirect('csp_app:location')
        if code == None or code == '':
            messages.warning(request, "Location Code Cannot Be Blank")
            return redirect('csp_app:location')
        city_fk = master_city.objects.get(pk=city)
        try:
            dup_location = master_location.objects.get(location_name= location_name , fk_city_code =city_fk,location_code= code, status = active_status)

            messages.error(request, "Location Already Exist")
            return redirect('csp_app:location')
        except ObjectDoesNotExist: 
            new_location = master_location( location_name= location_name ,location_code=code, fk_city_code =city_fk, created_by = str(request.user), created_date_time= datetime.now())
            new_location.save()
            messages.success(request, "Location Saved Successfully")
            return redirect('csp_app:location')
    return render(request, 'csp_app/location.html', {'l_list': created_by_location(),'allcandidates': all_active_candidates,})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_location(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    state_list = master_state.objects.filter(status=active_status)
    city_list = master_city.objects.filter(status=active_status)
    location_list = master_location.objects.filter(status=active_status)

    try:
        if request.method == 'POST':
            location_id = request.POST.get("view_id")
            view_location_list = master_location.objects.filter(pk = location_id)
        return render(request, 'csp_app/viewlocation.html', {'l_list': created_by_location(),'allcandidates': all_active_candidates,'view_location_list': view_location_list,'location_list': location_list, 'city_list': city_list, 'state_list': state_list,'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_location(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    state_list = master_state.objects.filter(status=active_status)
    city_list = master_city.objects.filter(status=active_status)
    location_list = master_location.objects.filter(status=active_status)

    try:
        if request.method == 'POST':
            location_id = request.POST.get("view_id")
            selected = master_location.objects.filter(pk = location_id)        
        return render(request, 'csp_app/editlocation.html', {'l_list': created_by_location(),'allcandidates': all_active_candidates,'view_location_list': selected,'location_list': location_list, 'city_list': city_list, 'state_list': state_list,'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_location(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    state_list = master_state.objects.filter(status=active_status)
    city_list = master_city.objects.filter(status=active_status)
    location_list = master_location.objects.filter(status=active_status)

    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_location.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_location_name") != None:
                    name = request.POST.get("e_location_name")
                    code = request.POST.get("e_location_code")
                    city = request.POST.get("e_location_city")
                    # entity = request.POST.get("e_state_entity")
                    # print(region)

                    if city == None or city == '':
                        messages.warning(request, "Choose city and Try Again")
                        return redirect('csp_app:location')
                    city_fk = master_city.objects.get(pk = city)
                    try:
                        a = master_location.objects.get(location_name= name, location_code= code, fk_city_code= city_fk, status= active_status)
                        messages.error(request, "Location Already Exist")
                        return redirect('csp_app:location')
                        if selected.location_name == name  and selected.fk_city_code == city_fk:
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:location')
                        
                    except ObjectDoesNotExist:
                        selected.location_name = name 
                        selected.location_code = code 

                        selected.fk_city_code = city_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "Location Updated Successfully")
                        return redirect('csp_app:location')
                else:
                    messages.warning(request, "Location Name Cannot Be Blank")
                    return redirect('csp_app:location')         
           
        return render(request, 'csp_app/editlocation.html', {'l_list': created_by_location(),'allcandidates': all_active_candidates,'view_location_list': selected,'city_list': city_list, 'state_list': state_list, 'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_location(request):
    try:
        if request.method == 'POST':
            loc_id = request.POST.get("delete_id")
            loc_c = master_candidate.objects.filter(fk_location_code= loc_id, status=active_status)
            if len(loc_c) >= 1:
                messages.error(request, "Location Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:location')
            else:
                selected = master_location.objects.get(pk = loc_id, status= active_status)
                selected.status = deactive_status
                selected.modified_by = str(request.user)
                selected.modified_date_time = datetime.now()
                selected.save()
                messages.success(request, "Location Deleted Successfully")
                return redirect('csp_app:location')
        return render(request, 'csp_app/location.html', {'allcandidates': all_active_candidates,})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")





@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_user_view(request):
    user_list = User.objects.all().exclude(is_superuser=True)
    
    group_list = Group.objects.all().exclude(name='Candidate')    
    return render(request, 'csp_app/create_user.html', {'allcandidates': all_active_candidates,'user_list': user_list, 'group_list': group_list})



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_user(request):
    if request.method == 'POST':
        usrname = request.POST.get('email')
        firstname = request.POST.get('firstname').capitalize()
        lastname = request.POST.get('lastname').capitalize()
        email = request.POST.get('email')
        group = request.POST.get('usergroup')
        try:               
            assign_group = Group.objects.get(name=group) 
            if assign_group.name == 'Onboarding SPOC':
                try:
                    a = User.objects.get(groups__name='Onboarding SPOC', is_active=True)
                    messages.error(request, "Only One Onboarding SPOC Can Be Created.")
                    return redirect('csp_app:user')
                except ObjectDoesNotExist:
                    pass
            password = User.objects.make_random_password()
            assign_group = Group.objects.get(name=group) 
            
            user = User.objects.create_user(usrname)
            password = User.objects.make_random_password()
            user.password = password
            user.set_password(user.password)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            if group == 'Admin':
                user.is_staff = True
            # user.groups = group
            
            assign_group.user_set.add(user)
            user.save()
            template = render_to_string('emailtemplates/new_user_et.html', {'user': firstname ,'username': email, 'password': password})
            our_email = EmailMessage(
                'Account Created with UDAAN CSP_APP.',
                template,
                settings.EMAIL_HOST_USER,
                [ email, 'sadaf.shaikh@udaan.com'],
            ) 
            our_email.fail_silently = False
            our_email.send()
            admintemplate = render_to_string('emailtemplates/new_user_admin_et.html', {'user': firstname ,'username': email, 'password': password})
            our_email = EmailMessage(
                'Account Created with UDAAN CSP_APP.',
                admintemplate,
                settings.EMAIL_HOST_USER,
                [ request.user.email , 'sadaf.shaikh@udaan.com'],
            ) 
            our_email.fail_silently = False
            our_email.send()
            # msg = 'User account of type " ' + group +' " created with Username " ' + usrname + '" and  Password " ' + password + '" " ."'
            # send_mail('New User Account Created', msg,'workmail052020@gmail.com',[ email, 'sadaf.shaikh@udaan.com', 'rahul.gandhi@udaan.com'],fail_silently=False)
            # print("after")
            # return HttpResponse("success")
            messages.success(request, "User Created Successfully")
            return redirect('csp_app:user')
        except IntegrityError:
            messages.error(request, "Username Already Exist")
            return redirect('csp_app:user')
    return render(request, 'csp_app/create_user.html', {'allcandidates': all_active_candidates,})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  disable_user(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get("disable_id")
            if user_id == None or user_id == '':
                messages.warning(request, "Username Not Found")
                return redirect('csp_app:user')
            selected_user = User.objects.get(pk = user_id)
          
            if str(selected_user.username) == str(request.user):
                messages.warning(request, "Cannot Disable Self")
                return redirect('csp_app:user')
            selected_user.is_active = False
            selected_user.save()
            messages.success(request, "User Disabled")
            return redirect('csp_app:user')
        return render(request, 'csp_app/create_user.html', {'allcandidates': all_active_candidates,})        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  enable_user(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get("enable_id")
            if user_id == None or user_id == '':
                messages.warning(request, "Username Not Found")
                return redirect('csp_app:user')
            selected_user = User.objects.get(pk = user_id)
            selected_user.is_active = True
            selected_user.save()
            messages.success(request, "User Enabled")
            return redirect('csp_app:user')
        return render(request, 'csp_app/create_user.html', {'allcandidates': all_active_candidates,})        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
def  index(request):
    return HttpResponse("Hello Sdf")

@login_required(login_url='/notlogin/')
def  admin(request):
    return render(request, 'csp_app/adminhome.html', {'allcandidates': all_active_candidates,})




def csp_login(request):
    if request.method == "POST":
        if request.POST.get('username') != None or request.POST.get('username') != '':
            usrname = request.POST.get('username')
            pwd = request.POST.get('password')
            if usrname == '':
                messages.add_message(request, messages.WARNING, "Please Enter UID")
                return redirect('csp_app:login')
            elif pwd == '':
                messages.add_message(request, messages.WARNING, "Please Enter Password")
                return redirect('csp_app:login')
            user = authenticate(request, username=usrname, password=pwd)
            if user is not None and user.is_active:
                login(request, user)
                try:
                    User.objects.filter(pk=request.user.pk).update(last_login= datetime.now())
                    group = request.user.groups.all()

                    for groupname in group:
                        group_name = groupname
                    if str(group_name) == 'Admin':
                        messages.success(request, "Login Successfull")
                        return redirect('csp_app:entity')
                    elif str(group_name) == 'Vendor':
                        messages.success(request, "Login Successfull")
                        return redirect('csp_app:candidate')
                    elif str(group_name) == 'Candidate':
                        messages.success(request, "Login Successfull")
                        return redirect('csp_app:candidate_profile')   
                    else:
                        messages.success(request, "Login Successfull")
                        return redirect('csp_app:candidate')
                except UnboundLocalError:
                    messages.success(request, "Login Successfull")
                    return redirect('csp_app:rm_joined')
            else:
                messages.add_message(request, messages.ERROR, "Invalid Credentials")
                return redirect('csp_app:login')
    return render(request, 'csp_app/Login.html', {'allcandidates': all_active_candidates,})

@login_required(login_url='/notlogin/')
def  csp_logout(request):
    logout(request)
    return redirect('csp_app:login')


def notlogin(request):
    return render(request, 'csp_app/timeout.html', {'allcandidates': all_active_candidates,})

