from django.db import models
import datetime

class status(models.Model):
    pk_status_code = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length= 10)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.status_name

class master_entity(models.Model):
    pk_entity_code = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.entity_name

class master_agency(models.Model):
    pk_agency_code = models.AutoField(primary_key=True)
    agency_name = models.CharField(max_length=100)
    fk_entity_code = models.ForeignKey(master_entity, on_delete=models.CASCADE)
    spoc_name = models.CharField(max_length=50)
    agency_phone_number = models.CharField(max_length=10)
    agency_email_id = models.EmailField()
    agency_email_id_password = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.agency_name

class master_department(models.Model):
    pk_department_code = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    fk_entity_code = models.ForeignKey( master_entity, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
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
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
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
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
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
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.sub_team_name

class master_designation(models.Model):
    pk_designation_code = models.AutoField(primary_key=True)
    designation_name = models.CharField(max_length=100)
    fk_sub_team_code = models.ForeignKey(master_sub_team, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.designation_name

class master_region(models.Model):
    pk_region_code = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=100)
    fk_designation_code = models.ForeignKey(master_designation, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.region_name

class master_state(models.Model):
    pk_state_code = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=100)
    fk_region_code = models.ForeignKey(master_region, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.state_name

class master_city(models.Model):
    pk_city_code = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    fk_state_code = models.ForeignKey(master_state, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.city_name

class master_location(models.Model):
    pk_location_code = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=100)
    fk_city_code = models.ForeignKey(master_city, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.location_name

class hiring_type(models.Model):
    pk_hiring_type_code = models.AutoField(primary_key=True)
    hiring_type_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.hiring_type_name

class sub_source(models.Model):
    pk_sub_source_code = models.AutoField(primary_key=True)
    sub_source_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.sub_source_name

class gender(models.Model):
    pk_gender_code = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.gender_name

class laptop_allocation(models.Model):
    pk_laptop_allocation_code = models.AutoField(primary_key=True)
    option_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.option_name

class salary_type(models.Model):
    pk_salary_type_code = models.AutoField(primary_key=True)
    salary_type_name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)

    def __str__(self):
        return self.salary_type_name
    
    
class master_candidate(models.Model):
    pk_candidate_code = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100)
    Middle_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Date_of_Joining = models.DateField()
    Father_Name = models.CharField(max_length=100)
    Date_of_Birth = models.DateField()
    Aadhaar_Number = models.CharField(max_length=12)
    PAN_Number = models.CharField(max_length=10)
    Contact_Number = models.CharField(max_length=10)
    Emergency_Contact_Number = models.CharField(max_length=10)
    Type_of_Hiring = models.ForeignKey( hiring_type, on_delete=models.CASCADE)
    Replacement = models.CharField(max_length=20) #should come from employees table ?
    Sub_Source = models.ForeignKey(sub_source, on_delete=models.CASCADE)
    Referral = models.CharField(max_length=20) #should come from employees table ?
    Agency = models.ForeignKey(master_agency, on_delete=models.CASCADE)
    Entity = models.ForeignKey(master_entity, on_delete=models.CASCADE)
    Department = models.ForeignKey(master_department, on_delete=models.CASCADE)
    Function = models.ForeignKey(master_function, on_delete=models.CASCADE)
    Team = models.ForeignKey(master_team, on_delete=models.CASCADE)
    Sub_Team = models.ForeignKey(master_sub_team, on_delete=models.CASCADE)
    Designation = models.ForeignKey(master_designation, on_delete=models.CASCADE)
    Region = models.ForeignKey(master_region, on_delete=models.CASCADE)
    State = models.ForeignKey(master_state, on_delete=models.CASCADE)
    City = models.ForeignKey(master_city, on_delete=models.CASCADE)
    Location = models.ForeignKey(master_location, on_delete=models.CASCADE)
    Reporting_Manager = models.CharField(max_length=20) #should come from employees table ?
    Reporting_Manager_E_Mail_ID = models.CharField(max_length=100) #should come from employees table ?
    Gender = models.ForeignKey(gender, on_delete=models.CASCADE)
    E_Mail_ID_Creation = models.CharField(max_length=10)
    Laptop_Allocation = models.ForeignKey(laptop_allocation, on_delete=models.CASCADE)
    Salary_Type = models.ForeignKey(salary_type, on_delete=models.CASCADE)
    Gross_Salary_Amount = models.FloatField()
    created_by = models.CharField(max_length=100, default="User")
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = status = models.ForeignKey(status, on_delete=models.CASCADE, default= 1)
