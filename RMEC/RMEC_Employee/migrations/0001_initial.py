# Generated by Django 2.2.5 on 2019-12-24 09:25

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='RMEC_Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('doc_no', models.IntegerField(unique=True, verbose_name='DOC #')),
                ('correctional_facility', models.CharField(blank=True, max_length=100, null=True)),
                ('home_address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.CharField(blank=True, choices=[('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('AS', 'AS'), ('DC', 'DC'), ('FM', 'FM'), ('GU', 'GU'), ('MH', 'MH'), ('MP', 'MP'), ('PW', 'PW'), ('PR', 'PR'), ('VI', 'VI')], max_length=200, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('education', models.CharField(blank=True, choices=[('GED', 'GED'), ('HIGH SCHOOL DIPLOMA', 'HIGH SCHOOL DIPLOMA'), ('COLLEGE DEGREE', 'COLLEGE DEGREE')], max_length=200, null=True)),
                ('certificate', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('HVAC', 'HVAC'), ('CDL', 'CDL'), ('HEAVY EQUIPMENT', 'HEAVY EQUIPMENT'), ('FORKLIFT', 'FORKLIFT'), ('FLAGGER', 'FLAGGER'), ('ELECTRICAL', 'ELECTRICAL'), ('MASONRY/CONCRETE', 'MASONRY/CONCRETE'), ('CONSTRUCTION', 'CONSTRUCTION'), ('GENERAL LABOR', 'GENERAL LABOR'), ('SUPERVISOR', 'SUPERVISOR'), ('OTHER', 'OTHER')], max_length=300, null=True)),
                ('work_area', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('METRO DENVER', 'METRO DENVER'), ('WESTERN SLOP', 'WESTERN SLOP'), ('EASTERN COLORADO', 'EASTERN COLORADO'), ('SOUTHERN COLORADO', 'SOUTHERN COLORADO'), ('NOTHERN COLORADO', 'NOTHERN COLORADO'), ('NO RESTRICTIONS', 'NO RESTRICTIONS')], max_length=300, null=True)),
                ('job_status', models.BooleanField(default=False)),
                ('hired_date', models.DateField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateField(blank=True, max_length=200, null=True)),
                ('updated_date', models.DateField(blank=True, max_length=200, null=True)),
                ('hired_by', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('business_name', models.CharField(blank=True, max_length=200)),
                ('business_address', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('state', models.CharField(blank=True, max_length=200)),
                ('zip_code', models.CharField(blank=True, max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('is_passwordreset', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
