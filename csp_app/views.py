from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from csp_app.models import status, master_candidate, master_entity, master_designation, master_vendor, master_department, \
                            master_function, master_team, master_sub_team, master_region, master_state, master_city, master_location, hiring_type, \
                            sub_source, salary_type, gender, laptop_allocation
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


active_status = status.objects.get(pk=1)
deactive_status = status.objects.get(pk=2)

@login_required(login_url='/notlogin/')
def candidate(request):
    
    entity_list = master_entity.objects.filter(status = active_status)
    vendor_list = master_vendor.objects.filter(status = active_status)

    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)
    subteam_list = master_sub_team.objects.filter(status = active_status)
    desg_list = master_designation.objects.filter(status = active_status)
    region_list = master_region.objects.filter(status = active_status)
    state_list = master_state.objects.filter(status = active_status)
    city_list = master_city.objects.filter(status= active_status)
    location_list = master_location.objects.filter(status= active_status)
    hiring_type_list = hiring_type.objects.filter(status= active_status)
    sub_source_list = sub_source.objects.filter(status= active_status)
    salary_type_list = salary_type.objects.filter(status= active_status)
    gender_list = gender.objects.filter(status= active_status)
    laptop_allocation_list = laptop_allocation.objects.filter(status= active_status)
    candidate_list = master_candidate.objects.all()
    return render(request, 'csp_app/candidates.html', {'entity_list': entity_list, 'location_list': location_list, 
    'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 
    'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list,
    'hiring_type_list': hiring_type_list, 'sub_source_list': sub_source_list, 'salary_type_list': salary_type_list, 
    'gender_list': gender_list, 'laptop_allocation_list': laptop_allocation_list, 'vendor_list': vendor_list, 'candidate_list': candidate_list })

