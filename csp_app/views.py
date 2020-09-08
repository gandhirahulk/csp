from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from csp_app.models import status, master_candidate, master_entity, master_designation, master_agency, master_department, master_function, master_team, master_sub_team, master_region, master_state, master_city, master_location
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.decorators import login_required


active_status = status.objects.get(pk=1)

def candidate(request):
    return render(request, 'csp_app/candidates.html', {})

def entity(request):
    entity_list = master_entity.objects.filter(status = active_status)
    return render(request, 'csp_app/entity.html', {'entity_list': entity_list})

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
            new_entity = master_entity(entity_name= entity_name, created_by = "user")
            new_entity.save()
            messages.success(request, "Entity Created Successfully")
            return redirect('csp_app:entity')
    return render(request, 'csp_app/entity.html', {})

def agency(request):
    entity_list = master_entity.objects.filter(status = active_status)
    agency_list = master_agency.objects.filter(status = active_status)

    return render(request, 'csp_app/agency.html', {'entity_list': entity_list, 'agency_list': agency_list})

def create_agency(request):
    if request.method == 'POST':
        agency_name = request.POST.get("agency_name")
        agency_spoc = request.POST.get("agency_spoc")
        agency_phone = request.POST.get("agency_phone")
        agency_email = request.POST.get("agency_email")
        agency_email_pwd = request.POST.get("agency_email_pwd")
        entity = request.POST.get("agency_entity")
        if entity == None:
            messages.warning(request, "Choose Entity And Try Again")
            return redirect('csp_app:agency')
        entity_fk = master_entity.objects.get(pk=entity)
        try:
            duplicate_agency_entity_spoc = master_agency.objects.filter(agency_name=agency_name, fk_entity_code= entity, spoc_name=agency_spoc, status = active_status)
            if duplicate_agency_entity_spoc:
                messages.error(request, "Agency Already Exist")
                return redirect('csp_app:agency')
        except ObjectDoesNotExist:
            pass
        try:
            duplicate_agency_email = master_agency.objects.filter( agency_email_id= agency_email, status = active_status)
            if duplicate_agency_email:
                messages.error(request, "Agency Email ID Already Exist")
                return redirect('csp_app:agency')
        except ObjectDoesNotExist:
            pass
        try:
            duplicate_agency_entity = master_agency.objects.filter( agency_name=agency_name, fk_entity_code= entity, status = active_status)
            if duplicate_agency_entity:                
                messages.error(request, "Agency Already Exist")
                return redirect('csp_app:agency')
        except ObjectDoesNotExist:            
            new_agency = master_agency(agency_name= agency_name, spoc_name= agency_spoc, agency_phone_number= agency_phone, agency_email_id= agency_email, agency_email_id_password= agency_email_pwd, fk_entity_code= entity_fk, created_by = "user")
            new_agency.save()
            messages.success(request, "Agency Saved Successfully")
            return redirect('csp_app:agency')
    return render(request, 'csp_app/agency.html', {})

