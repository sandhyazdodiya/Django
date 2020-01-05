
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from RMEC_Employee.models import RMEC_Employee
from django.urls import  reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from django.views.generic import UpdateView,CreateView,DeleteView,ListView
from django.contrib.auth.views import LoginView
import csv,io
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,get_user_model,update_session_auth_hash
from RMEC_Employee.forms import CustomPasswordChangeForm,SignUpForm,AdminSignUpForm,ParticipantForm,CustomPasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import logout
from django.http import HttpResponse
from django.core.mail import EmailMessage
import smtplib
import secrets
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.views import PasswordResetView
from .resources import RMEC_EmployeeResource
import datetime
User = get_user_model()

def export_data_template(request):
    if request.method == 'POST':
        file_format_input = request.POST.get('file_format')
        if(file_format_input == "0"):
            RMEC_Employee_resource = RMEC_EmployeeResource()
            dataset = RMEC_Employee_resource.export()
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="persons.csv"'
        if(file_format_input == "1"):
            RMEC_Employee_resource = RMEC_EmployeeResource()
            dataset = RMEC_Employee_resource.export()
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="persons.xls"'
        return response
    else:
        return render(request, 'export_data.html')


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    pass
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm

def hired_status(request,pk):
        obj= get_object_or_404(RMEC_Employee, id=pk)
        obj.job_status = 1
        obj.hired_by=request.user.id
        obj.save()
        sender_address=settings.EMAIL_HOST_USER
        subject="Partner hired"
        receiver_address="info@eleorex.com"
        message = "Hello admin participant with DOC # " +str(obj.doc_no)+ ",\n\n" + \
                  "is hired by industry partner with email " +str(request.user.email)+ ",\n\n" + \
                  " on date "+str(datetime.datetime.now().date())
        send_mail(sender_address,receiver_address,subject,message)
        return redirect("hiredby_partner")
def hired_status_none(request,pk):
        obj= get_object_or_404(RMEC_Employee, id=pk)
        obj.job_status = 0
        obj.hired_by=None
        obj.save()
        return redirect("not_hired")
def check_admin(user):
   return user.is_superuser
def logout_request(request):
    logout(request)
    return redirect("login")


