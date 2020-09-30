from django.db import models
import datetime

class status(models.Model):
    pk_status_code = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length= 10)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.status_name

class skill_type(models.Model):
    pk_skill_code = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=20)

    def __str__(self):
        return self.skill_name

class states(models.Model):
    pk_state_code = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=50)

    def __str__(self):
        return self.state_name

class zones(models.Model):
    pk_zone_code = models.AutoField(primary_key=True)
    zone_name = models.CharField(max_length=50)

    def __str__(self):
        return self.zone_name

class master_minimum_wages(models.Model):
    pk_minimum_wages_code = models.AutoField(primary_key=True)
    fk_state_code = models.ForeignKey(states, on_delete=models.CASCADE)
    fk_zone_code = models.ForeignKey(zones, on_delete=models.CASCADE)
    fk_skill_code = models.ForeignKey(skill_type, on_delete=models.CASCADE)
    wages = models.FloatField()
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)



    

class master_entity(models.Model):
    pk_entity_code = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.entity_name
    
    class Meta:
        get_latest_by = 'created_date_time'



class port_list(models.Model):
    pk_port_code = models.AutoField(primary_key=True)
    port = models.IntegerField()
    ssl = models.BooleanField()
    tls = models.BooleanField()

class master_vendor(models.Model):
    pk_vendor_code = models.AutoField(primary_key=True)
    vendor_name = models.CharField(max_length=100)
    fk_entity_code = models.ForeignKey(master_entity, on_delete=models.CASCADE)
    spoc_name = models.CharField(max_length=50)
    spoc_email_id = models.EmailField()
    vendor_phone_number = models.CharField(max_length=10)
    vendor_email_id = models.EmailField()
    vendor_email_id_password = models.CharField(max_length=100)
    vendor_smtp = models.CharField(max_length=100)
    vendor_email_port = models.ForeignKey(port_list, on_delete= models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.vendor_name

class master_department(models.Model):
    pk_department_code = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    fk_entity_code = models.ForeignKey( master_entity, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.department_name

class master_function(models.Model):
    pk_function_code = models.AutoField(primary_key=True)
    function_name = models.CharField(max_length=100)
    fk_department_code = models.ForeignKey(master_department, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.function_name

class master_team(models.Model):
    pk_team_code = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    fk_function_code = models.ForeignKey(master_function, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.team_name

class master_sub_team(models.Model):
    pk_sub_team_code = models.AutoField(primary_key=True)
    sub_team_name = models.CharField(max_length=100)
    fk_team_code = models.ForeignKey(master_team, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.sub_team_name

class master_designation(models.Model):
    pk_designation_code = models.AutoField(primary_key=True)
    designation_name = models.CharField(max_length=100)
    fk_sub_team_code = models.ForeignKey(master_sub_team, on_delete=models.CASCADE)
    fk_skill_code = models.ForeignKey(skill_type, on_delete= models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.designation_name

class master_region(models.Model):
    pk_region_code = models.AutoField(primary_key=True)
    region_name = models.ForeignKey(zones, on_delete=models.CASCADE, default=1)
    fk_entity_code = models.ForeignKey(master_entity, on_delete=models.CASCADE, default=1)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.region_name.zone_name

class master_state(models.Model):
    pk_state_code = models.AutoField(primary_key=True)
    state_name = models.ForeignKey(states, models.CASCADE, default=1)
    fk_region_code = models.ForeignKey(master_region, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.state_name.state_name

class master_city(models.Model):
    pk_city_code = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    fk_state_code = models.ForeignKey(master_state, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.city_name

class master_location(models.Model):
    pk_location_code = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=100)
    location_code = models.CharField(max_length=20)
    fk_city_code = models.ForeignKey(master_city, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.location_name

class hiring_type(models.Model):
    pk_hiring_type_code = models.AutoField(primary_key=True)
    hiring_type_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.hiring_type_name

class sub_source(models.Model):
    pk_sub_source_code = models.AutoField(primary_key=True)
    sub_source_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.sub_source_name

class gender(models.Model):
    pk_gender_code = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.gender_name

class laptop_allocation(models.Model):
    pk_laptop_allocation_code = models.AutoField(primary_key=True)
    option_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.option_name

class salary_type(models.Model):
    pk_salary_type_code = models.AutoField(primary_key=True)
    salary_type_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.salary_type_name
    
class candidate_status(models.Model):
    pk_status_code = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.status_name

class onboarding_status(models.Model):
    pk_status_code = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.status_name

class vendor_status(models.Model):
    pk_status_code = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.status_name
    

class master_candidate(models.Model):
    pk_candidate_code = models.CharField(primary_key=True, max_length=10)
    First_Name = models.CharField(max_length=100)
    Middle_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Date_of_Birth = models.CharField(max_length=20)
    Contact_Number = models.CharField(max_length=10)
    Emergency_Contact_Number = models.CharField(max_length=10)
    Personal_Email_Id = models.CharField( max_length=100)
    Gender = models.ForeignKey(gender, on_delete=models.CASCADE)
    Father_Name = models.CharField(max_length=100)
    Father_Date_of_Birth = models.CharField(max_length=20)
    Aadhaar_Number = models.CharField(max_length=12)
    PAN_Number = models.CharField(max_length=10)
    Type_of_Hiring = models.ForeignKey( hiring_type, on_delete=models.CASCADE)
    Date_of_Joining = models.CharField(max_length=20)
    Replacement = models.CharField(max_length=20, null=True, blank=True) #should come from employees table ?
    Referral = models.CharField(max_length=20, null=True, blank=True) #should come from employees table ?
    Sub_Source = models.ForeignKey(sub_source, on_delete=models.CASCADE)
    fk_entity_code = models.ForeignKey(master_entity, on_delete=models.CASCADE)
    fk_vendor_code = models.ForeignKey(master_vendor, on_delete=models.CASCADE)
    fk_department_code = models.ForeignKey(master_department, on_delete=models.CASCADE)
    fk_function_code = models.ForeignKey(master_function, on_delete=models.CASCADE)
    fk_team_code = models.ForeignKey(master_team, on_delete=models.CASCADE)
    fk_subteam_code = models.ForeignKey(master_sub_team, on_delete=models.CASCADE)
    fk_designation_code = models.ForeignKey(master_designation, on_delete=models.CASCADE)
    fk_region_code = models.ForeignKey(master_region, on_delete=models.CASCADE)
    fk_state_code = models.ForeignKey(master_state, on_delete=models.CASCADE)
    fk_city_code = models.ForeignKey(master_city, on_delete=models.CASCADE)
    fk_location_code = models.ForeignKey(master_location, on_delete=models.CASCADE)
    location_code = models.CharField(max_length=10)#not_sure
    TA_Spoc_Email_Id = models.EmailField()
    Onboarding_Spoc_Email_Id = models.EmailField()
    Reporting_Manager = models.CharField(max_length=20) #should come from employees table ?
    Reporting_Manager_E_Mail_ID = models.CharField(max_length=100) #should come from employees table ?
    E_Mail_ID_Creation = models.CharField(max_length=10)
    Laptop_Allocation = models.ForeignKey(laptop_allocation, on_delete=models.CASCADE)
    Salary_Type = models.ForeignKey(salary_type, on_delete=models.CASCADE)
    Gross_Salary_Amount = models.FloatField()
    candidate_status = models.ForeignKey( candidate_status, on_delete=models.CASCADE, default=2)
    onboarding_status = models.ForeignKey( onboarding_status, on_delete=models.CASCADE, default=2)
    vendor_status = models.ForeignKey( vendor_status, on_delete=models.CASCADE, default=2)

    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)


    def __str__(self):
        return self.pk_candidate_code


class dummy_candidate(models.Model):
    pk_candidate_code = models.CharField(primary_key=True, max_length=10)
    First_Name = models.CharField(max_length=100)
    Middle_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Date_of_Birth = models.CharField(max_length=20)
    Contact_Number = models.CharField(max_length=10)
    Emergency_Contact_Number = models.CharField(max_length=10)
    Personal_Email_Id = models.CharField( max_length=100)
    Gender = models.ForeignKey(gender, on_delete=models.CASCADE)
    Father_Name = models.CharField(max_length=100)
    Father_Date_of_Birth = models.CharField(max_length=20)
    Aadhaar_Number = models.CharField(max_length=12)
    PAN_Number = models.CharField(max_length=10)
    Type_of_Hiring = models.ForeignKey( hiring_type, on_delete=models.CASCADE)
    Date_of_Joining = models.CharField(max_length=20)
    Replacement = models.CharField(max_length=20, null=True, blank=True) #should come from employees table ?
    Referral = models.CharField(max_length=20, null=True, blank=True) #should come from employees table ?
    Sub_Source = models.ForeignKey(sub_source, on_delete=models.CASCADE)
    fk_entity_code = models.ForeignKey(master_entity, on_delete=models.CASCADE)
    fk_vendor_code = models.ForeignKey(master_vendor, on_delete=models.CASCADE)
    fk_department_code = models.ForeignKey(master_department, on_delete=models.CASCADE)
    fk_function_code = models.ForeignKey(master_function, on_delete=models.CASCADE)
    fk_team_code = models.ForeignKey(master_team, on_delete=models.CASCADE)
    fk_subteam_code = models.ForeignKey(master_sub_team, on_delete=models.CASCADE)
    fk_designation_code = models.ForeignKey(master_designation, on_delete=models.CASCADE)
    fk_region_code = models.ForeignKey(master_region, on_delete=models.CASCADE)
    fk_state_code = models.ForeignKey(master_state, on_delete=models.CASCADE)
    fk_city_code = models.ForeignKey(master_city, on_delete=models.CASCADE)
    fk_location_code = models.ForeignKey(master_location, on_delete=models.CASCADE)
    location_code = models.CharField(max_length=10)#not_sure
    TA_Spoc_Email_Id = models.EmailField()
    Onboarding_Spoc_Email_Id = models.EmailField()
    Reporting_Manager = models.CharField(max_length=20) #should come from employees table ?
    Reporting_Manager_E_Mail_ID = models.CharField(max_length=100) #should come from employees table ?
    E_Mail_ID_Creation = models.CharField(max_length=10)
    Laptop_Allocation = models.ForeignKey(laptop_allocation, on_delete=models.CASCADE)
    Salary_Type = models.ForeignKey(salary_type, on_delete=models.CASCADE)
    Gross_Salary_Amount = models.FloatField()
    candidate_status = models.ForeignKey( candidate_status, on_delete=models.CASCADE, default=2)
    onboarding_status = models.ForeignKey( onboarding_status, on_delete=models.CASCADE, default=2)
    vendor_status = models.ForeignKey( vendor_status, on_delete=models.CASCADE, default=2)

    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)


    def __str__(self):
        return self.pk_candidate_code

class dummy_candidate_code(models.Model):
    pk_count = models.AutoField(primary_key=True)
    candidate_code = models.CharField(max_length=10)

    def __str__(self):
        return self.candidate_code

class csp_candidate_code(models.Model):
    pk_count = models.AutoField(primary_key=True)
    candidate_code = models.CharField(max_length=10)

    def __str__(self):
        return self.candidate_code

class mandatory_documents(models.Model):
    pk_mandatory_code = models.AutoField(primary_key=True)
    document_name = models.CharField(max_length=50)

    def __str__(self):
        return self.document_name
    

class candidate_document(models.Model):
    pk_document_code = models.AutoField(primary_key=True)
    fk_candidate_code = models.ForeignKey(master_candidate, on_delete=models.CASCADE)
    document_catagory = models.ForeignKey( mandatory_documents, on_delete=models.CASCADE, default=1)
    file_name = models.CharField(max_length=200)
    file_upload = models.FileField(upload_to='documents/')
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

class candidate_salary(models.Model):
    pk_salary_code = models.AutoField(primary_key=True)
    candidate_code = models.ForeignKey(master_candidate, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(  blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)


class salary_structure_particulars(models.Model):
    pk_ssp_code = models.AutoField(primary_key=True)
    particulars = models.CharField(max_length=100)

    def __str__(self):
        return self.particulars

class employee_contributions_particulars(models.Model):
    pk_ecp_code = models.AutoField(primary_key=True)
    particulars = models.CharField(max_length=100)

    def __str__(self):
        return self.particulars

class employer_contributions_particulars(models.Model):
    pk_ercp_code = models.AutoField(primary_key=True)
    particulars = models.CharField(max_length=100)

    def __str__(self):
        return self.particulars
    

    