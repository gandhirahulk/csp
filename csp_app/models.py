from django.db import models

class master_entity(models.Model):
    pk_entity_code = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=10, default="Active")

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
    status = models.CharField(max_length=10, default="Active")

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
    status = models.CharField(max_length=10, default="Active")

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
    status = models.CharField(max_length=10, default="Active")

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
    status = models.CharField(max_length=10, default="Active")

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
    status = models.CharField(max_length=10, default="Active")

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
    status = models.CharField(max_length=10, default="Active")

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
    status = models.CharField(max_length=10, default="Active")

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
    status = models.CharField(max_length=10, default="Active")

    def __str__(self):
        return self.state_name

class master_city(models.Model):
    pk_city_code = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    fk_region_code = models.ForeignKey(master_region, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True,blank=True)
    modified_date_time = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=10, default="Active")

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
    status = models.CharField(max_length=10, default="Active")

    def __str__(self):
        return self.location_name
    
