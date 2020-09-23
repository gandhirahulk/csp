from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.db.utils import IntegrityError
from csp_app.models import status, master_candidate, master_entity, master_designation, master_vendor, master_department, \
                            master_function, master_team, master_sub_team, master_region, master_state, master_city, master_location, hiring_type, \
                            sub_source, salary_type, gender, laptop_allocation, candidate_status, onboarding_status, vendor_status, csp_candidate_code, \
                            mandatory_documents, candidate_document
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.files.storage import FileSystemStorage



deactive_status = status.objects.get(pk=2)
active_status = status.objects.get(pk=1)
pending_status = candidate_status.objects.get(pk=2)
approve_onboarding = onboarding_status.objects.get(pk = 1)
pending_onboarding = onboarding_status.objects.get(pk=2)
pending_vendor = vendor_status.objects.get(pk=2)

all_active_candidates = master_candidate.objects.filter(status=active_status)
count_it = master_candidate.objects.filter( onboarding_status= pending_onboarding)
count = len(count_it)

def vendor_candidates(usrname):
    try:
        s_vendor = master_vendor.objects.filter(vendor_email_id= usrname, status=active_status)
        vs_candidates = []
        for e in s_vendor:
            vs_candidates.append(master_candidate.objects.filter(fk_vendor_code=e.pk, status= active_status))
        return vs_candidates
    except ObjectDoesNotExist:
        pass