def login_success(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("participants_list")
        else:
            print(request.user.is_passwordreset)
            if request.user.is_passwordreset is False:
                return redirect("change_password")
            else:
                return redirect('not_hired')
# def login_redirect(request):
#     if request.user.is_authenticated:
#         return redirect("participants_list")
#     else:
#         return redirect("login")

@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():

            user = form.save()
            obj= get_object_or_404(User, email=request.user)
            print(obj)
            obj.is_passwordreset=1
            obj.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('not_hired')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
def send_mail(sender_address,receiver_address,subject, mail_content):
	try:
		print("Sending an email")
		#The mail addresses and password
		# sender_address = 'info@eleorex.com'
		# sender_pass = ''
		# receiver_address = 'sandhyazaverdodiya@gmail.com'
		#Setup the MIME
		message = MIMEMultipart()
		message['From'] = sender_address
		message['To'] = receiver_address
		message['Subject'] = subject   #The subject line
		#The body and the attachments for the mail
		message.attach(MIMEText(mail_content, 'plain'))
		#Create SMTP session for sending the mail
		session = smtplib.SMTP('216.239.232.196', 25) #use gmail with port
		#session.starttls() #enable security
		#session.login(sender_address, sender_pass) #login with mail_id and password
		session.ehlo() #enable security
		text = message.as_string()
		session.sendmail(sender_address, receiver_address, text)
		session.quit()
	except Exception as e:
		print("Exception " + str(e))


def IndustryPartnerRegistration(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            print(password)
            form.save()
            return redirect('thankyou')
    else:
        form = SignUpForm()
        
        
    return render(request,'industry_partner_registration.html',{'form': form})
def Thankyou(request):
   return render(request,'thankyou.html')
@user_passes_test(check_admin)
def Main(request):
    RMEC_Employee_count = RMEC_Employee.objects.count()
    RMEC_Employee_hired=RMEC_Employee.objects.filter(job_status=1).count()
    IndustryPartner_count = User.objects.filter(is_superuser=0).filter(is_active=1).count()
    return render(request,'dashboard.html',{'RMEC_Employee_hired':RMEC_Employee_hired,'RMEC_Employee_count':RMEC_Employee_count,'IndustryPartner_count':IndustryPartner_count})
@login_required(login_url='/accounts/login/')
def Setting_rmec(request):
   return render(request,'settings_rmec.html')
# def Industry_Partners(request):
#    return render(request,'industry_partners.html')

class participants_nothired(LoginRequiredMixin,View):
    def get(self,request):
        last_name_input = request.GET.get('last_name')
        first_name_input = request.GET.get('first_name')
        doc_no_input = request.GET.get('doc_no')
        correctional_facility_input = request.GET.get('correctional_facility')
        home_address_input = request.GET.get('home_address')
        city_input = request.GET.get('city')
        state_input = request.GET.get('state')
        zip_code_input = request.GET.get('zip_code')
        phone_input = request.GET.get('phone')
        email_input = request.GET.get('email')
        education_input = request.GET.get('education')
        certificate_input = request.GET.getlist('certificate[]')
        work_area_input = request.GET.getlist('work_area[]')
        job_status_input = request.GET.get('job_status')
        hired_date_gt_input = request.GET.get('hired_date_gt')
        hired_date_lt_input = request.GET.get('hired_date_lt')
        # created_date_input = request.GET.get('created_date')
        # updated_date_input = request.GET.get('updated_date')

        sql="SELECT * FROM  rmec_employee_rmec_employee WHERE job_status='0'"
        flag = 0
        sql2 = ""
        if last_name_input is not None and last_name_input is not "":
            sql2= " last_name LIKE '%%" +str(last_name_input) +"%%'"
            flag=1
        if first_name_input is not None and first_name_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 +" first_name LIKE '%%" +str(first_name_input) +"%%'"
            flag=1
        if phone_input is not None and phone_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " phone LIKE '%%" +str(phone_input) +"%%'"
            flag=1
        if doc_no_input is not None and doc_no_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " doc_no LIKE '%%" +str(doc_no_input) +"%%'"
            flag=1
        if correctional_facility_input is not None and correctional_facility_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= " correctional_facility LIKE '%%" +str(correctional_facility_input) +"%%'"
            flag=1
        if home_address_input is not None and home_address_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " home_address LIKE '%%" +str(home_address_input) +"%%'"
            flag=1
        if city_input is not None and city_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " city LIKE '%%" +str(city_input) +"%%'"
            flag=1
        if state_input is not None and state_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " state LIKE '%%" +str(state_input) +"%%'"
            flag=1
        if zip_code_input is not None and zip_code_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " zip_code LIKE '%%" +str(zip_code_input) +"%%'"
            flag=1
        if email_input is not None and email_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "

            sql2= sql2 +" email LIKE '%%" +str(email_input) +"%%'"
            flag=1
        if education_input is not None and education_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " education LIKE '%%" +str(education_input) +"%%'"
            flag=1
        if len(certificate_input) != 0:
            if(flag==1):
                 sql2= sql2 + " AND "
            for x in certificate_input:
                sql2= sql2 + " certificate LIKE '%%" + str(x) +"%%'"
                if x != certificate_input[-1]:
                    sql2= sql2 + " OR "
            flag=1

        if len(work_area_input) != 0:
            if(flag==1):
                 sql2= sql2 + " AND "
            for x in work_area_input:
                sql2= sql2 + " work_area LIKE '%%" + str(x) +"%%'"
                if x != work_area_input[-1]:
                    sql2= sql2 + " OR "
            flag=1
        if job_status_input is not None and job_status_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " job_status= '" +str(job_status_input) +"'"
            flag=1
        if hired_date_gt_input is not None and hired_date_gt_input is not "" and hired_date_lt_input is not None and hired_date_lt_input is not "" :
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " hired_date BETWEEN '" + str(hired_date_gt_input) +"' AND '" + str(hired_date_lt_input) +"'"
            flag=1
        if sql2 is not "":
            sql= sql + " AND "

        sql = sql+sql2

        participantss_list = RMEC_Employee.objects.raw(sql)
        paginator = Paginator(participantss_list, 25) # Show 25 contacts per page

        page = request.GET.get('page')
        participantss = paginator.get_page(page)
        if last_name_input is None:
           last_name_input=''
        else:
            last_name_input=last_name_input
        if first_name_input is None:
           first_name_input=''
        else:
            first_name_input=first_name_input
        if doc_no_input is None:
           doc_no_input=''
        else:
            doc_no_input=doc_no_input
        if phone_input is None:
           phone_input=''
        else:
            phone_input=phone_input
        if email_input is None:
           email_input=''
        else:
            email_input=email_input
        if home_address_input is None:
           home_address_input=''
        else:
            home_address_input=home_address_input
        if city_input is None:
           city_input=''
        else:
            city_input=city_input
        if state_input is None:
           state_input=''
        else:
            state_input=state_input
        if zip_code_input is None:
           zip_code_input=''
        else:
            zip_code_input=zip_code_input
        if correctional_facility_input is None:
           correctional_facility_input=''
        else:
            correctional_facility_input=correctional_facility_input

        if hired_date_gt_input is None:
           hired_date_gt_input=''
        else:
            hired_date_gt_input=hired_date_gt_input
        if hired_date_lt_input is None:
           hired_date_lt_input=''
        else:
            hired_date_lt_input=hired_date_lt_input


        return render(request,'not_hired.html',{'participantss':participantss,'sql':sql,'last_name_input':last_name_input,'first_name_input':first_name_input,'doc_no_input':doc_no_input,'phone_input':phone_input,'email_input':email_input,'home_address_input':home_address_input,'city_input':city_input,'state_input':state_input,'zip_code_input':zip_code_input,'correctional_facility_input':correctional_facility_input,'hired_date_gt_input':hired_date_gt_input,'hired_date_lt_input':hired_date_lt_input})


class participants_hired(LoginRequiredMixin,View):
    def get(self,request):
        last_name_input = request.GET.get('last_name')
        first_name_input = request.GET.get('first_name')
        doc_no_input = request.GET.get('doc_no')
        correctional_facility_input = request.GET.get('correctional_facility')
        home_address_input = request.GET.get('home_address')
        city_input = request.GET.get('city')
        state_input = request.GET.get('state')
        zip_code_input = request.GET.get('zip_code')
        phone_input = request.GET.get('phone')
        email_input = request.GET.get('email')
        education_input = request.GET.get('education')
        certificate_input = request.GET.getlist('certificate[]')
        work_area_input = request.GET.getlist('work_area[]')
        job_status_input = request.GET.get('job_status')
        hired_date_gt_input = request.GET.get('hired_date_gt')
        hired_date_lt_input = request.GET.get('hired_date_lt')
        # created_date_input = request.GET.get('created_date')
        # updated_date_input = request.GET.get('updated_date')


        sql="SELECT * FROM  rmec_employee_rmec_employee WHERE job_status= '1' AND hired_by = '"+ str(request.user.id) +"'"
        flag = 0
        sql2 = ""
        if last_name_input is not None and last_name_input is not "":
            sql2= " last_name LIKE '%%" +str(last_name_input) +"%%'"
            flag=1
        if first_name_input is not None and first_name_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 +" first_name LIKE '%%" +str(first_name_input) +"%%'"
            flag=1
        if phone_input is not None and phone_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " phone= '" +str(phone_input) +"'"
            flag=1
        if doc_no_input is not None and doc_no_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " doc_no= '" +str(doc_no_input) +"'"
            flag=1
        if correctional_facility_input is not None and correctional_facility_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= " correctional_facility= '" +str(correctional_facility_input) +"'"
            flag=1
        if home_address_input is not None and home_address_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " home_address= '" +str(home_address_input) +"'"
            flag=1
        if city_input is not None and city_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " city= '" +str(city_input) +"'"
            flag=1
        if state_input is not None and state_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " state= '" +str(state_input) +"'"
            flag=1
        if zip_code_input is not None and zip_code_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " zip_code= '" +str(zip_code_input) +"'"
            flag=1
        if email_input is not None and email_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "

            sql2= sql2 +" email LIKE '%%" +str(email_input) +"%%'"
            flag=1
        if education_input is not None and education_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " education= '" +str(education_input) +"'"
            flag=1
        if len(certificate_input) != 0:
            if(flag==1):
                 sql2= sql2 + " AND "
            for x in certificate_input:
                sql2= sql2 + " certificate LIKE '%%" + str(x) +"%%'"
                if x != certificate_input[-1]:
                    sql2= sql2 + " OR "
            flag=1
            #sql="SELECT * FROM rmec_employee_rmec_employee WHERE (certificate LIKE '%%CDL%%') OR (certificate LIKE '%%general labour%%')"
        if len(work_area_input) != 0:
            if(flag==1):
                 sql2= sql2 + " AND "
            for x in work_area_input:
                sql2= sql2 + " work_area LIKE '%%" + str(x) +"%%'"
                if x != work_area_input[-1]:
                    sql2= sql2 + " OR "
            flag=1
        if job_status_input is not None and job_status_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " job_status= '" +str(job_status_input) +"'"
            flag=1
        if hired_date_gt_input is not None and hired_date_gt_input is not "" and hired_date_lt_input is not None and hired_date_lt_input is not "" :
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " hired_date BETWEEN '" + str(hired_date_gt_input) +"' AND '" + str(hired_date_lt_input) +"'"
            flag=1
        if sql2 is not "":
            sql= sql + " AND "

        sql = sql+sql2

        participantss_list = RMEC_Employee.objects.raw(sql)
        paginator = Paginator(participantss_list, 25) # Show 25 contacts per page

        page = request.GET.get('page')
        participantss = paginator.get_page(page)
        if last_name_input is None:
           last_name_input=''
        else:
            last_name_input=last_name_input
        if first_name_input is None:
           first_name_input=''
        else:
            first_name_input=first_name_input
        if doc_no_input is None:
           doc_no_input=''
        else:
            doc_no_input=doc_no_input
        if phone_input is None:
           phone_input=''
        else:
            phone_input=phone_input
        if email_input is None:
           email_input=''
        else:
            email_input=email_input
        if home_address_input is None:
           home_address_input=''
        else:
            home_address_input=home_address_input
        if city_input is None:
           city_input=''
        else:
            city_input=city_input
        if state_input is None:
           state_input=''
        else:
            state_input=state_input
        if zip_code_input is None:
           zip_code_input=''
        else:
            zip_code_input=zip_code_input
        if correctional_facility_input is None:
           correctional_facility_input=''
        else:
            correctional_facility_input=correctional_facility_input

        if hired_date_gt_input is None:
           hired_date_gt_input=''
        else:
            hired_date_gt_input=hired_date_gt_input
        if hired_date_lt_input is None:
           hired_date_lt_input=''
        else:
            hired_date_lt_input=hired_date_lt_input


        return render(request,'hiredby_partner.html',{'participantss':participantss,'sql':sql,'last_name_input':last_name_input,'first_name_input':first_name_input,'doc_no_input':doc_no_input,'phone_input':phone_input,'email_input':email_input,'home_address_input':home_address_input,'city_input':city_input,'state_input':state_input,'zip_code_input':zip_code_input,'correctional_facility_input':correctional_facility_input,'hired_date_gt_input':hired_date_gt_input,'hired_date_lt_input':hired_date_lt_input})



class DashboardView(LoginRequiredMixin,View):
    def get(self,request):
        last_name_input = request.GET.get('last_name')
        first_name_input = request.GET.get('first_name')
        doc_no_input = request.GET.get('doc_no')
        correctional_facility_input = request.GET.get('correctional_facility')
        home_address_input = request.GET.get('home_address')
        city_input = request.GET.get('city')
        state_input = request.GET.get('state')
        zip_code_input = request.GET.get('zip_code')
        phone_input = request.GET.get('phone')
        email_input = request.GET.get('email')
        education_input = request.GET.get('education')
        certificate_input = request.GET.getlist('certificate[]')
        work_area_input = request.GET.getlist('work_area[]')
        job_status_input = request.GET.get('job_status')
        hired_date_gt_input = request.GET.get('hired_date_gt')
        hired_date_lt_input = request.GET.get('hired_date_lt')
        # created_date_input = request.GET.get('created_date')
        # updated_date_input = request.GET.get('updated_date')

        sql="SELECT * FROM  rmec_employee_rmec_employee "
        flag = 0
        sql2 = ""
        if last_name_input is not None and last_name_input is not "":
            sql2= " last_name LIKE '%%" +str(last_name_input) +"%%'"
            flag=1
        if first_name_input is not None and first_name_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 +" first_name LIKE '%%" +str(first_name_input) +"%%'"
            flag=1
        if phone_input is not None and phone_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " phone LIKE '%%" +str(phone_input) +"%%'"
            flag=1
        if doc_no_input is not None and doc_no_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " doc_no LIKE '%%" +str(doc_no_input) +"%%'"
            flag=1
        if correctional_facility_input is not None and correctional_facility_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= " correctional_facility LIKE '%%" +str(correctional_facility_input) +"%%'"
            flag=1
        if home_address_input is not None and home_address_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " home_address LIKE '%%" +str(home_address_input) +"%%'"
            flag=1
        if city_input is not None and city_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " city LIKE '%%" +str(city_input) +"%%'"
            flag=1
        if state_input is not None and state_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " state LIKE '%%" +str(state_input) +"%%'"
            flag=1
        if zip_code_input is not None and zip_code_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " zip_code LIKE '%%" +str(zip_code_input) +"%%'"
            flag=1
        if email_input is not None and email_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "

            sql2= sql2 +" email LIKE '%%" +str(email_input) +"%%'"
            flag=1
        if education_input is not None and education_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " education LIKE '%%" +str(education_input) +"%%'"
            flag=1
        if len(certificate_input) != 0:
            if(flag==1):
                 sql2= sql2 + " AND "
            for x in certificate_input:
                sql2= sql2 + " certificate LIKE '%%" + str(x) +"%%'"
                if x != certificate_input[-1]:
                    sql2= sql2 + " OR "
            flag=1

        if len(work_area_input) != 0:
            if(flag==1):
                 sql2= sql2 + " AND "
            for x in work_area_input:
                sql2= sql2 + " work_area LIKE '%%" + str(x) +"%%'"
                if x != work_area_input[-1]:
                    sql2= sql2 + " OR "
            flag=1
        if job_status_input is not None and job_status_input is not "":
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " job_status= '" +str(job_status_input) +"'"
            flag=1
        if hired_date_gt_input is not None and hired_date_gt_input is not "" and hired_date_lt_input is not None and hired_date_lt_input is not "" :
            if(flag==1):
                 sql2= sql2 + " AND "
            sql2= sql2 + " hired_date BETWEEN '" + str(hired_date_gt_input) +"' AND '" + str(hired_date_lt_input) +"'"
            flag=1
        if sql2 is not "":
            sql= sql + " WHERE "
        print(sql2)
        sql = sql+sql2+'ORDER BY id DESC'


        if last_name_input is None:
           last_name_input=''
        else:
            last_name_input=last_name_input
        if first_name_input is None:
           first_name_input=''
        else:
            first_name_input=first_name_input
        if doc_no_input is None:
           doc_no_input=''
        else:
            doc_no_input=doc_no_input
        if phone_input is None:
           phone_input=''
        else:
            phone_input=phone_input
        if email_input is None:
           email_input=''
        else:
            email_input=email_input
        if home_address_input is None:
           home_address_input=''
        else:
            home_address_input=home_address_input
        if city_input is None:
           city_input=''
        else:
            city_input=city_input
        if state_input is None:
           state_input=''
        else:
            state_input=state_input
        if zip_code_input is None:
           zip_code_input=''
        else:
            zip_code_input=zip_code_input
        if correctional_facility_input is None:
           correctional_facility_input=''
        else:
            correctional_facility_input=correctional_facility_input

        if hired_date_gt_input is None:
           hired_date_gt_input=''
        else:
            hired_date_gt_input=hired_date_gt_input
        if hired_date_lt_input is None:
           hired_date_lt_input=''
        else:
            hired_date_lt_input=hired_date_lt_input

        participantss_list = RMEC_Employee.objects.raw(sql)
        paginator = Paginator(participantss_list, 25)

        page = request.GET.get('page')
        participantss = paginator.get_page(page)
        return render(request,'participants_list.html',{'participantss':participantss,'sql':sql,'sql2':sql2,'last_name_input':last_name_input,'first_name_input':first_name_input,'doc_no_input':doc_no_input,'phone_input':phone_input,'email_input':email_input,'home_address_input':home_address_input,'city_input':city_input,'state_input':state_input,'zip_code_input':zip_code_input,'correctional_facility_input':correctional_facility_input,'hired_date_gt_input':hired_date_gt_input,'hired_date_lt_input':hired_date_lt_input})

class RMEC_EmployeeDelete(LoginRequiredMixin,DeleteView):
    model = RMEC_Employee
    success_url = reverse_lazy('participants_list')
@login_required(login_url='/accounts/login/')
def participantsAdd(request):

    if request.method == 'POST':

        form = ParticipantForm(request.POST)

        if form.is_valid():
            form.save()


            return redirect('participants_list')


    else:
        form = ParticipantForm()
    return render(request, 'participants_add.html', {'form': form})

@login_required(login_url='/accounts/login/')
def RMEC_EmployeeUpdate(request, pk):
        obj= get_object_or_404(RMEC_Employee, id=pk)
        form = ParticipantForm(request.POST or None, instance= obj)
        context= {'form': form,}

        if form.is_valid():
                obj= form.save(commit= False)
                obj.save()
                context= {'form': form}
                return redirect('participants_list')
        else:
                context= {'form': form,}
                return render(request,'participants_update.html' , context)

@login_required(login_url='/accounts/login/')
def RMEC_Employee_upload(request):
    return render(request,'change_list_import_item.html')
@login_required(login_url='/accounts/login/')
def RMEC_Employee_download(request):
    items=RMEC_Employee.objects.all()
    response=HttpResponse(content_type='text/csv')
    response['Content-Desposition']='attachment; filename="participant.csv"'
    writer=csv.writer(response)
    writer.writerow(['id','last_name','first_name','doc_no','correctional_facility','home_address','city','state','zip_code','phone','email','education','certificate','work_area','job_status','hired_date','created_date','updated_date'])
    for obj in items:
         writer.writerow([obj.id,obj.last_name,obj.first_name,obj.doc_no,obj.correctional_facility,obj.home_address,obj.city,obj.state,obj.zip_code,obj.phone,obj.email,obj.education,obj.certificate,obj.work_area,obj.job_status,obj.hired_date,obj.created_date,obj.updated_date])
    return response
class UsersView(LoginRequiredMixin, ListView):
     template_name = 'users.html'
     paginate_by =10
     def get_queryset(self):
          return User.objects.filter(is_superuser=True)
class IndustrypartnerlistView(LoginRequiredMixin, ListView):
     template_name = 'industry_partner_list.html'
     paginate_by =10
     def get_queryset(self):
          return User.objects.filter(is_superuser=False)


@login_required(login_url='/accounts/login/')
def AdminRegistration(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            form.save()
            user = authenticate(email=email, password=raw_password)
            return redirect('users')
    else:
        form = AdminSignUpForm()
    return render(request,'admin_registration.html',{'form': form,})
# def AdminRegistrationUpdate(request,pk):
#     form = AdminSignUpForm()
#     return render(request, 'RMEC_Employee/user_update_form.html', {'form': form})

class IndustrypartnerUpdate(UpdateView):
    model = User
    fields = ['email','first_name','last_name','is_active','business_name','business_address','city','state','zip_code','phone']
    template_name_suffix = '_partner_update_form'


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_is_active=request.POST.get('is_active')
        print(form_is_active)
        db_is_active=self.object.is_active
        print(db_is_active)


        if form_is_active == "on" and db_is_active is False:
            sender_address=settings.EMAIL_HOST_USER
            subject="RMEC Login Details"
            new_password = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(7))
            message = 'Dear ' + self.object.first_name + ",\n\n" + \
                    "Username: " + str(self.object) + "\n" + \
                    "Password: " + new_password + "\n\n" + \
                    "Please click on below link to Login" + "\n" + \
                    "http://reentry.rmecosha.com/accounts/login/" + "\n\n" + \
                    "Thank you," + "\n" + \
                    "RMEC"
            u = User.objects.get(email=self.object)
            u.set_password(new_password)
            u.save()
            send_mail(sender_address,str(self.object),subject,message)
        return super().post(request, *args, **kwargs)
    success_url = reverse_lazy('IndustrypartnerlistView')
class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    fields = ['email','first_name','last_name','is_active','business_name','business_address','city','state','zip_code','phone']
    template_name_suffix = '_profile_update_form'
    success_url = reverse_lazy('profile_update')
class UsersUpdate(LoginRequiredMixin,UpdateView):
    model = User
    fields = ['email','first_name','last_name','is_active']
    
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('users')
class UsersDelete(LoginRequiredMixin,DeleteView):
    model = User
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('users')
class IndustrypartnerDelete(DeleteView):
    model = User
    template_name_suffix = '_partner_confirm_delete'
    success_url = reverse_lazy('IndustrypartnerlistView')