@login_required(login_url='/notlogin/')
def create_candidate(request):
    if request.method == 'POST':

        firstname = request.POST.get("c_firstname")
        middlename = request.POST.get("c_middlename")
        lastname = request.POST.get("c_lastname")
        doj = request.POST.get("c_doj")
        fathername = request.POST.get("c_fathername")
        dob = request.POST.get("c_dob")
        aadhaar = request.POST.get("c_aadhaar")
        Pan = request.POST.get("c_pan")
        contact_no = request.POST.get("c_contact")
        emergency_no = request.POST.get("c_emergency")
        hiring = request.POST.get("c_hiring_type")
        replacement = request.POST.get("c_replacement")
        subsource = request.POST.get("c_sub_source")
        referral = request.POST.get("c_referral")
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
        reporting_manager = request.POST.get("c_reporting_manager")
        reporting_manager_email = request.POST.get("c_reporting_manager_email")
        c_gender = request.POST.get("c_gender")
        email_creation = request.POST.get("c_email_creation")
        laptopallocation = request.POST.get("c_laptop_allocation")
        salarytype = request.POST.get("c_salary_type")
        gross_salary = request.POST.get("c_gross_salary")
        if hiring == None:
            messages.warning(request, "Choose Hiring Type And Try Again")
            return redirect("csp_app:candidate")
        hiring_fk = hiring_type.objects.get(pk= hiring)
        if sub_source == None:
            messages.warning(request, "Choose  Sub Source Type And Try Again")
            return redirect("csp_app:candidate")
        subsource_fk = sub_source.objects.get(pk= subsource)
        if c_gender == None:
            messages.warning(request, "Choose  Gender And Try Again")
            return redirect("csp_app:candidate")
        gender_fk = gender.objects.get(pk= c_gender)
        if laptopallocation == None:
            messages.warning(request, "Choose  Laptop Allocation And Try Again")
            return redirect("csp_app:candidate")
        la_fk = laptop_allocation.objects.get(pk= laptopallocation)
        if salarytype == None:
            messages.warning(request, "Choose  Salary Type And Try Again")
            return redirect("csp_app:candidate")
        salarytype_fk = salary_type.objects.get(pk= salarytype)
        if entity == None:
            messages.warning(request, "Choose  Entity Type And Try Again")
            return redirect("csp_app:candidate")
        entity_fk = master_entity.objects.get(pk= entity)
        if vendor == None:
            messages.warning(request, "Choose  vendor Type And Try Again")
            return redirect("csp_app:candidate")
        vendor_fk = master_vendor.objects.get(pk= vendor)
        if department == None:
            messages.warning(request, "Choose  Department Type And Try Again")
            return redirect("csp_app:candidate")
        department_fk = master_department.objects.get(pk= department)
        if function == None:
            messages.warning(request, "Choose  Function Type And Try Again")
            return redirect("csp_app:candidate")
        function_fk = master_function.objects.get(pk= function)
        if team == None:
            messages.warning(request, "Choose  Team Type And Try Again")
            return redirect("csp_app:candidate")
        team_fk = master_team.objects.get(pk= team)
        if sub_team == None:
            messages.warning(request, "Choose  Sub Team Type And Try Again")
            return redirect("csp_app:candidate")
        sub_team_fk = master_sub_team.objects.get(pk= sub_team)
        if designation == None:
            messages.warning(request, "Choose  Designation Type And Try Again")
            return redirect("csp_app:candidate")
        designation_fk = master_designation.objects.get(pk= designation)
        if region == None:
            messages.warning(request, "Choose  Region Type And Try Again")
            return redirect("csp_app:candidate")
        region_fk = master_region.objects.get(pk= region)
        if state == None:
            messages.warning(request, "Choose  State Type And Try Again")
            return redirect("csp_app:candidate")
        state_fk = master_state.objects.get(pk= state)
        if city == None:
            messages.warning(request, "Choose  City Type And Try Again")
            return redirect("csp_app:candidate")
        city_fk = master_city.objects.get(pk= city)
        if location == None:
            messages.warning(request, "Choose  Location Type And Try Again")
            return redirect("csp_app:candidate")
        location_fk = master_location.objects.get(pk= location)
        try:
            dup_candidate_aadhaar = master_candidate.objects.get(Aadhaar_Number= aadhaar, status= active_status)
            messages.error( request, "Candidate Aadhaar Number Already Exist")
            return redirect("csp_app:candidate")
            dup_candidate_pan = master_candidate.objects.get(PAN_Number= Pan, status= active_status)
            messages.error( request, "Candidate PAN Number Already Exist")
            return redirect("csp_app:candidate")
            dup_candidate_pan = master_candidate.objects.get(Contact_Number= contact_no, status= active_status)
            messages.error( request, "Candidate Contact Number Already Exist")
            return redirect("csp_app:candidate")
        except ObjectDoesNotExist:
            last_code_query = master_candidate.objects.latest('pk')
            last_code_str = last_code_query.pk
            next_code_int = int(last_code_str[1:])+ 1
            new_code = 'C' + str(next_code_int).zfill(9) #pk_candidate_code
            new_candidate = master_candidate(pk_candidate_code=new_code, First_Name=firstname, Middle_Name=middlename, Last_Name= lastname, Date_of_Joining= doj, Date_of_Birth= dob, Father_Name= fathername, Father_Date_of_Birth= dob,
            Aadhaar_Number= aadhaar, PAN_Number= Pan, Contact_Number= contact_no, Emergency_Contact_Number= emergency_no, Type_of_Hiring= hiring_fk, Replacement= replacement,
            Sub_Source= subsource_fk, Referral= referral, fk_vendor_code= vendor_fk, fk_entity_code= entity_fk, fk_department_code= department_fk, fk_function_code= function_fk, 
            fk_team_code= team_fk, fk_subteam_code= sub_team_fk, fk_designation_code= designation_fk, fk_region_code= region_fk, fk_state_code= state_fk, fk_city_code= city_fk, fk_location_code= location_fk,
            Reporting_Manager= reporting_manager, Reporting_Manager_E_Mail_ID= reporting_manager_email, Gender= gender_fk, E_Mail_ID_Creation= email_creation,
            Laptop_Allocation= la_fk, Salary_Type= salarytype_fk, Gross_Salary_Amount= gross_salary, created_by = str(request.user))
            new_candidate.save()
            msg = 'Candidate account created'
            send_mail('Candidate Account Created', msg,'workmail052020@gmail.com',['sadaf.shaikh@udaan.com', 'rahul.gandhi@udaan.com', reporting_manager_email, vendor_fk.spoc_email_id],fail_silently=False)
       
            messages.success(request, "Candidate Saved Successfully")
            return redirect("csp_app:candidate")

        return render(request, 'csp_app/candidates.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_candidate(request):
    candidate_list = master_candidate.objects.filter(status = active_status)
    try:
        if request.method == 'POST':
            candidate_id = request.POST.get("view_id")
            view_candidate_list = master_candidate.objects.filter(pk = candidate_id)
        return render(request, 'csp_app/viewcandidate.html', {'view_candidate_list': view_candidate_list, 'candidate_list': candidate_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def entity(request):
    entity_list = master_entity.objects.filter(status = active_status)
    # view_entity_list = []
    # if request.method == 'GET':
    #     print("here")
    #     print(request.GET.get("view_id"))
    #     # print(request.DIALOG.get)
    #     if request.GET.get("view_id") != '':
            
    #         entity_id = request.POST.get("view_id")
    #         print(entity_id)
    #         view_entity_list = master_entity.objects.get(pk = entity_id)

    return render(request, 'csp_app/entity.html', {'entity_list': entity_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def delete_entity(request):
    try:
        if request.method == 'POST':
            entity_id = request.POST.get("delete_id")
            entity_a = master_vendor.objects.filter(fk_entity_code=entity_id, status=active_status)
            entity_d = master_department.objects.filter(fk_entity_code=entity_id, status=active_status)
            entity_c = master_candidate.objects.filter(Entity=entity_id, status=active_status)
            if len(entity_a) >= 1 or len(entity_d) >= 1 or len(entity_c) >= 1:
                messages.error(request, "Entity Refrenced By Other Module Cannot Delete")
                return redirect('csp_app:entity')
            else:
                selected_entity = master_entity.objects.get(pk = entity_id, status= active_status)
                selected_entity.status = deactive_status
                selected_entity.save()
                messages.success(request, "Entity Deleted Successfully")
                return redirect('csp_app:entity')
        return render(request, 'csp_app/entity.html', {})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_entity(request):
    entity_list = master_entity.objects.filter(status = active_status)
    try:
        if request.method == 'POST':
            entity_id = request.POST.get("view_id")
            view_entity_list = master_entity.objects.filter(pk = entity_id)
        return render(request, 'csp_app/viewentity.html', {'view_entity_list': view_entity_list, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def view_edit_entity(request):
    entity_list = master_entity.objects.filter(status = active_status)
    try:
        if request.method == 'POST':
            entity_id = request.POST.get("view_id")
            selected_entity = master_entity.objects.filter(pk = entity_id)         
           
        return render(request, 'csp_app/editentity.html', {'view_entity_list': selected_entity, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def save_edit_entity(request):
    entity_list = master_entity.objects.filter(status = active_status)
    try:
        if request.method == 'POST':
           if request.POST.get("e_id") != '':
                entity = master_entity.objects.get(pk = request.POST.get("e_id"))
                if request.POST.get("e_entity_name") != None:
                    name = request.POST.get("e_entity_name")
                    try:
                        master_entity.objects.filter(entity_name= name, status= active_status)
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
           
        return render(request, 'csp_app/editentity.html', {'view_entity_list': selected_entity, 'entity_list': entity_list})
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")
    #  

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def create_entity(request):
    if request.method == 'POST':
        entity_name = request.POST.get("entity_name")
        if entity_name == None:
            messages.warning(request, "Entity Name Expected")
            return redirect('csp_app:entity')
        try:
            duplicate_entity = master_entity.objects.get(entity_name=entity_name, status = active_status)
            messages.error(request, "Entity Already Exist")
            return redirect('csp_app:entity')
        except ObjectDoesNotExist:
            new_entity = master_entity(entity_name= entity_name, created_by = str(request.user))
            new_entity.save()
            messages.success(request, "Entity Created Successfully")
            return redirect('csp_app:entity')
    return render(request, 'csp_app/entity.html', {})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def vendor(request):
    entity_list = master_entity.objects.filter(status = active_status)
    vendor_list = master_vendor.objects.filter(status = active_status)

    return render(request, 'csp_app/vendor.html', {'entity_list': entity_list, 'vendor_list': vendor_list})

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
        if entity == None:
            messages.warning(request, "Choose Entity And Try Again")
            return redirect('csp_app:vendor')
        entity_fk = master_entity.objects.get(pk=entity)
        
        try:
            print(1)
            duplicate_vendor_entity_spoc = master_vendor.objects.filter(vendor_name=vendor_name, fk_entity_code= entity, spoc_email_id=vendor_spoc_email, status = active_status)
            if duplicate_vendor_entity_spoc:
                messages.error(request, "vendor Already Exist")
                return redirect('csp_app:vendor')
           
        except ObjectDoesNotExist:
            print(2)
        # try:
        #     duplicate_vendor_email = master_vendor.objects.filter( vendor_email_id= vendor_email, status = active_status)
        #     if duplicate_vendor_email:
        #         messages.error(request, "vendor Email ID Already Exist")
        #         return redirect('csp_app:vendor')
        #     print(3)
        # except ObjectDoesNotExist:
        #     print(4)
        try:
            duplicate_vendor_entity = master_vendor.objects.filter( vendor_name=vendor_name, fk_entity_code= entity, status = active_status)
            if duplicate_vendor_entity:                
                messages.error(request, "vendor Already Exist")
                return redirect('csp_app:vendor')
            print(5)
        except ObjectDoesNotExist:   
            print('here')

        new_vendor = master_vendor(vendor_name= vendor_name, spoc_name= vendor_spoc,spoc_email_id= vendor_spoc_email, vendor_phone_number= vendor_phone, vendor_email_id= vendor_email, vendor_email_id_password= vendor_email_pwd, fk_entity_code= entity_fk, created_by = str(request.user))
        new_vendor.save()
        messages.success(request, "vendor Saved Successfully")
        return redirect('csp_app:vendor')
    return render(request, 'csp_app/vendor.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  department(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    return render(request, 'csp_app/department.html', {'entity_list': entity_list, 'department_list': dept_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_department(request):
    
    if request.method == 'POST':
        dept_name = request.POST.get("dept_name")
        if dept_name == None or dept_name == ' ':
            messages.warning(request, "Department Name Cannot Be Blank")
            return redirect('csp_app:department')
        entity = request.POST.get("dept_entity")
        if entity == None:
            messages.warning(request, "Choose Entity And Try Again")
            return redirect('csp_app:department')
        entity_fk = master_entity.objects.get(pk=entity)
        try:
            duplicate_dept = master_department.objects.get(department_name=dept_name, fk_entity_code= entity_fk, status = active_status)
            messages.error(request, "Department Already Exist")
            return redirect('csp_app:department')
        except ObjectDoesNotExist:
            new_department = master_department(department_name= dept_name, fk_entity_code= entity_fk, created_by = str(request.user))
            new_department.save()
            return redirect('csp_app:department')
    return render(request, 'csp_app/department.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  function(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    return render(request, 'csp_app/function.html', {'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_function(request):
    if request.method == 'POST':
        function_name = request.POST.get("function_name")
        function_dept = request.POST.get("function_dept")
        if function_name == None or function_name == '':
            messages.warning(request, "Function Name Cannot Be Blank")
            return redirect('csp_app:function')
        if function_dept == None:
            messages.warning(request, "Choose Department And Try Again")
            return redirect('csp_app:function')
        department_fk = master_department.objects.get(pk=function_dept)
        try:
            duplicate_function = master_function.objects.get(function_name=function_name, fk_department_code= department_fk, status = active_status)
            messages.error(request, "Function Already Exist")
            return redirect('csp_app:function')
        except ObjectDoesNotExist:            
            new_function = master_function( function_name= function_name, fk_department_code= department_fk, created_by = str(request.user))
            new_function.save()
            messages.success(request, "Function Saved Successfully")
            return redirect('csp_app:function')
    return render(request, 'csp_app/function.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  team(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)

    return render(request, 'csp_app/team.html', {'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get("team_name")
        team_function = request.POST.get("team_function")
        if team_name == None or team_name == '':
            messages.warning(request, "Team Name Cannot Be Blank")
            return redirect('csp_app:team')
        if team_function == None:
            messages.warning(request, "Choose Function And Try Again")
            return redirect('csp_app:team')
        function_fk = master_function.objects.get(pk=team_function)
       
        try:
            duplicate_team = master_team.objects.get( team_name= team_name, fk_function_code=function_fk, created_by = str(request.user))
            messages.error(request, "Team Already Exist")
            return redirect('csp_app:team')
        except ObjectDoesNotExist: 
            new_team = master_team( team_name= team_name, fk_function_code=function_fk, created_by = str(request.user))
            new_team.save()
            messages.success(request, "Team Saved Successfully")
            return redirect('csp_app:team')
    return render(request, 'csp_app/team.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  subteam(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)
    subteam_list = master_sub_team.objects.filter(status = active_status)
    return render(request, 'csp_app/subteam.html', {'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'subteam_list': subteam_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_subteam(request):

    if request.method == 'POST':
        subteam_name = request.POST.get("subteam_name")
        team = request.POST.get("subteam_team")
        if subteam_name == None or subteam_name == '':
            messages.warning(request, "Sub Team Name Cannot Be Blank")
            return redirect('csp_app:subteam')
        if team == None:
            messages.warning(request, "Choose Team And Try Again")
            return redirect('csp_app:subteam')
        team_fk = master_team.objects.get(pk= team)
        try:
            duplicate_subteam = master_sub_team.objects.get( sub_team_name= subteam_name, fk_team_code=team_fk, status = active_status)
            messages.error(request, "Sub Team Already Exist")
            return redirect('csp_app:subteam')
        except ObjectDoesNotExist: 
            new_subteam = master_sub_team( sub_team_name= subteam_name, fk_team_code=team_fk, created_by = str(request.user))
            new_subteam.save()
            messages.success(request, "Sub Team Saved Successfully")
            return redirect('csp_app:subteam')
    return render(request, 'csp_app/subteam.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  designation(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)
    subteam_list = master_sub_team.objects.filter(status = active_status)
    desg_list = master_designation.objects.filter(status = active_status)
    return render(request, 'csp_app/designation.html', {'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_designation(request):
    if request.method == 'POST':
        designation_name = request.POST.get("desg_name")
        subteam = request.POST.get("desg_subteam")
        if subteam == None:
            messages.warning(request, "Choose Sub Team And Try Again")
            return redirect('csp_app:designation')
        if designation_name == None:
            messages.warning(request, "Designation Cannot Be Blank")
            return redirect('csp_app:designation')
        subteam_fk = master_sub_team.objects.get(pk=subteam)
        try:
            dup_designation = master_designation.objects.get( designation_name= designation_name, fk_sub_team_code=subteam_fk, status = active_status)
           
            messages.error(request, "Designation Already Exist")
            return redirect('csp_app:subteam')
        except ObjectDoesNotExist: 

            new_designation = master_designation( designation_name= designation_name, fk_sub_team_code=subteam_fk, created_by = str(request.user))
            new_designation.save()
            messages.success(request, "Designation Saved Successfully")
            return redirect('csp_app:designation')
    return render(request, 'csp_app/designation.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def region(request):
    entity_list = master_entity.objects.filter(status = active_status)
    region_list = master_region.objects.filter(status = active_status)
    return render(request, 'csp_app/region.html', {'entity_list': entity_list,'region_list': region_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_region(request):
    if request.method == 'POST':
        region_name = request.POST.get("region_name")
        entity = request.POST.get("region_entity")
        if entity == None:
            messages.warning(request, "Choose Entity And Try Again")
            return redirect('csp_app:region')
        if region_name == None:
            messages.warning(request, "Region Cannot Be Blank")
            return redirect('csp_app:region')
        desg_fk = master_designation.objects.get(pk=desg)
        try:
            dup_region = master_region.objects.get( region_name= region_name, fk_entity_code =desg_fk, status = active_status)

            messages.error(request, "Region Already Exist")
            return redirect('csp_app:region')
        except ObjectDoesNotExist: 
            new_region = master_region( region_name= region_name, fk_entity_code =desg_fk, created_by = str(request.user))
            new_region.save()
            
            messages.success(request, "Region Saved Succesfully")
            return redirect('csp_app:region')
    return render(request, 'csp_app/region.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  state(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)
    subteam_list = master_sub_team.objects.filter(status = active_status)
    desg_list = master_designation.objects.filter(status = active_status)
    region_list = master_region.objects.filter(status = active_status)
    state_list = master_state.objects.filter(status = active_status)
    return render(request, 'csp_app/state.html', {'entity_list': entity_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_state(request):
    if request.method == 'POST':
        state_name = request.POST.get("state_name")
        region = request.POST.get("state_region")
        if region == None:
            messages.warning(request, "Choose Region And Try Again")
            return redirect('csp_app:state')
        if state_name == None:
            messages.warning(request, "State Cannot Be Blank")
            return redirect('csp_app:state')
        region_fk = master_region.objects.get(pk=region)
        try:
            dup_region = master_state.objects.get( state_name= state_name, fk_region_code =region_fk,status = active_status)

            messages.error(request, "State Already Exist")
            return redirect('csp_app:state')
        except ObjectDoesNotExist: 
            new_state = master_state( state_name= state_name, fk_region_code =region_fk, created_by = str(request.user))
            new_state.save()
            messages.success(request, "State Saved Successfully")
            return redirect('csp_app:state')
    return render(request, 'csp_app/state.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  city(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)
    subteam_list = master_sub_team.objects.filter(status = active_status)
    desg_list = master_designation.objects.filter(status = active_status)
    region_list = master_region.objects.filter(status = active_status)
    state_list = master_state.objects.filter(status = active_status)
    city_list = master_city.objects.filter(status= active_status)
    return render(request, 'csp_app/city.html', {'entity_list': entity_list, 'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_city(request):
    if request.method == 'POST':
        city_name = request.POST.get("city_name")
        state = request.POST.get("city_state")
        if state == None:
            messages.warning(request, "Choose State And Try Again")
            return redirect('csp_app:city')
        if city_name == None:
            messages.warning(request, "City Cannot Be Blank")
            return redirect('csp_app:city')
        state_fk = master_state.objects.get(pk=state)
        try:
            dup_city = master_city.objects.get( city_name= city_name, fk_state_code =state_fk,status = active_status)

            messages.error(request, "City Already Exist")
            return redirect('csp_app:city')
        except ObjectDoesNotExist: 
            new_city = master_city( city_name= city_name, fk_state_code =state_fk, created_by = str(request.user))
            new_city.save()
            messages.success(request, "City Saved Successfully")
            return redirect('csp_app:city')
    return render(request, 'csp_app/city.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  location(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)
    subteam_list = master_sub_team.objects.filter(status = active_status)
    desg_list = master_designation.objects.filter(status = active_status)
    region_list = master_region.objects.filter(status = active_status)
    state_list = master_state.objects.filter(status = active_status)
    city_list = master_city.objects.filter(status= active_status)
    location_list = master_location.objects.filter(status= active_status)
    return render(request, 'csp_app/location.html', {'entity_list': entity_list, 'location_list': location_list, 'city_list': city_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_location(request):
    if request.method == 'POST':
        location_name = request.POST.get("location_name")
        city = request.POST.get("location_city")
        if city == None:
            messages.warning(request, "Choose City And Try Again")
            return redirect('csp_app:location')
        if location_name == None:
            messages.warning(request, "Location Cannot Be Blank")
            return redirect('csp_app:location')
        city_fk = master_city.objects.get(pk=city)
        try:
            dup_location = master_location.objects.get( location_name= location_name, fk_city_code =city_fk,status = active_status)

            messages.error(request, "City Already Exist")
            return redirect('csp_app:location')
        except ObjectDoesNotExist: 
            new_location = master_location( location_name= location_name, fk_city_code =city_fk, created_by = str(request.user))
            new_location.save()
            messages.success(request, "Location Saved Successfully")
            return redirect('csp_app:location')
    return render(request, 'csp_app/location.html', {})

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_user_view(request):
    user_list = User.objects.all().exclude(is_superuser=True)
    group_list = Group.objects.all()    
    return render(request, 'csp_app/create_user.html', {'user_list': user_list, 'group_list': group_list})



@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  create_user(request):
    if request.method == 'POST':
        usrname = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        group = request.POST.get('usergroup')
        # try:
        password = User.objects.make_random_password()
        assign_group = Group.objects.get(name=group) 
        
        # new_user = User(username= usrname, password=password, first_name= firstname, last_name=lastname, email=email, groups.set_group(group))        
        # new_user.save()
        # print("saved")
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
        msg = 'User account of type " ' + group +' " created with Username " ' + usrname + '" and  Password " ' + password + '" " ."'
        send_mail('New User Account Created', msg,'workmail052020@gmail.com',[ email, 'sadaf.shaikh@udaan.com', 'rahul.gandhi@udaan.com'],fail_silently=False)
        # print("after")
        # return HttpResponse("success")
        messages.success(request, "User Created Successfully")
        return redirect('csp_app:user')
        # except IntegrityError:
        #     return HttpResponse("choose unique username")
    return render(request, 'csp_app/create_user.html', {})


@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  disable_user(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get("disable_id")
            if user_id == None:
                messages.warning(request, "Username Not Found")
                return redirect('csp_app:user')
            selected_user = User.objects.get(pk = user_id)
            selected_user.is_active = False
            selected_user.save()
            messages.success(request, "User Disabled")
            return redirect('csp_app:user')
        return render(request, 'csp_app/create_user.html', {})        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
@user_passes_test(lambda u: u.groups.filter(name='Admin').exists())
def  enable_user(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get("enable_id")
            if user_id == None:
                messages.warning(request, "Username Not Found")
                return redirect('csp_app:user')
            selected_user = User.objects.get(pk = user_id)
            selected_user.is_active = True
            selected_user.save()
            messages.success(request, "User Enabled")
            return redirect('csp_app:user')
        return render(request, 'csp_app/create_user.html', {})        
    except UnboundLocalError:
        return HttpResponse("No Data To Display.")

@login_required(login_url='/notlogin/')
def  index(request):
    return HttpResponse("Hello Sdf")

@login_required(login_url='/notlogin/')
def  admin(request):
    return render(request, 'csp_app/adminhome.html', {})




def csp_login(request):
    if request.method == "POST":
        if request.POST.get('empcode') == None:
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
                print(group_name)
                print(usrname)

                print(request.user.groups.all()[0].name)
                print(request.session.session_key)
                # print(type(group_name))
                # print(str(group_name))
                # print(str(group_name) == 'Admin')
                if str(group_name) == 'Admin':
                    print("here")
                    messages.success(request, "Login Successfull")
                    return redirect('csp_app:entity')
                elif str(group_name) == 'Vendor':
                    print("here 2")
                    messages.success(request, "Login Successfull")
                    return redirect('csp_app:candidate')
                else:
                    print("here3")
                    messages.success(request, "Login Successfull")
                    return redirect('csp_app:candidate')
            else:
                messages.add_message(request, messages.ERROR, "Invalid Credentials")
                return redirect('csp_app:login')
    return render(request, 'csp_app/Login.html', {})

@login_required(login_url='/notlogin/')
def  csp_logout(request):
    logout(request)
    return redirect('csp_app:login')


def notlogin(request):
    return render(request, 'csp_app/timeout.html', {})