def vendor_pending_candidates(usrname):
    try:
        s_vendor = master_vendor.objects.filter(vendor_email_id= usrname, status=active_status)
        vs_candidates = []
        for e in s_vendor:
            vs_candidates.append(master_candidate.objects.filter(fk_vendor_code=e.pk, vendor_status= pending_vendor, status= active_status))
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
@user_passes_test(lambda u: u.groups.filter(name='Onboarding SPOC').exists() or u.groups.filter(name='Vendor').exists())
def process_requests(request, cid):    
    try:
        selected_candidate_data = master_candidate.objects.filter(pk= cid)
        # selected_candidate = ''
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
        hiring_type_list = hiring_type.objects.filter(status= active_status)
        sub_source_list = sub_source.objects.filter(status= active_status)
        salary_type_list = salary_type.objects.filter(status= active_status)
        gender_list = gender.objects.filter(status= active_status)
        laptop_allocation_list = laptop_allocation.objects.filter(status= active_status)
        c_status_list = candidate_status.objects.all()
        v_status_list = vendor_status.objects.all()
        if request.method == 'POST':
            firstname = request.POST.get("c_firstname")
            middlename = request.POST.get("c_middlename")
            lastname = request.POST.get("c_lastname")
            dob = request.POST.get("c_dob")
            contact_no = request.POST.get("c_contact")
            emergency_no = request.POST.get("c_emergency")
            email = request.POST.get("c_email")
            c_gender = request.POST.get("c_gender")
            fathername = request.POST.get("c_fathername")
            father_dob = request.POST.get("c_father_dob")
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
            loc_code = 'GGG' #check
            ta_spoc = request.POST.get("c_ta_spoc") #check
            onboarding_spoc = request.POST.get("c_onboarding_spoc") #check
            reporting_manager = request.POST.get("c_reporting_manager")
            reporting_manager_email = request.POST.get("c_reporting_manager_email")
            email_creation = request.POST.get("c_email_creation")
            laptopallocation = request.POST.get("c_laptop_allocation")
            salarytype = request.POST.get("c_salary_type")
            gross_salary = request.POST.get("c_gross_salary")
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
                messages.warning(request, "Choose  Entity Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            entity_fk = master_entity.objects.get(pk= entity)
            if vendor == None or vendor == '':
                messages.warning(request, "Choose  vendor And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            vendor_fk = master_vendor.objects.get(pk= vendor)
            if department == None or department == '':
                messages.warning(request, "Choose  Department Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            department_fk = master_department.objects.get(pk= department)
            if function == None or function == '':
                messages.warning(request, "Choose  Function Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            function_fk = master_function.objects.get(pk= function)
            if team == None or team == '':
                messages.warning(request, "Choose  Team Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            team_fk = master_team.objects.get(pk= team)
            if sub_team == None or sub_team == '':
                messages.warning(request, "Choose  Sub Team Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            sub_team_fk = master_sub_team.objects.get(pk= sub_team)
            if designation == None or designation == '':
                messages.warning(request, "Choose  Designation Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            designation_fk = master_designation.objects.get(pk= designation)
            if region == None or region == '':
                messages.warning(request, "Choose  Region Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            region_fk = master_region.objects.get(pk= region)
            if state == None or state == '':
                messages.warning(request, "Choose  State Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            state_fk = master_state.objects.get(pk= state)
            if city == None or city == '':
                messages.warning(request, "Choose  City Type And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            city_fk = master_city.objects.get(pk= city)
            if location == None or location == '':
                messages.warning(request, "Choose  Location And Try Again")
                return redirect("csp_app:process_request", cid = cid)
            location_fk = master_location.objects.get(pk= location)
            spoc_status = request.POST.get('s_status')
            try:
                dup_candidate_aadhaar = master_candidate.objects.get(Aadhaar_Number= aadhaar, status= active_status).exclude(pk=cid)
                messages.error( request, "Candidate Aadhaar Number Already Exist")
                return redirect("csp_app:process_request", cid = cid)
                dup_candidate_pan = master_candidate.objects.get(PAN_Number= Pan, status= active_status).exclude(pk=cid)
                messages.error( request, "Candidate PAN Number Already Exist")
                return redirect("csp_app:process_request", cid = cid)
                dup_candidate_pan = master_candidate.objects.get(Contact_Number= contact_no, status= active_status).exclude(pk=cid)
                messages.error( request, "Candidate Contact Number Already Exist")
                return redirect("csp_app:process_request", cid = cid)
            except ObjectDoesNotExist:
                selected_candidate = master_candidate.objects.get(pk= cid)
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
                if selected_candidate.Father_Date_of_Birth != father_dob:
                    changes_list['Father DOB'] = [ selected_candidate.Father_Date_of_Birth, father_dob ]
                selected_candidate.Father_Date_of_Birth= father_dob
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
                if selected_candidate.TA_Spoc_Email_Id != ta_spoc:
                    changes_list['TA Spoc Email Id'] = [ selected_candidate.TA_Spoc_Email_Id, ta_spoc ]
                    selected_candidate.TA_Spoc_Email_Id= ta_spoc
                if selected_candidate.Onboarding_Spoc_Email_Id != onboarding_spoc:
                    changes_list['Onboarding Spoc Email Id'] = [ selected_candidate.Onboarding_Spoc_Email_Id, onboarding_spoc ]
                    selected_candidate.Onboarding_Spoc_Email_Id= onboarding_spoc
                if selected_candidate.Laptop_Allocation != la_fk:
                    changes_list['Laptop Allocation'] = [ selected_candidate.Laptop_Allocation, la_fk ]
                    selected_candidate.Laptop_Allocation= la_fk
                if selected_candidate.Salary_Type != salarytype_fk:
                    changes_list['Salary Type'] = [ selected_candidate.Salary_Type, salarytype ]
                    selected_candidate.Salary_Type= salarytype_fk
                if selected_candidate.Gross_Salary_Amount != gross_salary:
                    changes_list['Gross Salary Amount'] = [ selected_candidate.Gross_Salary_Amount, gross_salary ]
                    selected_candidate.Gross_Salary_Amount= gross_salary
                selected_candidate.modified_by = str(request.user)
                if selected_candidate.onboarding_status != approve_onboarding:
                    changes_list['Onboarding Status'] = [ selected_candidate.onboarding_status, approve_onboarding ]
                    selected_candidate.onboarding_status = approve_onboarding
                selected_candidate.modified_date_time=datetime.now()
                selected_candidate.save()
                
                limtemplate = render_to_string('csp_app/candidate_edited_by_onboarding_et.html', {'candidate_code':new_code ,'user': request.user, 'vendor': vendor_fk.vendor_name })
                our_email = EmailMessage(
                    'Candidate Edited .',
                    limtemplate,
                    settings.EMAIL_HOST_USER,
                    [ vendor_fk.vendor_email_id , 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()
                
                alltemplate = render_to_string('csp_app/candidate_edited_by_onboarding_admin_et.html', {'candidate_code':new_code ,'user': request.user, 'changes': changes_list})
                our_email = EmailMessage(
                    'Candidate account created action required.',
                    alltemplate,
                    settings.EMAIL_HOST_USER,
                    [ 'sadaf.shaikh@udaan.com', 'workmail052020@gmail.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()
                
                messages.success(request, "Candidate details mailed to vendor.")
                return redirect("csp_app:process_request", cid = cid)


        return render(request, 'csp_app/processrequests.html', {'selected_candidate': selected_candidate_data, 'count': count, 'allcandidates': all_active_candidates,'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
        'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
        'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
        'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
        'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Onboarding SPOC').exists() or u.groups.filter(name='Vendor').exists())
def pending_requests(request):    
    try:
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
        hiring_type_list = hiring_type.objects.filter(status= active_status)
        sub_source_list = sub_source.objects.filter(status= active_status)
        salary_type_list = salary_type.objects.filter(status= active_status)
        gender_list = gender.objects.filter(status= active_status)
        laptop_allocation_list = laptop_allocation.objects.filter(status= active_status)
        try:
            specific_vendor = master_vendor.objects.filter(vendor_email_id= request.user, status=active_status)
            vendor_specific_candidate = []
            for e in specific_vendor:
                vendor_specific_candidate.append(master_candidate.objects.filter(fk_vendor_code=e.pk, onboarding_status= approve_onboarding))
     
        except ObjectDoesNotExist:
            specific_vendor = ''
            vendor_specific_candidate = []
        for eachgroup in request.user.groups.all():
            if str(eachgroup) == 'Onboarding SPOC':
                candidate_list = onboarding_candidates(request.user)
                all_active_candidates = onboarding_candidates(request.user)
                pending_candidate_list = onboarding_pending_candidates(request.user)
                count = len(pending_candidate_list)
            else:
                candidate_list = vendor_specific_candidate
                all_active_candidates = vendor_candidates(request.user)
                pending_candidate_list = vendor_pending_candidates(request.user)
                count = len(pending_candidate_list)
        return render(request, 'csp_app/pendingrequests.html', {'count':count,'pending_candidate_list': pending_candidate_list, 'allcandidates': all_active_candidates,'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
        'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
        'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
        'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
        'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'candidate_list': candidate_list })
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")




@login_required(login_url='/notlogin/')
def candidate(request):
    
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
    hiring_type_list = hiring_type.objects.filter(status= active_status)
    sub_source_list = sub_source.objects.filter(status= active_status)
    salary_type_list = salary_type.objects.filter(status= active_status)
    gender_list = gender.objects.filter(status= active_status)
    laptop_allocation_list = laptop_allocation.objects.filter(status= active_status)
    c_status_list = candidate_status.objects.all()
    v_status_list = vendor_status.objects.all()
    try:
        specific_vendor = master_vendor.objects.filter(vendor_email_id= request.user, status=active_status)
        vendor_specific_candidate = []
        for e in specific_vendor:
            vendor_specific_candidate.append(master_candidate.objects.filter(fk_vendor_code=e.pk, onboarding_status= approve_onboarding))
     
    except ObjectDoesNotExist:
        specific_vendor = ''
        vendor_specific_candidate = []
    for eachgroup in request.user.groups.all():
        if str(eachgroup) == 'Vendor':
            candidate_list = vendor_specific_candidate
            all_active_candidates = vendor_candidates(request.user)
            count = len(candidate_list)
        elif str(eachgroup) == 'Onboarding SPOC':
            candidate_list = onboarding_candidates(request.user)
            all_active_candidates = onboarding_candidates(request.user)
            pending_candidate_list = onboarding_pending_candidates(request.user)
            count = len(pending_candidate_list)
        
    return render(request, 'csp_app/candidates.html', {'count': count, 'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
    'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
    'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
    'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 'c_status_list': c_status_list,
    'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'candidate_list': candidate_list, 'v_status_list': v_status_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='User').exists())
def new_candidate(request):    
    try:
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
        hiring_type_list = hiring_type.objects.filter(status= active_status)
        sub_source_list = sub_source.objects.filter(status= active_status)
        salary_type_list = salary_type.objects.filter(status= active_status)
        gender_list = gender.objects.filter(status= active_status)
        laptop_allocation_list = laptop_allocation.objects.filter(status= active_status)
        candidate_list = master_candidate.objects.all()
        return render(request, 'csp_app/newcandidate.html', {'allcandidates': all_active_candidates,'allcandidates': all_active_candidates, 'entity_list': entity_list, 'location_list': location_list, 
        'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
        'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
        'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
        'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'candidate_list': candidate_list })
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='User').exists() )
def edit_candidate(request): 
    try:
        if request.method == 'POST':
            candidate_id = request.POST.get("view_id")   
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
            hiring_type_list = hiring_type.objects.filter(status= active_status)
            sub_source_list = sub_source.objects.filter(status= active_status)
            salary_type_list = salary_type.objects.filter(status= active_status)
            gender_list = gender.objects.filter(status= active_status)
            laptop_allocation_list = laptop_allocation.objects.filter(status= active_status)
            candidate_list = master_candidate.objects.filter(pk=candidate_id)
            if request.POST.get('c_id') != '':
                cid = request.POST.get('c_id')
                firstname = request.POST.get("c_firstname")
                middlename = request.POST.get("c_middlename")
                lastname = request.POST.get("c_lastname")
                dob = request.POST.get("c_dob")
                contact_no = request.POST.get("c_contact")
                emergency_no = request.POST.get("c_emergency")
                email = request.POST.get("c_email")
                c_gender = request.POST.get("c_gender")
                fathername = request.POST.get("c_fathername")
                father_dob = request.POST.get("c_father_dob")
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
                loc_code = 'GGG' #check

                ta_spoc = request.POST.get("c_ta_spoc") #check
                onboarding_spoc = request.POST.get("c_onboarding_spoc") #check
                reporting_manager = request.POST.get("c_reporting_manager")
                reporting_manager_email = request.POST.get("c_reporting_manager_email")
                email_creation = request.POST.get("c_email_creation")
                laptopallocation = request.POST.get("c_laptop_allocation")
                salarytype = request.POST.get("c_salary_type")
                gross_salary = request.POST.get("c_gross_salary")
                if hiring == None or hiring == '':
                    messages.warning(request, "Choose Hiring Type And Try Again")
                    return redirect("csp_app:candidate")
                hiring_fk = hiring_type.objects.get(pk= hiring)
                if sub_source == None or sub_source == '':
                    messages.warning(request, "Choose  Sub Source Type And Try Again")
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
                    messages.warning(request, "Choose  Entity Type And Try Again")
                    return redirect("csp_app:candidate")
                entity_fk = master_entity.objects.get(pk= entity)
                if vendor == None or vendor == '':
                    messages.warning(request, "Choose  vendor Type And Try Again")
                    return redirect("csp_app:candidate")
                vendor_fk = master_vendor.objects.get(pk= vendor)
                if department == None or department == '':
                    messages.warning(request, "Choose  Department Type And Try Again")
                    return redirect("csp_app:candidate")
                department_fk = master_department.objects.get(pk= department)
                if function == None or function == '':
                    messages.warning(request, "Choose  Function Type And Try Again")
                    return redirect("csp_app:candidate")
                function_fk = master_function.objects.get(pk= function)
                if team == None or team == '':
                    messages.warning(request, "Choose  Team Type And Try Again")
                    return redirect("csp_app:candidate")
                team_fk = master_team.objects.get(pk= team)
                if sub_team == None or sub_team == '':
                    messages.warning(request, "Choose  Sub Team Type And Try Again")
                    return redirect("csp_app:candidate")
                sub_team_fk = master_sub_team.objects.get(pk= sub_team)
                if designation == None or designation == '':
                    messages.warning(request, "Choose  Designation Type And Try Again")
                    return redirect("csp_app:candidate")
                designation_fk = master_designation.objects.get(pk= designation)
                if region == None or region == '':
                    messages.warning(request, "Choose  Region Type And Try Again")
                    return redirect("csp_app:candidate")
                region_fk = master_region.objects.get(pk= region)
                if state == None or state == '':
                    messages.warning(request, "Choose  State Type And Try Again")
                    return redirect("csp_app:candidate")
                state_fk = master_state.objects.get(pk= state)
                if city == None or city == '':
                    messages.warning(request, "Choose  City Type And Try Again")
                    return redirect("csp_app:candidate")
                city_fk = master_city.objects.get(pk= city)
                if location == None or location == '':
                    messages.warning(request, "Choose  Location Type And Try Again")
                    return redirect("csp_app:candidate")
                location_fk = master_location.objects.get(pk= location)
                selected_candidate = master_candidate.objects.get(pk = cid)
                selected_candidate.First_Name=firstname
                selected_candidate.Middle_Name=middlename
                selected_candidate.Last_Name= lastname
                selected_candidate.Date_of_Joining= doj
                selected_candidate.Date_of_Birth= dob
                selected_candidate.Father_Name= fathername
                selected_candidate.Father_Date_of_Birth= father_dob
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
                selected_candidate.location_code= loc_code,
                selected_candidate.Reporting_Manager= reporting_manager
                selected_candidate.Reporting_Manager_E_Mail_ID= reporting_manager_email
                selected_candidate.Gender= gender_fk 
                selected_candidate.E_Mail_ID_Creation= email_creation
                selected_candidate.TA_Spoc_Email_Id= ta_spoc
                selected_candidate.Onboarding_Spoc_Email_Id= onboarding_spoc
                selected_candidate.Laptop_Allocation= la_fk
                selected_candidate.Salary_Type= salarytype_fk
                selected_candidate.Gross_Salary_Amount= gross_salary
                selected_candidate.modified_by = str(request.user)
                selected_candidate.modified_date_time=datetime.now()
                alltemplate = render_to_string('csp_app/candidate_edited_et.html', {'candidate_code':new_code ,'user': request.user})
                our_email = EmailMessage(
                    'Candidate Account Updated.',
                    alltemplate,
                    settings.EMAIL_HOST_USER,
                    [ ta_spoc, onboarding_spoc, 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()
                limtemplate = render_to_string('csp_app/candidate_edited_et_limited.html', {'candidate_code':new_code ,'user': request.user})
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

        return render(request, 'csp_app/editcandidate.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'location_list': location_list, 
        'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
        'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
        'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
        'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'selected_candidate': candidate_list })
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

# @login_required(login_url='/notlogin/')
# def candidate_document(request, cid): 
#     if request.method != 'POST':
#         candidate_id = request.POST.get("view_id")   
#         entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
#         vendor_list = master_vendor.objects.filter(status = active_status).order_by('vendor_name')
#         dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
#         function_list = master_function.objects.filter(status = active_status).order_by('function_name')
#         team_list = master_team.objects.filter(status = active_status).order_by('team_name')
#         subteam_list = master_sub_team.objects.filter(status = active_status).order_by('sub_team_name')
#         desg_list = master_designation.objects.filter(status = active_status).order_by('designation_name')
#         region_list = master_region.objects.filter(status = active_status).order_by('region_name')
#         state_list = master_state.objects.filter(status = active_status).order_by('state_name')
#         city_list = master_city.objects.filter(status= active_status).order_by('city_name')
#         location_list = master_location.objects.filter(status= active_status).order_by('location_name')
#         hiring_type_list = hiring_type.objects.filter(status= active_status)
#         sub_source_list = sub_source.objects.filter(status= active_status)
#         salary_type_list = salary_type.objects.filter(status= active_status)
#         gender_list = gender.objects.filter(status= active_status)
#         laptop_allocation_list = laptop_allocation.objects.filter(status= active_status)
#         view_candidate = master_candidate.objects.filter(pk=cid)
#     return render(request, 'csp_app/document.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'location_list': location_list, 
#     'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
#     'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
#     'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
#     'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'view_candidate': candidate_list })


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists() or u.groups.filter(name='User').exists())
def create_candidate(request):
    try:
        if request.method == 'POST':

            firstname = request.POST.get("c_firstname")
            middlename = request.POST.get("c_middlename")
            lastname = request.POST.get("c_lastname")
            dob = request.POST.get("c_dob")
            contact_no = request.POST.get("c_contact")
            emergency_no = request.POST.get("c_emergency")
            email = request.POST.get("c_email")
            c_gender = request.POST.get("c_gender")
            fathername = request.POST.get("c_fathername")
            father_dob = request.POST.get("c_father_dob")
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
            loc_code = 'GGG' #check

            ta_spoc = request.POST.get("c_ta_spoc") #check
            onboarding_spoc = request.POST.get("c_onboarding_spoc") #check
            reporting_manager = request.POST.get("c_reporting_manager")
            reporting_manager_email = request.POST.get("c_reporting_manager_email")
            email_creation = request.POST.get("c_email_creation")
            laptopallocation = request.POST.get("c_laptop_allocation")
            salarytype = request.POST.get("c_salary_type")
            gross_salary = request.POST.get("c_gross_salary")
            if hiring == None or hiring == '':
                messages.warning(request, "Choose Hiring Type And Try Again")
                return redirect("csp_app:new_candidate")
            hiring_fk = hiring_type.objects.get(pk= hiring)
            if sub_source == None or sub_source == '':
                messages.warning(request, "Choose  Sub Source Type And Try Again")
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
                messages.warning(request, "Choose  Entity Type And Try Again")
                return redirect("csp_app:new_candidate")
            entity_fk = master_entity.objects.get(pk= entity)
            if vendor == None or vendor == '':
                messages.warning(request, "Choose  vendor And Try Again")
                return redirect("csp_app:new_candidate")
            vendor_fk = master_vendor.objects.get(pk= vendor)
            if department == None or department == '':
                messages.warning(request, "Choose  Department Type And Try Again")
                return redirect("csp_app:new_candidate")
            department_fk = master_department.objects.get(pk= department)
            if function == None or function == '':
                messages.warning(request, "Choose  Function Type And Try Again")
                return redirect("csp_app:new_candidate")
            function_fk = master_function.objects.get(pk= function)
            if team == None or team == '':
                messages.warning(request, "Choose  Team Type And Try Again")
                return redirect("csp_app:new_candidate")
            team_fk = master_team.objects.get(pk= team)
            if sub_team == None or sub_team == '':
                messages.warning(request, "Choose  Sub Team Type And Try Again")
                return redirect("csp_app:new_candidate")
            sub_team_fk = master_sub_team.objects.get(pk= sub_team)
            if designation == None or designation == '':
                messages.warning(request, "Choose  Designation Type And Try Again")
                return redirect("csp_app:new_candidate")
            designation_fk = master_designation.objects.get(pk= designation)
            if region == None or region == '':
                messages.warning(request, "Choose  Region Type And Try Again")
                return redirect("csp_app:new_candidate")
            region_fk = master_region.objects.get(pk= region)
            if state == None or state == '':
                messages.warning(request, "Choose  State Type And Try Again")
                return redirect("csp_app:new_candidate")
            state_fk = master_state.objects.get(pk= state)
            if city == None or city == '':
                messages.warning(request, "Choose  City Type And Try Again")
                return redirect("csp_app:new_candidate")
            city_fk = master_city.objects.get(pk= city)
            if location == None or location == '':
                messages.warning(request, "Choose  Location Type And Try Again")
                return redirect("csp_app:new_candidate")
            location_fk = master_location.objects.get(pk= location)
            try:
                dup_candidate_aadhaar = master_candidate.objects.get(Aadhaar_Number= aadhaar, status= active_status)
                messages.error( request, "Candidate Aadhaar Number Already Exist")
                return redirect("csp_app:new_candidate")
                dup_candidate_pan = master_candidate.objects.get(PAN_Number= Pan, status= active_status)
                messages.error( request, "Candidate PAN Number Already Exist")
                return redirect("csp_app:new_candidate")
                dup_candidate_pan = master_candidate.objects.get(Contact_Number= contact_no, status= active_status)
                messages.error( request, "Candidate Contact Number Already Exist")
                return redirect("csp_app:new_candidate")
            except ObjectDoesNotExist:
                # try:
                last_code_query = csp_candidate_code.objects.latest('candidate_code')
                
                last_code_str = last_code_query.candidate_code
                next_code_int = int(last_code_str[1:]) + 1
                new_code = 'C' + str(next_code_int).zfill(9) #pk_candidate_code
                print(new_code)
                new_candidate = master_candidate(pk_candidate_code=new_code, First_Name=firstname , Middle_Name=middlename , Last_Name= lastname , Date_of_Joining= doj, Date_of_Birth= dob, Father_Name= fathername, Father_Date_of_Birth= dob,
                Aadhaar_Number= aadhaar, PAN_Number= Pan, Contact_Number= contact_no, Emergency_Contact_Number= emergency_no, Type_of_Hiring= hiring_fk, Replacement= replacement , Personal_Email_Id= email,
                Sub_Source= subsource_fk, Referral= referral , fk_vendor_code= vendor_fk, fk_entity_code= entity_fk, fk_department_code= department_fk, fk_function_code= function_fk, 
                fk_team_code= team_fk, fk_subteam_code= sub_team_fk, fk_designation_code= designation_fk, fk_region_code= region_fk, fk_state_code= state_fk, fk_city_code= city_fk, fk_location_code= location_fk, location_code= loc_code,
                Reporting_Manager= reporting_manager , Reporting_Manager_E_Mail_ID= reporting_manager_email, Gender= gender_fk, E_Mail_ID_Creation= email_creation, TA_Spoc_Email_Id= ta_spoc, Onboarding_Spoc_Email_Id= onboarding_spoc,
                Laptop_Allocation= la_fk, Salary_Type= salarytype_fk, Gross_Salary_Amount= gross_salary, created_by = str(request.user), candidate_status=pending_status, created_date_time=datetime.now())
                new_candidate.save()
                save_new_code = csp_candidate_code(candidate_code= new_code)
                save_new_code.save()
                limtemplate = render_to_string('csp_app/candidate_saved_et_limited.html', {'candidate_code':new_code ,'user': request.user})
                our_email = EmailMessage(
                    'Candidate account created action required.',
                    limtemplate,
                    settings.EMAIL_HOST_USER,
                    [ reporting_manager_email, 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()
                alltemplate = render_to_string('csp_app/candidate_saved_et_all.html', {'candidate_code':new_code ,'user': request.user})
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

            return render(request, 'csp_app/candidates.html', {'allcandidates': all_active_candidates,})

    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_candidate(request):
    candidate_list = master_candidate.objects.filter(status = active_status)
    try:
        if request.method == 'POST':
            candidate_id = request.POST.get("view_id")
            view_candidate_list = master_candidate.objects.filter(pk = candidate_id)
        return render(request, 'csp_app/viewcandidate.html', {'allcandidates': all_active_candidates,'view_candidate_list': view_candidate_list, 'candidate_list': candidate_list})
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
                template = render_to_string('csp_app/hold_status_change_et.html', {'allcandidates': all_active_candidates, 'candidatecode':candidate.pk ,'prev_status':prev_status, 'newstatus':status.status_name , 'user': request.user})
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
            template = render_to_string('csp_app/status_change_email_temlate.html', {'allcandidates': all_active_candidates, 'candidatecode':candidate.pk ,'prev_status':prev_status, 'newstatus':status.status_name , 'user': request.user})
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
        return render(request, 'csp_app/candidates.html', {'allcandidates': all_active_candidates,'candidate_list': candidate_list })        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Vendor').exists())
def candidate_document_upload(request, candidate_id):
    try:
        # candidate_id = 'C000000006'

        candidate = master_candidate.objects.filter(pk = candidate_id)
        candidate_fk = master_candidate.objects.get(pk = candidate_id)
        
        document_list = candidate_document.objects.filter(fk_candidate_code= candidate_fk, status=active_status)
        
        mandatory_list = mandatory_documents.objects.all()
        if request.method == 'POST':
            f_catogory = request.POST.get("c_catogory")
            print(f_catogory)
            file_name = request.POST.get("c_filename")
            print(file_name)
            c_file = request.FILES['file']
            # if file_catogory == None or file_catogory == '':
            #     messages.warning(request, "Choose File Catogory")
            #     return redirect('csp_app:document_upload')
            if c_file == None or c_file == '':
                messages.warning(request, "Choose File")
                return redirect('csp_app:document_upload')
            file_name = c_file.name
            fs = FileSystemStorage()
            filename = fs.save(file_name, c_file)
            print(fs.url(filename))
            file_url = fs.url(filename)          
            catogory_fk = mandatory_documents.objects.get(pk = f_catogory)
            try:
                duplicate_doc = candidate_document.objects.get(file_name=file_name, file_upload = c_file, fk_candidate_code= candidate_fk, status = active_status)
                messages.error(request, "Duplicate File Name")
                return redirect('csp_app:document_upload', candidate_id = candidate_id )
            except ObjectDoesNotExist:
                new_document = candidate_document(fk_candidate_code= candidate_fk, document_catagory= catogory_fk , file_name= filename, file_upload = file_url, created_by= request.user)
                new_document.save()
                messages.success(request, "Duplicate Saved Successfully")
                return redirect('csp_app:document_upload', candidate_id = candidate_id)
        all_active_candidates = vendor_candidates(request.user)
        return render(request, 'csp_app/candidatedocuments.html', {'allcandidates': all_active_candidates, 'view_candidate': candidate, 'mandatory_list': mandatory_list, 'document_list': document_list })        

    except UnboundLocalError:
        return HttpResponse("No Data To Display.")


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Vendor').exists())
def delete_document(request):
    try:
        if request.method == 'POST':
            document_id = request.POST.get("delete_id")          
            selected_document = candidate_document.objects.get(pk = document_id, status= active_status)
            selected_document.modified_by = str(request.user)
            selected_document.modified_date_time = datetime.now()
            selected_document.status = deactive_status
            selected_document.save()
            messages.success(request, "Document Deleted Successfully")
            return redirect('csp_app:document_upload', selected_document.fk_candidate_code)
        all_active_candidates = vendor_candidates(request.user)
        return render(request, 'csp_app/candidatedocuments.html', {'allcandidates': all_active_candidates, 'view_candidate': candidate, 'mandatory_list': mandatory_list, 'document_list': document_list })        
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
            template = render_to_string('csp_app/vendor_status_change_et.html', {'candidate_code':candidate.pk ,'prev':prev_status, 'current':status.status_name , 'user': request.user})
            our_email = EmailMessage(
                'Candidate Status Updated By Vendor',
                template,
                settings.EMAIL_HOST_USER,
                [ candidate_vendor_mailid, 'sadaf.shaikh@udaan.com'],
            ) 
            our_email.fail_silently = False
            our_email.send()
            if str(status_id) == '0':
                template = render_to_string('csp_app/loi.html', {'candidate_name': candidate.First_Name, 'candidate_code':candidate.pk ,'status':status.status_name })
                our_email = EmailMessage(
                    'LOI',
                    template,
                    settings.EMAIL_HOST_USER,
                    [ candidate.Personal_Email_Id , 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
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
        return render(request, 'csp_app/candidates.html', {'allcandidates': all_active_candidates,'candidate_list': candidate_list })        
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
            template = render_to_string('csp_app/vendor_status_change_et.html', {'candidate_code':candidate.pk ,'prev':prev_status, 'current':status.status_name , 'user': request.user})
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
                template = render_to_string('csp_app/loi.html', {'candidate_name': candidate.First_Name, 'candidate_code':candidate.pk ,'status':status.status_name })
                our_email = EmailMessage(
                    'LOI',
                    template,
                    settings.EMAIL_HOST_USER,
                    [ candidate.Personal_Email_Id , 'sadaf.shaikh@udaan.com'],
                ) 
                our_email.fail_silently = False
                our_email.send()
            # msg = 'Candidate status for '+ str(candidate.First_Name) +' updated to' + str(status.status_name) +' from ' + str(prev_status) + ' with candidate code " ' + str(candidate.pk) + ' by ' + str(request.user) + ' .'
            # send_mail('Candidate Status Updated', msg,'workmail052020@gmail.com',[ candidate_vendor_mailid, 'sadaf.shaikh@udaan.com'],fail_silently=False)
      
            messages.success(request, "Candidate Status Updated")
            return redirect('csp_app:candidate')
        return render(request, 'csp_app/candidates.html', {'allcandidates': all_active_candidates,'candidate_list': candidate_list })        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def entity(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('created_date_time')
    # view_entity_list = []
    # if request.method == 'GET':
    #     print("here")
    #     print(request.GET.get("view_id"))
    #     # print(request.DIALOG.get)
    #     if request.GET.get("view_id") != '':
            
    #         entity_id = request.POST.get("view_id")
    #         print(entity_id)
    #         view_entity_list = master_entity.objects.get(pk = entity_id)

    return render(request, 'csp_app/entity.html', {'allcandidates': all_active_candidates,'entity_list': entity_list})

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
                messages.error(request, "Entity Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:entity')
            else:
                selected_entity = master_entity.objects.get(pk = entity_id, status= active_status)
                selected_entity.modified_by = str(request.user)
                selected_entity.modified_date_time = datetime.now()
                selected_entity.status = deactive_status
                selected_entity.save()
                messages.success(request, "Entity Deleted Successfully")
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
        return render(request, 'csp_app/viewentity.html', {'allcandidates': all_active_candidates,'view_entity_list': view_entity_list, 'entity_list': entity_list})
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
           
        return render(request, 'csp_app/editentity.html', {'allcandidates': all_active_candidates,'view_entity_list': selected_entity, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

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
                        messages.error(request, "Entity Already Exist")
                        return redirect('csp_app:entity')
                    except ObjectDoesNotExist:
                        entity.entity_name = name 
                        entity.modified_by = str(request.user)
                        entity.modified_date_time = datetime.now()
                        entity.save()
                        messages.success(request, "Entity Updated Successfully")
                        return redirect('csp_app:entity')
                else:
                    messages.warning(request, "Entity Name Cannot Be Blank")
                    return redirect('csp_app:entity')         
           
        return render(request, 'csp_app/editentity.html', {'allcandidates': all_active_candidates,'view_entity_list': entity, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def create_entity(request):
    if request.method == 'POST':
        entity_name = request.POST.get("entity_name")
        if entity_name == None or entity_name == ' ':
            messages.warning(request, "Entity Name Expected")
            return redirect('csp_app:entity')
        try:
            duplicate_entity = master_entity.objects.get(entity_name=entity_name , status = active_status)
            messages.error(request, "Entity Already Exist")
            return redirect('csp_app:entity')
        except ObjectDoesNotExist:
            new_entity = master_entity(entity_name= entity_name , created_by = str(request.user))
            new_entity.save()
            messages.success(request, "Entity Created Successfully")
            return redirect('csp_app:entity')
    return render(request, 'csp_app/entity.html', {'allcandidates': all_active_candidates,})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def vendor(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name').order_by('entity_name')
    vendor_list = master_vendor.objects.filter(status = active_status).order_by('vendor_name')

    return render(request, 'csp_app/vendor.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'vendor_list': vendor_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_vendor(request):
    vendor_list = master_vendor.objects.filter(status = active_status).order_by('vendor_name')
    try:
        if request.method == 'POST':
            vendor_id = request.POST.get("view_id")
            view_vendor_list = master_vendor.objects.filter(pk = vendor_id)
        return render(request, 'csp_app/viewvendor.html', {'allcandidates': all_active_candidates,'view_vendor_list': view_vendor_list, 'vendor_list': vendor_list})
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
                send_mail('Vendor Account Disabled', msg,'workmail052020@gmail.com',[ selected_vendor.vendor_email_id, 'sadaf.shaikh@udaan.com'],fail_silently=False)
      
                messages.success(request, "Vendor Deleted Successfully")
                return redirect('csp_app:vendor')
        return render(request, 'csp_app/vendor.html', {'allcandidates': all_active_candidates,})
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
           
        return render(request, 'csp_app/editvendor.html', {'allcandidates': all_active_candidates,'view_vendor_list': selected_vendor,'entity_list':entity_list, 'vendor_list': vendor_list})
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
                vendor_email_pwd = request.POST.get("e_vendor_email_pwd")
                entity = request.POST.get("e_vendor_entity")
                if entity == None or entity == '':
                    messages.warning(request, "Choose Entity and Try Again")
                    return redirect('csp_app:vendor')
                entity_fk = master_entity.objects.get(pk = entity)
                
                try:
                    #same data code to add
                    a = master_vendor.objects.get(vendor_name= vendor_name , spoc_name= vendor_spoc,spoc_email_id= vendor_spoc_email, vendor_phone_number= vendor_phone, vendor_email_id= vendor_email, fk_entity_code= entity_fk, status= active_status)
                    print(a)
                    messages.error(request, "Vendor Already Exist")
                    return redirect('csp_app:vendor')
                except ObjectDoesNotExist:
                    selected_user = User.objects.get(email=vendor_email)
                    selected_user.email = vendor_email
                    selected_user.first_name = vendor_name 
                    selected_user.save()
                    vendor.vendor_name = vendor_name 
                    vendor.spoc_name = vendor_spoc
                    vendor.fk_entity_code = entity_fk
                    vendor.spoc_email_id = vendor_spoc_email
                    vendor.vendor_email_id = vendor_email
                    vendor.vendor_email_id_password = vendor_email_pwd
                    vendor.modified_by = str(request.user)
                    vendor.modified_date_time = datetime.now()
                    vendor.save()
                    msg = 'Vendor '+ str(vendor.vendor_name) +' with Username " ' + str(vendor.vendor_email_id) + ' Updated by ' + str(request.user) + ' .'
                    send_mail('Vendor Account Updated', msg,'workmail052020@gmail.com',[ vendor.vendor_email_id, 'sadaf.shaikh@udaan.com'],fail_silently=False)
      
                    messages.success(request, "Vendor Updated Successfully")
                    return redirect('csp_app:vendor')
               
           
        return render(request, 'csp_app/editvendor.html', {'allcandidates': all_active_candidates,'view_vendor_list': vendor, 'entity_list': entity_list})
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
        entity = request.POST.get("vendor_entity")
        if entity == None or entity == '':
            messages.warning(request, "Choose Entity And Try Again")
            return redirect('csp_app:vendor')
        entity_fk = master_entity.objects.get(pk=entity)
        
        try:
            print(1)
            duplicate_vendor_entity_spoc = master_vendor.objects.filter(vendor_name=vendor_name , fk_entity_code= entity, spoc_email_id=vendor_spoc_email, status = active_status)
            if duplicate_vendor_entity_spoc:
                messages.error(request, "Vendor Already Exist")
                return redirect('csp_app:vendor')
           
        except ObjectDoesNotExist:
            print(2)
        try:
            duplicate_vendor_email = master_vendor.objects.filter( vendor_email_id= vendor_email, fk_entity_code= entity, status = active_status)
            if duplicate_vendor_email:
                messages.error(request, "Vendor Email ID Already Exist")
                return redirect('csp_app:vendor')
            print(3)
        except ObjectDoesNotExist:
            print(4)
        try:
            duplicate_vendor_entity = master_vendor.objects.filter( vendor_name=vendor_name , fk_entity_code= entity, status = active_status)
            if duplicate_vendor_entity:                
                messages.error(request, "Vendor Already Exist")
                return redirect('csp_app:vendor')
            print(5)
        except ObjectDoesNotExist:   
            print('here') 
        try:      
            
            
            new_vendor = master_vendor(vendor_name= vendor_name , spoc_name= vendor_spoc,spoc_email_id= vendor_spoc_email, vendor_phone_number= vendor_phone, vendor_email_id= vendor_email, vendor_email_id_password= vendor_email_pwd, fk_entity_code= entity_fk, created_by = str(request.user))
            new_vendor.save()
            
            newadmintemplate = render_to_string('csp_app/new_vendor_account_success_admin_et.html', {'vendor_name':vendor_name, 'vendor_email': vendor_email, 'vendor_spoc': vendor_spoc, 'vendor_spoc_email': vendor_spoc_email, 'admin': str(request.user)})
            our_email = EmailMessage(
                'CSP_APP: New vendor account created.',
                newadmintemplate,
                settings.EMAIL_HOST_USER,
                [ request.user.email, 'sadaf.shaikh@udaan.com' ],
            ) 
            our_email.fail_silently = False
            our_email.send() 
            assign_group = Group.objects.get(name='Vendor')         
            user = User.objects.create_user(vendor_email)
            # password = User.objects.make_random_password()
            user.password = vendor_email_pwd
            user.set_password(user.password)
            user.first_name = vendor_name 
            user.email = vendor_email
            assign_group.user_set.add(user)     
            user.save()
            newtemplate = render_to_string('csp_app/new_vendor_account_success_et.html', {'vendor':vendor_name, 'username': vendor_email, 'password': vendor_email_pwd})
            our_email = EmailMessage(
                'CSP_APP: New vendor account created.',
                newtemplate,
                settings.EMAIL_HOST_USER,
                [ vendor_email],
            ) 
            our_email.fail_silently = False
            our_email.send()
            messages.success(request, "Vendor Account Created. Check Mail For Credentials")            
            return redirect('csp_app:vendor')
        except IntegrityError:
            template = render_to_string('csp_app/use_old_password_vendor_et.html', {'vendor':vendor_name, 'entity': entity_fk})
            our_email = EmailMessage(
                'CSP_APP',
                template,
                settings.EMAIL_HOST_USER,
                [ vendor_email, 'sadaf.shaikh@udaan.com'],
            ) 
            our_email.fail_silently = False
            our_email.send()      
            messages.success(request, "Vendor Account Created. Check Mail For Credentials")            
            return redirect('csp_app:vendor')
       
    return render(request, 'csp_app/vendor.html', {'allcandidates': all_active_candidates})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  department(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
    return render(request, 'csp_app/department.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'department_list': dept_list})

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
            messages.warning(request, "Choose Entity And Try Again")
            return redirect('csp_app:department')
        entity_fk = master_entity.objects.get(pk=entity)
        try:
            duplicate_dept = master_department.objects.get(department_name=dept_name , fk_entity_code= entity_fk, status = active_status)
            messages.error(request, "Department Already Exist")
            return redirect('csp_app:department')
        except ObjectDoesNotExist:
            new_department = master_department(department_name= dept_name , fk_entity_code= entity_fk, created_by = str(request.user))
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
        return render(request, 'csp_app/viewdepartment.html', {'allcandidates': all_active_candidates,'view_dept_list': view_dept_list,'department_list': department_list, 'entity_list': entity_list})
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
        return render(request, 'csp_app/editdepartment.html', {'allcandidates': all_active_candidates,'view_dept_list': selected,'department_list': department_list, 'entity_list': entity_list})
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
                        messages.warning(request, "Choose Entity and Try Again")
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
           
        return render(request, 'csp_app/editdepartment.html', {'allcandidates': all_active_candidates,'view_department_list': department, 'department_list': department_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  function(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
    function_list = master_function.objects.filter(status = active_status).order_by('function_name')
    return render(request, 'csp_app/function.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list})

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
            new_function = master_function( function_name= function_name , fk_department_code= department_fk, created_by = str(request.user))
            new_function.save()
            messages.success(request, "Function Saved Successfully")
            return redirect('csp_app:function')
    return render(request, 'csp_app/function.html', {'allcandidates': all_active_candidates,})

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
        return render(request, 'csp_app/viewfunction.html', {'allcandidates': all_active_candidates,'view_function_list': view_function_list,'function_list': function_list, 'department_list': department_list, 'entity_list': entity_list})
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
        return render(request, 'csp_app/editfunction.html', {'allcandidates': all_active_candidates,'view_function_list': selected, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
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
           
        return render(request, 'csp_app/editfunction.html', {'allcandidates': all_active_candidates,'view_department_list': department, 'department_list': department_list, 'entity_list': entity_list})
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

    return render(request, 'csp_app/team.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list})

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
            new_team = master_team( team_name= team_name , fk_function_code=function_fk, created_by = str(request.user))
            new_team.save()
            messages.success(request, "Team Saved Successfully")
            return redirect('csp_app:team')
    return render(request, 'csp_app/team.html', {'allcandidates': all_active_candidates,})

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
        return render(request, 'csp_app/viewteam.html', {'allcandidates': all_active_candidates,'view_team_list': view_team_list,'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
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
        return render(request, 'csp_app/editteam.html', {'allcandidates': all_active_candidates,'view_team_list': selected,'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
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
           
        return render(request, 'csp_app/editteam.html', {'allcandidates': all_active_candidates,'view_team_list': selected,'function_list': function_list, 'department_list': department_list, 'entity_list': entity_list})
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
    return render(request, 'csp_app/subteam.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'subteam_list': subteam_list})

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
            new_subteam = master_sub_team( sub_team_name= subteam_name , fk_team_code=team_fk, created_by = str(request.user))
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
        return render(request, 'csp_app/viewsubteam.html', {'allcandidates': all_active_candidates,'view_subteam_list': view_subteam_list,'subteam_list': subteam_list, 'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
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
        return render(request, 'csp_app/editsubteam.html', {'allcandidates': all_active_candidates,'view_subteam_list': selected,'subteam_list': subteam_list, 'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
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
           
        return render(request, 'csp_app/editsubteam.html', {'allcandidates': all_active_candidates,'view_subteam_list': selected,'team_list': team_list, 'function_list': function_list, 'department_list': department_list, 'entity_list': entity_list})
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
    return render(request, 'csp_app/designation.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_designation(request):
    if request.method == 'POST':
        designation_name = request.POST.get("desg_name")
        subteam = request.POST.get("desg_subteam")
        if subteam == None or subteam == '':
            messages.warning(request, "Choose Sub Team And Try Again")
            return redirect('csp_app:designation')
        if designation_name == None or designation_name == '':
            messages.warning(request, "Designation Cannot Be Blank")
            return redirect('csp_app:designation')
        subteam_fk = master_sub_team.objects.get(pk=subteam)
        try:
            dup_designation = master_designation.objects.get( designation_name= designation_name , fk_sub_team_code=subteam_fk, status = active_status)
           
            messages.error(request, "Designation Already Exist")
            return redirect('csp_app:subteam')
        except ObjectDoesNotExist: 

            new_designation = master_designation( designation_name= designation_name , fk_sub_team_code=subteam_fk, created_by = str(request.user))
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
        return render(request, 'csp_app/viewdesignation.html', {'allcandidates': all_active_candidates,'view_designation_list': view_designation_list,'designation_list': designation_list,  'subteam_list': subteam_list, 'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
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

    try:
        if request.method == 'POST':
            designation_id = request.POST.get("view_id")
            selected = master_designation.objects.filter(pk = designation_id)        
        return render(request, 'csp_app/editdesignation.html', {'allcandidates': all_active_candidates,'view_designation_list': selected, 'designation_list':designation_list, 'subteam_list': subteam_list, 'team_list': team_list, 'function_list': function_list,'department_list': department_list, 'entity_list': entity_list})
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

    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_designation.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_designation_name") != None:
                    name = request.POST.get("e_designation_name")
                    subteam = request.POST.get("e_designation_subteam")
                    if subteam == None or subteam == '':
                        messages.warning(request, "Choose Sub Team and Try Again")
                        return redirect('csp_app:designation')
                    subteam_fk = master_sub_team.objects.get(pk = subteam)
                    try:
                        if selected.designation_name == name  and selected.fk_sub_team_code == subteam_fk:
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:designation')
                        a = master_designation.objects.get(designation_name= name , fk_sub_team_code= subteam_fk, status= active_status)
                        messages.error(request, "Designation Already Exist")
                        return redirect('csp_app:designation')
                    except ObjectDoesNotExist:
                        selected.designation_name = name 
                        selected.fk_sub_team_code = subteam_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "Designation Updated Successfully")
                        return redirect('csp_app:designation')
                else:
                    messages.warning(request, "Sub Team Name Cannot Be Blank")
                    return redirect('csp_app:designation')         
           
        return render(request, 'csp_app/editdesignation.html', {'allcandidates': all_active_candidates,'view_designation_list': selected,'subteam_list':subteam_list, 'team_list': team_list, 'function_list': function_list, 'department_list': department_list, 'entity_list': entity_list})
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
    return render(request, 'csp_app/region.html', {'allcandidates': all_active_candidates,'entity_list': entity_list,'region_list': region_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_region(request):
    if request.method == 'POST':
        region_name = request.POST.get("region_name")
        entity = request.POST.get("region_entity")
        if entity == None or entity == '':
            messages.warning(request, "Choose Entity And Try Again")
            return redirect('csp_app:region')
        if region_name == None or region_name== '':
            messages.warning(request, "Region Cannot Be Blank")
            return redirect('csp_app:region')
        entity_fk = master_entity.objects.get(pk=entity)
        try:
            dup_region = master_region.objects.get( region_name= region_name , fk_entity_code =entity_fk, status = active_status)

            messages.error(request, "Region Already Exist")
            return redirect('csp_app:region')
        except ObjectDoesNotExist: 
            new_region = master_region( region_name= region_name , fk_entity_code =entity_fk, created_by = str(request.user))
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
        return render(request, 'csp_app/viewregion.html', {'allcandidates': all_active_candidates,'view_region_list': view_region_list,'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_region(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)

    try:
        if request.method == 'POST':
            region_id = request.POST.get("view_id")
            selected = master_region.objects.filter(pk = region_id)        
        return render(request, 'csp_app/editregion.html', {'allcandidates': all_active_candidates,'view_region_list': selected,'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_region(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_region.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_region_name") != None:
                    name = request.POST.get("e_region_name")
                    entity = request.POST.get("e_region_entity")
                    if entity == None or entity == '':
                        messages.warning(request, "Choose Entity and Try Again")
                        return redirect('csp_app:region')
                    entity_fk = master_entity.objects.get(pk = entity)
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
           
        return render(request, 'csp_app/editregion.html', {'allcandidates': all_active_candidates,'view_region_list': region, 'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  




@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  state(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    dept_list = master_department.objects.filter(status = active_status).order_by('department_name')
    function_list = master_function.objects.filter(status = active_status).order_by('function_name')
    team_list = master_team.objects.filter(status = active_status).order_by('team_name')
    subteam_list = master_sub_team.objects.filter(status = active_status).order_by('sub_team_name')
    desg_list = master_designation.objects.filter(status = active_status).order_by('designation_name')
    region_list = master_region.objects.filter(status = active_status).order_by('region_name')
    state_list = master_state.objects.filter(status = active_status).order_by('state_name')
    return render(request, 'csp_app/state.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_state(request):
    if request.method == 'POST':
        state_name = request.POST.get("state_name")
        region = request.POST.get("state_region")
        if region == None or region == '':
            messages.warning(request, "Choose Region And Try Again")
            return redirect('csp_app:state')
        if state_name == None or state_name == '':
            messages.warning(request, "State Cannot Be Blank")
            return redirect('csp_app:state')
        region_fk = master_region.objects.get(pk=region)
        try:
            dup_region = master_state.objects.get( state_name= state_name , fk_region_code =region_fk,status = active_status)

            messages.error(request, "State Already Exist")
            return redirect('csp_app:state')
        except ObjectDoesNotExist: 
            new_state = master_state( state_name= state_name , fk_region_code =region_fk, created_by = str(request.user))
            new_state.save()
            messages.success(request, "State Saved Successfully")
            return redirect('csp_app:state')
    return render(request, 'csp_app/state.html', {'allcandidates': all_active_candidates,})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_state(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    state_list = master_state.objects.filter(status=active_status)
    try:
        if request.method == 'POST':
            state_id = request.POST.get("view_id")
            view_state_list = master_state.objects.filter(pk = state_id)
        return render(request, 'csp_app/viewstate.html', {'allcandidates': all_active_candidates,'view_state_list': view_state_list,'state_list': state_list, 'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_state(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    state_list = master_state.objects.filter(status=active_status)
    try:
        if request.method == 'POST':
            state_id = request.POST.get("view_id")
            selected = master_state.objects.filter(pk = state_id)        
        return render(request, 'csp_app/editstate.html', {'allcandidates': all_active_candidates,'view_state_list': selected, 'state_list': state_list,'region_list': region_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_state(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status= active_status)
    state_list = master_state.objects.filter(status=active_status)
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                selected = master_state.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_state_name") != None:
                    name = request.POST.get("e_state_name")
                    region = request.POST.get("e_state_dept")
                    # entity = request.POST.get("e_state_entity")
                    print(region)
                    if region == None or region == '':
                        messages.warning(request, "Choose region and Try Again")
                        return redirect('csp_app:state')
                    region_fk = master_region.objects.get(pk = region)
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
           
        return render(request, 'csp_app/editstate.html', {'allcandidates': all_active_candidates,'view_region_list': region, 'region_list': region_list, 'entity_list': entity_list})
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
    return render(request, 'csp_app/city.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'city_list': city_list, 'state_list':state_list, 'region_list': region_list})


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
        return render(request, 'csp_app/viewcity.html', {'allcandidates': all_active_candidates,'view_city_list': view_city_list,'city_list': city_list, 'function_list': function_list,'region_list': region_list, 'entity_list': entity_list})
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
        return render(request, 'csp_app/editcity.html', {'allcandidates': all_active_candidates,'view_city_list': selected,'city_list': city_list, 'function_list': function_list,'region_list': region_list, 'entity_list': entity_list})
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
           
        return render(request, 'csp_app/editcity.html', {'allcandidates': all_active_candidates,'view_city_list': selected,'state_list': state_list, 'region_list': region_list, 'entity_list': entity_list})
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
            new_city = master_city( city_name= city_name , fk_state_code =state_fk, created_by = str(request.user))
            new_city.save()
            messages.success(request, "City Saved Successfully")
            return redirect('csp_app:city')
    return render(request, 'csp_app/city.html', {'allcandidates': all_active_candidates,})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  location(request):
    entity_list = master_entity.objects.filter(status = active_status).order_by('entity_name')
    region_list = master_region.objects.filter(status = active_status).order_by('region_name')
    state_list = master_state.objects.filter(status = active_status).order_by('state_name')
    city_list = master_city.objects.filter(status= active_status).order_by('city_name')
    location_list = master_location.objects.filter(status= active_status).order_by('location_name')
    return render(request, 'csp_app/location.html', {'allcandidates': all_active_candidates,'entity_list': entity_list, 'location_list': location_list, 'city_list': city_list, 'state_list':state_list, 'region_list': region_list})

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
            new_location = master_location( location_name= location_name ,location_code=code, fk_city_code =city_fk, created_by = str(request.user))
            new_location.save()
            messages.success(request, "Location Saved Successfully")
            return redirect('csp_app:location')
    return render(request, 'csp_app/location.html', {'allcandidates': all_active_candidates,})


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
        return render(request, 'csp_app/viewlocation.html', {'allcandidates': all_active_candidates,'view_location_list': view_location_list,'location_list': location_list, 'city_list': city_list, 'state_list': state_list,'region_list': region_list, 'entity_list': entity_list})
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
        return render(request, 'csp_app/editlocation.html', {'allcandidates': all_active_candidates,'view_location_list': selected,'location_list': location_list, 'city_list': city_list, 'state_list': state_list,'region_list': region_list, 'entity_list': entity_list})
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
                    city = request.POST.get("e_location_city")
                    # entity = request.POST.get("e_state_entity")
                    # print(region)
                    if city == None or city == '':
                        messages.warning(request, "Choose city and Try Again")
                        return redirect('csp_app:location')
                    city_fk = master_city.objects.get(pk = city)
                    try:
                        if selected.location_name == name  and selected.fk_city_code == city_fk:
                            messages.warning(request, "No Changes Detected")
                            return redirect('csp_app:city')
                        a = master_location.objects.get(location_name= name , fk_city_code= city_fk, status= active_status)
                        messages.error(request, "city Already Exist")
                        return redirect('csp_app:city')
                    except ObjectDoesNotExist:
                        selected.location_name = name 
                        selected.fk_city_code = city_fk
                        selected.modified_by = str(request.user)
                        selected.modified_date_time = datetime.now()
                        selected.save()
                        messages.success(request, "Sub city Updated Successfully")
                        return redirect('csp_app:location')
                else:
                    messages.warning(request, "Sub state Name Cannot Be Blank")
                    return redirect('csp_app:location')         
           
        return render(request, 'csp_app/editlocation.html', {'allcandidates': all_active_candidates,'view_location_list': selected,'city_list': city_list, 'state_list': state_list, 'region_list': region_list, 'entity_list': entity_list})
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
    print(request.user)
    user_list = User.objects.all().exclude(is_superuser=True)
    group_list = Group.objects.all()    
    return render(request, 'csp_app/create_user.html', {'allcandidates': all_active_candidates,'user_list': user_list, 'group_list': group_list})



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_user(request):
    if request.method == 'POST':
        usrname = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        group = request.POST.get('usergroup')
        try:
        
            password = User.objects.make_random_password()
            assign_group = Group.objects.get(name=group) 
            
            user = User.objects.create_user(usrname)
            password = User.objects.make_random_password()
            print(password)
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
            template = render_to_string('csp_app/new_user_et.html', {'user': firstname ,'username': email, 'password': password})
            our_email = EmailMessage(
                'Account Created with UDAAN CSP_APP.',
                template,
                settings.EMAIL_HOST_USER,
                [ email, 'sadaf.shaikh@udaan.com'],
            ) 
            our_email.fail_silently = False
            our_email.send()
            admintemplate = render_to_string('csp_app/new_user_admin_et.html', {'user': firstname ,'username': email, 'password': password})
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
                group = request.user.groups.all()
                for groupname in group:
                    group_name = groupname
                # print(group_name)
                # print(usrname)
                # print(request.user.groups.all()[0].name)
                # print(request.session.session_key)
                # print(type(group_name))
                # print(str(group_name))
                # print(str(group_name) == 'Admin')
                if str(group_name) == 'Admin':
                    messages.success(request, "Login Successfull")
                    return redirect('csp_app:entity')
                elif str(group_name) == 'Vendor':
                    messages.success(request, "Login Successfull")
                    return redirect('csp_app:candidate')
                else:
                    messages.success(request, "Login Successfull")
                    return redirect('csp_app:candidate')
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

