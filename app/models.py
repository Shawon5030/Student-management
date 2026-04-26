from django.db import models


class Students(models.Model):

    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    
    # Academic Information
    semester = models.IntegerField()
    roll = models.IntegerField(unique=True)
    reg = models.IntegerField(unique=True)
    session = models.CharField(max_length=20)
    shift = models.CharField(max_length=10, choices=[('Morning', 'Morning'), ('Day', 'Day')])
    section = models.CharField(max_length=5,blank=True,null=True)
    
    # Contact Information
    mobile_number = models.CharField(max_length=15)
    alternate_mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    present_address = models.TextField()
    permanent_address = models.TextField()
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)
    
    # Other Information
    nationality = models.CharField(max_length=50, default='Bangladeshi')
    religion = models.CharField(max_length=30, blank=True, null=True)

    
    # Photo
    profile_picture = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    
class Additional_information(models.Model):
    login_page_image = models.ImageField(upload_to="login_page_image/")