import xlwt
from csp_app.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.utils import timezone
now_aware = timezone.now()

active_status = status.objects.get(pk=1)

def export_entity(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_Entity.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Entity')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['Entity Code', 'Entity Name', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_entity.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_entity_code, font_style)
        ws.write(row_num, 1, row.entity_name, font_style)
        ws.write(row_num, 2, row.created_by, font_style)
        ws.write(row_num, 3, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 4, row.modified_by, font_style)
        try:
            ws.write(row_num, 5, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 5, 'None', font_style)
        ws.write(row_num, 6, row.status.status_name, font_style)     
 
    wb.save(response)
    return response


def export_vendor(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_Vendor.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Vendor')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['Vendor Code', 'Entity','Vendor Name','Phone Number', 'Email','SMTP', 'PORT', 'SPOC', 'SPOC Mail ID', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_vendor.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_vendor_code, font_style)
        ws.write(row_num, 1, row.fk_entity_code.entity_name, font_style)
        ws.write(row_num, 2, row.vendor_name, font_style)
        ws.write(row_num, 3, row.vendor_phone_number, font_style)
        ws.write(row_num, 4, row.vendor_email_id, font_style)
        ws.write(row_num, 5, row.vendor_smtp, font_style)
        ws.write(row_num, 6, row.vendor_email_port.port, font_style)
        ws.write(row_num, 7, row.spoc_name, font_style)
        ws.write(row_num, 8, row.spoc_email_id, font_style)
        ws.write(row_num, 9, row.created_by, font_style)
        ws.write(row_num, 10, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 11, row.modified_by, font_style)
        try:
            ws.write(row_num, 12, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 12, 'None', font_style)
        ws.write(row_num, 13, row.status.status_name, font_style)     
 
    wb.save(response)
    return response


def export_department(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_Department.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Department')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['Department Code','Entity Name', 'Department Name', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_department.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_department_code, font_style)
        ws.write(row_num, 1, row.fk_entity_code.entity_name, font_style)
        ws.write(row_num, 2, row.department_name, font_style)
        ws.write(row_num, 3, row.created_by, font_style)
        ws.write(row_num, 4, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 5, row.modified_by, font_style)
        print(type(row.modified_date_time))
        try:
            ws.write(row_num, 6, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 6, 'None', font_style)
        ws.write(row_num, 7, row.status.status_name, font_style)     
 
    wb.save(response)
    return response


def export_function(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_Function.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Function')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['Function Code','Entity Name', 'Department Name', 'Function Name', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_function.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_function_code, font_style)
        ws.write(row_num, 1, row.fk_department_code.fk_entity_code.entity_name, font_style)
        ws.write(row_num, 2, row.fk_department_code.department_name, font_style)

        ws.write(row_num, 3, row.function_name, font_style)
        ws.write(row_num, 4, row.created_by, font_style)
        ws.write(row_num, 5, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 6, row.modified_by, font_style)
        try:
            ws.write(row_num, 7, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 7, 'None', font_style)
        ws.write(row_num, 8, row.status.status_name, font_style)     
 
    wb.save(response)
    return response

def export_team(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_Team.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Team')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['Team Code','Entity', 'Department', 'Function', 'Team Name', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_team.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_team_code, font_style)
        ws.write(row_num, 1, row.fk_function_code.fk_department_code.fk_entity_code.entity_name, font_style)
        ws.write(row_num, 2, row.fk_function_code.fk_department_code.department_name, font_style)
        ws.write(row_num, 3, row.fk_function_code.function_name, font_style)

        ws.write(row_num, 4, row.team_name, font_style)
        ws.write(row_num, 5, row.created_by, font_style)
        ws.write(row_num, 6, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 7, row.modified_by, font_style)
        print(type(row.modified_date_time))
        try:
            ws.write(row_num, 8, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 8, 'None', font_style)
        ws.write(row_num, 9, row.status.status_name, font_style)     
 
    wb.save(response)
    return response

def export_sub_team(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_Sub_Team.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sub_Team')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['Sub_Team Code','Entity', 'Department', 'Function', 'Team','Sub Team Name', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_sub_team.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_sub_team_code, font_style)
        ws.write(row_num, 1, row.fk_team_code.fk_function_code.fk_department_code.fk_entity_code.entity_name, font_style)
        ws.write(row_num, 2, row.fk_team_code.fk_function_code.fk_department_code.department_name, font_style)
        ws.write(row_num, 3, row.fk_team_code.fk_function_code.function_name, font_style)
        ws.write(row_num, 4, row.fk_team_code.team_name , font_style)

        ws.write(row_num, 5, row.sub_team_name, font_style)
        ws.write(row_num, 6, row.created_by, font_style)
        ws.write(row_num, 7, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 8, row.modified_by, font_style)
        print(type(row.modified_date_time))
        try:
            ws.write(row_num, 9, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 9, 'None', font_style)
        ws.write(row_num, 10, row.status.status_name, font_style)     
 
    wb.save(response)
    return response

def export_designation(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_Designation.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Designation')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['Designation Code','Entity', 'Department', 'Function', 'Team','Sub Team','Skill Type', 'Designation' , 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_designation.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_designation_code, font_style)
        ws.write(row_num, 1, row.fk_sub_team_code.fk_team_code.fk_function_code.fk_department_code.fk_entity_code.entity_name, font_style)
        ws.write(row_num, 2, row.fk_sub_team_code.fk_team_code.fk_function_code.fk_department_code.department_name, font_style)
        ws.write(row_num, 3, row.fk_sub_team_code.fk_team_code.fk_function_code.function_name, font_style)
        ws.write(row_num, 4, row.fk_sub_team_code.fk_team_code.team_name , font_style)
        ws.write(row_num, 5, row.fk_sub_team_code.sub_team_name , font_style)
        ws.write(row_num, 6, row.fk_skill_code.skill_name , font_style)

        ws.write(row_num, 7, row.designation_name, font_style)
        ws.write(row_num, 8, row.created_by, font_style)
        ws.write(row_num, 9, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 10, row.modified_by, font_style)
        print(type(row.modified_date_time))
        try:
            ws.write(row_num, 11, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 11, 'None', font_style)
        ws.write(row_num, 12, row.status.status_name, font_style)     
 
    wb.save(response)
    return response

def export_region(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_Region.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Region')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['Region Code','Entity Name', 'Region Name', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_region.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_region_code, font_style)
        ws.write(row_num, 1, row.fk_entity_code.entity_name, font_style)
        ws.write(row_num, 2, row.region_name, font_style)
        ws.write(row_num, 3, row.created_by, font_style)
        ws.write(row_num, 4, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 5, row.modified_by, font_style)
        print(type(row.modified_date_time))
        try:
            ws.write(row_num, 6, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 6, 'None', font_style)
        ws.write(row_num, 7, row.status.status_name, font_style)     
 
    wb.save(response)
    return response

def export_state(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_State.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('State')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['State Code','Entity Name', 'Region Name', 'State Name', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_state.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_state_code, font_style)
        ws.write(row_num, 1, row.fk_region_code.fk_entity_code.entity_name, font_style)
        ws.write(row_num, 2, row.fk_region_code.region_name, font_style)

        ws.write(row_num, 3, row.state_name, font_style)
        ws.write(row_num, 4, row.created_by, font_style)
        ws.write(row_num, 5, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 6, row.modified_by, font_style)
        try:
            ws.write(row_num, 7, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 7, 'None', font_style)
        ws.write(row_num, 8, row.status.status_name, font_style)     
 
    wb.save(response)
    return response

def export_city(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_City.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('City')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['City Code','Entity', 'Region', 'State', 'City Name', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_city.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_city_code, font_style)
        ws.write(row_num, 1, row.fk_state_code.fk_region_code.fk_entity_code.entity_name, font_style)
        ws.write(row_num, 2, row.fk_state_code.fk_region_code.region_name, font_style)
        ws.write(row_num, 3, row.fk_state_code.state_name, font_style)

        ws.write(row_num, 4, row.city_name, font_style)
        ws.write(row_num, 5, row.created_by, font_style)
        ws.write(row_num, 6, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 7, row.modified_by, font_style)
        try:
            ws.write(row_num, 8, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 8, 'None', font_style)
        ws.write(row_num, 9, row.status.status_name, font_style)     
 
    wb.save(response)
    return response

def export_location(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_location.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('location')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['location Code','Entity', 'Region', 'Function', 'City','Location Name', 'Location Code', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_location.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_location_code, font_style)
        ws.write(row_num, 1, row.fk_city_code.fk_state_code.fk_region_code.fk_entity_code.entity_name, font_style)
        ws.write(row_num, 2, row.fk_city_code.fk_state_code.fk_region_code.region_name, font_style)
        ws.write(row_num, 3, row.fk_city_code.fk_state_code.state_name, font_style)
        ws.write(row_num, 4, row.fk_city_code.city_name , font_style)

        ws.write(row_num, 5, row.location_name, font_style)
        ws.write(row_num, 6, row.location_code, font_style)

        ws.write(row_num, 7, row.created_by, font_style)
        ws.write(row_num, 8, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 9, row.modified_by, font_style)
        print(type(row.modified_date_time))
        try:
            ws.write(row_num, 10, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 10, 'None', font_style)
        ws.write(row_num, 11, row.status.status_name, font_style)     
 
    wb.save(response)
    return response

def export_minimum_wage(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_Minimum_Wage.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Minimum_Wage')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['Code','State', 'Zone','Skill', 'Wages', 'Created By', 'Created Date Time', 'Modified By', 'Modified Date Time', 'Status', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = master_minimum_wages.objects.filter(status=active_status)
    for row in rows:
        row_num += 1
        ws.write(row_num, 0, row.pk_minimum_wages_code, font_style)
        ws.write(row_num, 1, row.fk_state_code.state_name, font_style)
        ws.write(row_num, 2, row.fk_zone_code.zone_name, font_style)
        ws.write(row_num, 3, row.fk_skill_code.skill_name, font_style)
        ws.write(row_num, 4, row.wages, font_style)

        ws.write(row_num, 5, row.created_by, font_style)
        ws.write(row_num, 6, row.created_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        ws.write(row_num, 7, row.modified_by, font_style)
        try:
            ws.write(row_num, 8, row.modified_date_time.strftime("%Y-%m-%d %H:%M"), font_style)
        except AttributeError:
            ws.write(row_num, 8, 'None', font_style)
        ws.write(row_num, 9, row.status.status_name, font_style)     
 
    wb.save(response)
    return response


def export_user_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CSP_user.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('User')
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
 
    columns = ['Username', 'First name', 'Last name', 'Email address', ]
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
 
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
 
    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
 
    wb.save(response)
    return response

