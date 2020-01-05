from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser,BaseUserManager 
from multiselectfield import MultiSelectField
from django.utils.translation import ugettext_lazy as _
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

EDUCATION_CHOICES = [
    ('GED', 'GED'),
    ('HIGH SCHOOL DIPLOMA', 'HIGH SCHOOL DIPLOMA'),
    ('COLLEGE DEGREE', 'COLLEGE DEGREE'),
]
CERTIFICATE_CHOCIES=[
('HVAC','HVAC'),
('CDL','CDL'),
('HEAVY EQUIPMENT','HEAVY EQUIPMENT'),
('FORKLIFT','FORKLIFT'),
('FLAGGER','FLAGGER'),
('ELECTRICAL','ELECTRICAL'),
('MASONRY/CONCRETE','MASONRY/CONCRETE'),
('CONSTRUCTION','CONSTRUCTION'),
('GENERAL LABOR','GENERAL LABOR'),
('SUPERVISOR','SUPERVISOR'),
('OTHER','OTHER'),
]
WORKAREA_CHOCIES=[
('METRO DENVER','METRO DENVER'),
('WESTERN SLOP','WESTERN SLOP'),
('EASTERN COLORADO','EASTERN COLORADO'),
('SOUTHERN COLORADO','SOUTHERN COLORADO'),
('NOTHERN COLORADO','NOTHERN COLORADO'),
('NO RESTRICTIONS','NO RESTRICTIONS'),

]
STATE_CHOICE=[
     ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('AS', 'AS'),
    ('DC', 'DC'),
    ('FM', 'FM'),
    ('GU', 'GU'),
    ('MH', 'MH'),
    ('MP', 'MP'),
    ('PW', 'PW'),
    ('PR', 'PR'),
    ('VI', 'VI'),
]

class RMEC_Employee(models.Model):
   
    last_name = models.CharField(max_length=200,blank=True,null=True,)
    first_name = models.CharField(max_length=200,blank=True,null=True,)
    doc_no=models.IntegerField(verbose_name = "DOC #",unique=True)
    correctional_facility=models.CharField(max_length=100,blank=True,null=True,)
    home_address=models.CharField(max_length=200,blank=True,null=True,)
    city=models.CharField(max_length=200,blank=True,null=True,)
    state=models.CharField(max_length=200,choices=STATE_CHOICE,blank=True,null=True,)
    zip_code=models.CharField(max_length=200,blank=True,null=True,)
    phone=models.CharField(max_length=15,blank=True,null=True,)
    email=models.EmailField(max_length=200,blank=True,null=True,)
    education=models.CharField(max_length=200,choices=EDUCATION_CHOICES,blank=True,null=True,)
    certificate=MultiSelectField(max_length=300,choices=CERTIFICATE_CHOCIES,blank=True,max_choices=11,null=True,)
    work_area=MultiSelectField(max_length=300,choices=WORKAREA_CHOCIES,blank=True,max_choices=6,null=True,)
    job_status=models.BooleanField(default=False)
    hired_date=models.DateField(max_length=200,blank=True,null=True,)
    created_date=models.DateField(max_length=200,blank=True,null=True,)
    updated_date=models.DateField(max_length=200,blank=True,null=True,)
    hired_by=models.CharField(max_length=200,blank=True,null=True,)
  

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    username = None
    email = models.EmailField(unique=True)
    phone=models.CharField(max_length=15,blank=True)
    business_name=models.CharField(max_length=200,blank=True)
    business_address=models.CharField(max_length=200,blank=True)
    city=models.CharField(max_length=200,blank=True)
    state=models.CharField(max_length=200,blank=True,)
    zip_code=models.CharField(max_length=200,blank=True)
    is_active = models.BooleanField(default=False)
    is_passwordreset=models.BooleanField(default=False)
    REQUIRED_FIELDS=[]
    objects = UserManager()


      