def department(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    return render(request, 'csp_app/department.html', {'entity_list': entity_list, 'department_list': dept_list})

def create_department(request):
    
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
            new_department = master_department(department_name= dept_name, fk_entity_code= entity_fk, created_by = "user")
            new_department.save()
            return redirect('csp_app:department')
    return render(request, 'csp_app/department.html', {})

def function(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    return render(request, 'csp_app/function.html', {'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list})

def create_function(request):
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
            new_function = master_function( function_name= function_name, fk_department_code= department_fk, created_by = "user")
            new_function.save()
            messages.success(request, "Function Saved Successfully")
            return redirect('csp_app:function')
    return render(request, 'csp_app/function.html', {})

def team(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)

    return render(request, 'csp_app/team.html', {'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list})

def create_team(request):
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
            duplicate_team = master_team.objects.get( team_name= team_name, fk_function_code=function_fk, created_by = "user")
            messages.error(request, "Team Already Exist")
            return redirect('csp_app:team')
        except ObjectDoesNotExist: 
            new_team = master_team( team_name= team_name, fk_function_code=function_fk, created_by = "user")
            new_team.save()
            messages.success(request, "Team Saved Successfully")
            return redirect('csp_app:team')
    return render(request, 'csp_app/team.html', {})

def subteam(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)
    subteam_list = master_sub_team.objects.filter(status = active_status)
    return render(request, 'csp_app/subteam.html', {'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list})

def create_subteam(request):

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
            new_subteam = master_sub_team( sub_team_name= subteam_name, fk_team_code=team_fk, created_by = "user")
            new_subteam.save()
            messages.success(request, "Sub Team Saved Successfully")
            return redirect('csp_app:subteam')
    return render(request, 'csp_app/subteam.html', {})

def designation(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)
    subteam_list = master_sub_team.objects.filter(status = active_status)
    desg_list = master_designation.objects.filter(status = active_status)
    return render(request, 'csp_app/designation.html', {'entity_list': entity_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list})

def create_designation(request):
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

            new_designation = master_designation( designation_name= designation_name, fk_sub_team_code=subteam_fk, created_by = "user")
            new_designation.save()
            messages.success(request, "Designation Saved Successfully")
            return redirect('csp_app:designation')
    return render(request, 'csp_app/designation.html', {})

def region(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)
    subteam_list = master_sub_team.objects.filter(status = active_status)
    desg_list = master_designation.objects.filter(status = active_status)
    region_list = master_region.objects.filter(status = active_status)
    return render(request, 'csp_app/region.html', {'entity_list': entity_list,'region_list': region_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list})


def create_region(request):
    if request.method == 'POST':
        region_name = request.POST.get("region_name")
        desg = request.POST.get("region_desg")
        if desg == None:
            messages.warning(request, "Choose Designation And Try Again")
            return redirect('csp_app:region')
        if region_name == None:
            messages.warning(request, "Region Cannot Be Blank")
            return redirect('csp_app:region')
        desg_fk = master_designation.objects.get(pk=desg)
        try:
            dup_region = master_region.objects.get( region_name= region_name, fk_designation_code =desg_fk, status = active_status)

            messages.error(request, "Region Already Exist")
            return redirect('csp_app:region')
        except ObjectDoesNotExist: 
            new_region = master_region( region_name= region_name, fk_designation_code =desg_fk, created_by = "user")
            new_region.save()
            
            messages.success(request, "Region Saved Succesfully")
            return redirect('csp_app:region')
    return render(request, 'csp_app/region.html', {})

def state(request):
    entity_list = master_entity.objects.filter(status = active_status)
    dept_list = master_department.objects.filter(status = active_status)
    function_list = master_function.objects.filter(status = active_status)
    team_list = master_team.objects.filter(status = active_status)
    subteam_list = master_sub_team.objects.filter(status = active_status)
    desg_list = master_designation.objects.filter(status = active_status)
    region_list = master_region.objects.filter(status = active_status)
    state_list = master_state.objects.filter(status = active_status)
    return render(request, 'csp_app/state.html', {'entity_list': entity_list, 'state_list':state_list, 'region_list': region_list, 'department_list': dept_list, 'function_list': function_list, 'team_list': team_list, 'sub_team_list': subteam_list, 'designation_list': desg_list})

def create_state(request):
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
            new_state = master_region( state_name= state_name, fk_region_code =region_fk, created_by = "user")
            new_state.save()
            messages.success(request, "State Saved Successfully")
            return redirect('csp_app:state')
    return render(request, 'csp_app/state.html', {})

def city(request):
    return render(request, 'csp_app/city.html', {})

def create_city(request):
    return render(request, 'csp_app/city.html', {})

def location(request):
    return render(request, 'csp_app/location.html', {})

def create_location(request):
    return render(request, 'csp_app/location.html', {})

def create_user(request):
    if request.method == 'POST':
        usrname = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        try:
            user = User.objects.create_user(usrname)
            password = User.objects.make_random_password()
            print(password)
            user.password = password
            user.set_password(user.password)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.save()
            msg = 'username ' + usrname + " | password " + password
            send_mail('Account Created', msg,'sadaf.shaikh@udaan.com',[email],fail_silently=False,)
            return HttpResponse("user created try to login or check django admin users")
        except IntegrityError:
            return HttpResponse("choose unique username")
    return render(request, 'csp_app/create_user.html', {})


def disable_user(request):
    return render(request, 'csp_app/disableuser.html', {})

def index(request):
    return HttpResponse("Hello Sdf")

def admin(request):
    return render(request, 'csp_app/adminhome.html', {})

def vendor(request):
    return HttpResponse("Hello Vendor")


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
            if user is not None:
                login(request, user)
                if request.user.is_staff:
                    return redirect('csp_app:entity')
                # if user.is_s
                if usrname == 'vendor':
                    messages.success(request, "Login Successfull")
                    return redirect('csp_app:vendor')
                # elif usrname == 'admin':
                #     messages.success(request, "Login Successfull")
                #     return redirect('csp_app:admin')
                else:
                    messages.success(request, "Login Successfull")
                    return redirect('csp_app:candidate')
            else:
                messages.add_message(request, messages.ERROR, "Invalid Credentials")
                return redirect('csp_app:login')
    return render(request, 'csp_app/Login.html', {})

def csp_logout(request):
    logout(request)
    return redirect('csp_app:login')

