from django.db import models
from django.utils.timezone import now
from pytz import timezone
from django.utils.timezone import make_aware, localtime
from django.contrib.auth.models import User

# Create your models here.
class Role(models.Model):
    role_name = models.CharField(max_length=30,default='')
    email = models.EmailField(unique=True,default='')

    def __str__(self):
        return f"{self.email} {self.role_name}"
    
class Employee(models.Model):
    # user = models.OneToOneField(User,default='', on_delete=models.CASCADE)
    cust_user_id = models.CharField(max_length=8,primary_key=True,default='')
    fname = models.CharField(max_length=100)  
    lname = models.CharField(max_length=100)  
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    # gender = models.CharField(max_length=100)
    age = models.IntegerField()
    password = models.CharField(max_length=128,default='')
    # role = models.ForeignKey(Role,on_delete=models.CASCADE)
    
    is_user = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.fname} {self.lname} {self.email}"
    
class AddApps(models.Model):
    app_name = models.CharField(primary_key=True,max_length=100)
    app_link = models.CharField(max_length=100,default='')
    app_category = models.CharField(max_length=100)     
    sub_category  = models.CharField(max_length=100) 
    image = models.ImageField(upload_to='app_images/', null=True, blank=True)
    created_at = models.DateTimeField(default=now, editable=False)


    def __str__(self):
        # tt = self.created_at.strftime('%d-%m-%Y %I:%M %p')
        # print("tt",tt)
        # created_at=now()
        # print("created at ",created_at)
        utc_aware_time = self.created_at


        local_timezone = timezone('Asia/Kolkata')
        local_time = utc_aware_time.astimezone(local_timezone)

        # Format and print
        formatted_time = local_time.strftime('%d-%m-%Y %I:%M:%S %p %Z')
        print("Local Time:", formatted_time)

        return f"{self.app_name}"


    class Meta:
        ordering = ['created_at'] 

class Points(models.Model): 
    # id = models.IntegerField(primary_key=True, default='')
    points = models.IntegerField()
    app_name = models.ForeignKey(AddApps,on_delete=models.CASCADE, default='') 

    def __str__(self):
        return f"  {self.app_name}"
