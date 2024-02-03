from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from . models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import date
from datetime import timedelta
import random
import string
from django.db import models
from django.shortcuts import render,redirect

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from xhtml2pdf import pisa
from django.template.loader import get_template
from bs4 import BeautifulSoup
import io
from openpyxl import Workbook
from openpyxl import load_workbook
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from io import BytesIO
# Create your views here.
from datetime import date
from django.db.models import Max

from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from xhtml2pdf import pisa
from django.template.loader import get_template
from bs4 import BeautifulSoup
import io
from openpyxl import Workbook
from openpyxl import load_workbook
def Fin_index(request):
    return render(request,'Fin_index.html')


def Fin_login(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        passw = request.POST['password']
    
        log_user = auth.authenticate(username = user_name,
                                  password = passw)
    
        if log_user is not None:
            auth.login(request, log_user)

        # ---super admin---

            if request.user.is_staff==1:
                return redirect('Fin_Adminhome') 
            
        # -------distributor ------    
            
        if Fin_Login_Details.objects.filter(User_name = user_name,password = passw).exists():
            data =  Fin_Login_Details.objects.get(User_name = user_name,password = passw)  
            if data.User_Type == 'Distributor':
                did = Fin_Distributors_Details.objects.get(Login_Id=data.id) 
                if did.Admin_approval_status == 'Accept':
                    request.session["s_id"]=data.id
                    if 's_id' in request.session:
                        if request.session.has_key('s_id'):
                            s_id = request.session['s_id']
                            print(s_id)
                            
                            current_day=date.today() 
                            if current_day == did.End_date:
                                print("wrong")
                                   
                                return redirect('Fin_Wrong')
                            else:
                                return redirect('Fin_DHome')
                            
                    else:
                        return redirect('/')
                else:
                    messages.info(request, 'Approval is Pending..')
                    return redirect('Fin_DistributorReg')
                      
            if data.User_Type == 'Company':
                cid = Fin_Company_Details.objects.get(Login_Id=data.id) 
                if cid.Admin_approval_status == 'Accept' or cid.Distributor_approval_status == 'Accept':
                    request.session["s_id"]=data.id
                    if 's_id' in request.session:
                        if request.session.has_key('s_id'):
                            s_id = request.session['s_id']
                            print(s_id)
                            com = Fin_Company_Details.objects.get(Login_Id = s_id)
                            

                            current_day=date.today() 
                            if current_day >= com.End_date:
                                print("wrong")
                                   
                                return redirect('Fin_Wrong')
                            else:
                                return redirect('Fin_Com_Home')
                    else:
                        return redirect('/')
                else:
                    messages.info(request, 'Approval is Pending..')
                    return redirect('Fin_CompanyReg')  
            if data.User_Type == 'Staff': 
                cid = Fin_Staff_Details.objects.get(Login_Id=data.id)   
                if cid.Company_approval_status == 'Accept':
                    request.session["s_id"]=data.id
                    if 's_id' in request.session:
                        if request.session.has_key('s_id'):
                            s_id = request.session['s_id']
                            print(s_id)
                            com = Fin_Staff_Details.objects.get(Login_Id = s_id)
                            

                            current_day=date.today() 
                            if current_day >= com.company_id.End_date:
                                print("wrong")
                                messages.info(request, 'Your Account Temporary blocked')
                                return redirect('Fin_StaffReg') 
                            else:
                                return redirect('Fin_Com_Home')
                    else:
                        return redirect('/')
                else:
                    messages.info(request, 'Approval is Pending..')
                    return redirect('Fin_StaffReg') 
        else:
            messages.info(request, 'Invalid Username or Password. Try Again.')
            return redirect('Fin_CompanyReg')  
    else:  
        return redirect('Fin_CompanyReg')   
  

def logout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect('Fin_index')  

                    


 
    
# ---------------------------start admin ------------------------------------   


def Fin_Adminhome(request):
    noti = Fin_ANotification.objects.filter(status = 'New')
    n = len(noti)
    context = {
        'noti':noti,
        'n':n
    }
    return render(request,'Admin/Fin_Adminhome.html',context)

def Fin_PaymentTerm(request):
    terms = Fin_Payment_Terms.objects.all()
    noti = Fin_ANotification.objects.filter(status = 'New')
    n = len(noti)
    return render(request,'Admin/Fin_Payment_Terms.html',{'terms':terms,'noti':noti,'n':n})

def Fin_add_payment_terms(request):
  if request.method == 'POST':
    num=int(request.POST['num'])
    select=request.POST['select']
    if select == 'Years':
      days=int(num)*365
      pt = Fin_Payment_Terms(payment_terms_number = num,payment_terms_value = select,days = days)
      pt.save()
      messages.success(request, 'Payment term is added')
      return redirect('Fin_PaymentTerm')

    else:  
      days=int(num*30)
      pt = Fin_Payment_Terms(payment_terms_number = num,payment_terms_value = select,days = days)
      pt.save()
      messages.success(request, 'Payment term is added')
      return redirect('Fin_PaymentTerm')


  return redirect('Fin_PaymentTerm')

def Fin_ADistributor(request):
    noti = Fin_ANotification.objects.filter(status = 'New')
    n = len(noti)
    return render(request,"Admin/Fin_ADistributor.html",{'noti':noti,'n':n})

def Fin_Distributor_Request(request):
   data = Fin_Distributors_Details.objects.filter(Admin_approval_status = "NULL")
   print(data)
   noti = Fin_ANotification.objects.filter(status = 'New')
   n = len(noti)
   return render(request,"Admin/Fin_Distributor_Request.html",{'data':data,'noti':noti,'n':n})

def Fin_Distributor_Req_overview(request,id):
    data = Fin_Distributors_Details.objects.get(id=id)
    noti = Fin_ANotification.objects.filter(status = 'New')
    n = len(noti)
    return render(request,"Admin/Fin_Distributor_Req_overview.html",{'data':data,'noti':noti,'n':n})

def Fin_DReq_Accept(request,id):
   data = Fin_Distributors_Details.objects.get(id=id)
   data.Admin_approval_status = 'Accept'
   data.save()
   return redirect('Fin_Distributor_Request')

def Fin_DReq_Reject(request,id):
   data = Fin_Distributors_Details.objects.get(id=id)
   data.Login_Id.delete()
   data.delete()
   return redirect('Fin_Distributor_Request')

def Fin_Distributor_delete(request,id):
   data = Fin_Distributors_Details.objects.get(id=id)
   data.Login_Id.delete()
   data.delete()
   return redirect('Fin_All_distributors')

def Fin_All_distributors(request):
   data = Fin_Distributors_Details.objects.filter(Admin_approval_status = "Accept")
   print(data)
   noti = Fin_ANotification.objects.filter(status = 'New')
   n = len(noti)
   return render(request,"Admin/Fin_All_distributors.html",{'data':data,'noti':noti,'n':n})

def Fin_All_Distributor_Overview(request,id):
   data = Fin_Distributors_Details.objects.get(id=id)
   noti = Fin_ANotification.objects.filter(status = 'New')
   n = len(noti)
   return render(request,"Admin/Fin_All_Distributor_Overview.html",{'data':data,'noti':noti,'n':n})  

def Fin_AClients(request):
    noti = Fin_ANotification.objects.filter(status = 'New')
    n = len(noti)
    return render(request,"Admin/Fin_AClients.html",{'noti':noti,'n':n})


def Fin_AClients_Request(request):
    data = Fin_Company_Details.objects.filter(Registration_Type = "self", Admin_approval_status = "NULL")
    print(data)
    noti = Fin_ANotification.objects.filter(status = 'New')
    n = len(noti)
    return render(request,"Admin/Fin_AClients_Request.html",{'data':data,'noti':noti,'n':n})

def Fin_AClients_Request_OverView(request,id):
    data = Fin_Company_Details.objects.get(id=id)
    allmodules = Fin_Modules_List.objects.get(company_id = id,status = "New")
    noti = Fin_ANotification.objects.filter(status = 'New')
    n = len(noti)
    return render(request,'Admin/Fin_AClients_Request_OverView.html',{'data':data,'allmodules':allmodules,'noti':noti,'n':n})

def Fin_Client_Req_Accept(request,id):
   data = Fin_Company_Details.objects.get(id=id)
   data.Admin_approval_status = 'Accept'
   data.save()
   return redirect('Fin_AClients_Request')

def Fin_Client_Req_Reject(request,id):
   data = Fin_Company_Details.objects.get(id=id)
   data.Login_Id.delete()
   data.delete()
   return redirect('Fin_AClients_Request')

def Fin_Client_delete(request,id):
   data = Fin_Company_Details.objects.get(id=id)
   data.Login_Id.delete()
   data.delete()
   return redirect('Fin_Admin_clients')

def Fin_Admin_clients(request):
   data = Fin_Company_Details.objects.filter(Admin_approval_status = "Accept")
   print(data)
   noti = Fin_ANotification.objects.filter(status = 'New')
   n = len(noti)
   return render(request,"Admin/Fin_Admin_clients.html",{'data':data,'noti':noti,'n':n})

def Fin_Admin_clients_overview(request,id):
   data = Fin_Company_Details.objects.get(id=id)
   allmodules = Fin_Modules_List.objects.get(company_id = id,status = "New")
   noti = Fin_ANotification.objects.filter(status = 'New')
   n = len(noti)
   return render(request,"Admin/Fin_Admin_clients_overview.html",{'data':data,'allmodules':allmodules,'noti':noti,'n':n})   

def Fin_Anotification(request):
    noti = Fin_ANotification.objects.filter(status = 'New')
    n = len(noti)
    context = {
        'noti':noti,
        'n':n
    }
    return render(request,'Admin/Fin_Anotification.html',context) 

def  Fin_Anoti_Overview(request,id):
    noti = Fin_ANotification.objects.filter(status = 'New')
    n = len(noti)

    

    data = Fin_ANotification.objects.get(id=id)

    if data.Login_Id.User_Type == "Company":

        if data.Modules_List :
            allmodules = Fin_Modules_List.objects.get(Login_Id = data.Login_Id,status = "New")
            allmodules1 = Fin_Modules_List.objects.get(Login_Id = data.Login_Id,status = "pending")

        
            context = {
                'noti':noti,
                'n':n,
                'data':data,
                'allmodules':allmodules,
                'allmodules1':allmodules1,
            }
            return render(request,'Admin/Fin_Anoti_Overview.html',context)
        else:
            data1 = Fin_Company_Details.objects.get(Login_Id = data.Login_Id)
            context = {
                'noti':noti,
                'n':n,
                'data1':data1,
                'data':data,
                
            }
            return render(request,'Admin/Fin_Anoti_Overview.html',context)
    else:
        data1 = Fin_Distributors_Details.objects.get(Login_Id = data.Login_Id)
        context = {
                'noti':noti,
                'n':n,
                'data1':data1,
                'data':data,
                
            }

        return render(request,'Admin/Fin_Anoti_Overview.html',context)


def  Fin_Module_Updation_Accept(request,id):
    data = Fin_ANotification.objects.get(id=id)
    allmodules = Fin_Modules_List.objects.get(Login_Id = data.Login_Id,status = "New")
    allmodules.delete()

    allmodules1 = Fin_Modules_List.objects.get(Login_Id = data.Login_Id,status = "pending")
    allmodules1.status = "New"
    allmodules1.save()

    data.status = 'old'
    data.save()

    return redirect('Fin_Anotification')

def  Fin_Module_Updation_Reject(request,id):
    data = Fin_ANotification.objects.get(id=id)
    allmodules = Fin_Modules_List.objects.get(Login_Id = data.Login_Id,status = "pending")
    allmodules.delete()

    data.delete()

    return redirect('Fin_Anotification')

def  Fin_payment_terms_Updation_Accept(request,id):
    data = Fin_ANotification.objects.get(id=id)
    com = Fin_Company_Details.objects.get(Login_Id = data.Login_Id)
    terms=Fin_Payment_Terms.objects.get(id=data.PaymentTerms_updation.Payment_Term.id)
    
    
    com.Start_Date =date.today()
    days=int(terms.days)

    end= date.today() + timedelta(days=days)
    com.End_date = end
    com.Payment_Term = terms
    com.save()

    data.status = 'old'
    data.save()

    upt = Fin_Payment_Terms_updation.objects.get(id = data.PaymentTerms_updation.id)
    upt.status = 'old'
    upt.save()

    cnoti = Fin_CNotification.objects.filter(Company_id = com)
    for c in cnoti:
        c.status = 'old'
        c.save()    

    return redirect('Fin_Anotification')

def  Fin_payment_terms_Updation_Reject(request,id):
    data = Fin_ANotification.objects.get(id=id)

    upt = Fin_Payment_Terms_updation.objects.get(id = data.PaymentTerms_updation.id)

    upt.delete()
    data.delete()

    return redirect('Fin_Anotification')


def  Fin_ADpayment_terms_Updation_Accept(request,id):
    data = Fin_ANotification.objects.get(id=id)
    com = Fin_Distributors_Details.objects.get(Login_Id = data.Login_Id)
    terms=Fin_Payment_Terms.objects.get(id=data.PaymentTerms_updation.Payment_Term.id)
    
    
    com.Start_Date =date.today()
    days=int(terms.days)

    end= date.today() + timedelta(days=days)
    com.End_date = end
    com.Payment_Term = terms
    com.save()

    data.status = 'old'
    data.save()

    upt = Fin_Payment_Terms_updation.objects.get(id = data.PaymentTerms_updation.id)
    upt.status = 'old'
    upt.save()

    cnoti = Fin_DNotification.objects.filter(Distributor_id = com)
    for c in cnoti:
        c.status = 'old'
        c.save()    

    return redirect('Fin_Anotification')

def  Fin_ADpayment_terms_Updation_Reject(request,id):
    data = Fin_ANotification.objects.get(id=id)

    upt = Fin_Payment_Terms_updation.objects.get(id = data.PaymentTerms_updation.id)

    upt.delete()
    data.delete()

    return redirect('Fin_Anotification')

 
# ---------------------------end admin ------------------------------------ 






# ---------------------------start distributor------------------------------------   

 
def Fin_DHome(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Distributors_Details.objects.get(Login_Id = s_id)
        current_day=date.today() 
        diff = (data.End_date - current_day).days
        num = 20
        print(diff)
        if diff <= 20:
            n=Fin_DNotification(Login_Id = data.Login_Id,Distributor_id = data,Title = "Payment Terms Alert",Discription = "Your Payment Terms End Soon")
            n.save() 

        noti = Fin_DNotification.objects.filter(status = 'New',Distributor_id = data.id)
        n = len(noti)
        context = {
            'noti':noti,
            'n':n,
            'data':data
        }
        return render(request,'Distributor/Fin_DHome.html',context)
    else:
       return redirect('/')   

def Fin_DistributorReg(request):
    terms = Fin_Payment_Terms.objects.all()
    context = {
       'terms':terms
    }
    return render(request,'Distributor/Fin_DistributorReg.html',context)

def Fin_DReg_Action(request):
    if request.method == 'POST':
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      email = request.POST['email']
      user_name = request.POST['username']
      password = request.POST['dpassword']

      if Fin_Login_Details.objects.filter(User_name=user_name).exists():
        messages.info(request, 'This username already exists. Sign up again')
        return redirect('Fin_DistributorReg')
      
      elif Fin_Distributors_Details.objects.filter(Email=email).exists():
        messages.info(request, 'This email already exists. Sign up again')
        return redirect('Fin_DistributorReg')
      else:
        dlog = Fin_Login_Details(First_name = first_name,Last_name = last_name,
                                User_name = user_name,password = password,
                                User_Type = 'Distributor')
        dlog.save()

        code_length = 8  
        characters = string.ascii_letters + string.digits  # Letters and numbers

        while True:
            unique_code = ''.join(random.choice(characters) for _ in range(code_length))
        
            # Check if the code already exists in the table
            if not Fin_Company_Details.objects.filter(Company_Code = unique_code).exists():
              break 

        ddata = Fin_Distributors_Details(Email = email,Login_Id = dlog,Distributor_Code = unique_code,Admin_approval_status = "NULL")
        ddata.save()
        return redirect('Fin_DReg2',dlog.id)    

        # code=get_random_string(length=6)
        # if Fin_Distributors_Details.objects.filter( Distributor_Code = code).exists():
        #     code2=get_random_string(length=6)

        #     ddata = Fin_Distributors_Details(Email = email,Login_Id = dlog,Distributor_Code = code2,Admin_approval_status = "NULL")
        #     ddata.save()
        #     return redirect('Fin_DReg2',dlog.id)
        # else:
        #     ddata = Fin_Distributors_Details(Email = email,Login_Id = dlog,Distributor_Code = code,Admin_approval_status = "NULL")
        #     ddata.save()
        #     return redirect('Fin_DReg2',dlog.id)
 
    return redirect('Fin_DistributorReg')

def Fin_DReg2(request,id):
    dlog = Fin_Login_Details.objects.get(id = id)
    ddata = Fin_Distributors_Details.objects.get(Login_Id = id)
    terms = Fin_Payment_Terms.objects.all()
    context = {
       'terms':terms,
       'dlog':dlog,
       'ddata':ddata
    }
    return render(request,'Distributor/Fin_DReg2.html',context)

def Fin_DReg2_Action2(request,id):
   if request.method == 'POST':
      ddata = Fin_Distributors_Details.objects.get(Login_Id = id)

      ddata.Contact = request.POST['phone']
      ddata.Image=request.FILES.get('img')

      payment_term = request.POST['payment_term']
      terms=Fin_Payment_Terms.objects.get(id=payment_term)
    
      start_date=date.today()
      days=int(terms.days)

      end= date.today() + timedelta(days=days)
      End_date=end

      ddata.Payment_Term  = terms
      ddata.Start_Date = start_date
      ddata.End_date = End_date

      ddata.save()
      return redirect('Fin_DistributorReg')
   return render('Fin_DReg2',id)  

def Fin_DClient_req(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Distributors_Details.objects.get(Login_Id = s_id)
        data1 = Fin_Company_Details.objects.filter(Registration_Type = "distributor",Distributor_approval_status = "NULL",Distributor_id = data.id)
        noti = Fin_DNotification.objects.filter(status = 'New',Distributor_id = data.id)
        n = len(noti)
        return render(request,'Distributor/Fin_DClient_req.html',{'data':data,'data1':data1,'noti':noti,'n':n})
    else:
       return redirect('/') 
    
def Fin_DClient_req_overview(request,id):
    data = Fin_Company_Details.objects.get(id=id)
    allmodules = Fin_Modules_List.objects.get(company_id = id,status = "New")
    noti = Fin_DNotification.objects.filter(status = 'New',Distributor_id = data.id)
    n = len(noti)
    return render(request,'Distributor/Fin_DClient_req_overview.html',{'data':data,'allmodules':allmodules,'noti':noti,'n':n})    
    
def Fin_DClient_Req_Accept(request,id):
   data = Fin_Company_Details.objects.get(id=id)
   data.Distributor_approval_status = 'Accept'
   data.save()
   return redirect('Fin_DClient_req')

def Fin_DClient_Req_Reject(request,id):
   data = Fin_Company_Details.objects.get(id=id)
   data.Login_Id.delete()
   data.delete()
   return redirect('Fin_DClient_req')   

def Fin_DClients(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Distributors_Details.objects.get(Login_Id = s_id)
        data1 = Fin_Company_Details.objects.filter(Registration_Type = "distributor",Distributor_approval_status = "Accept",Distributor_id = data.id)
        noti = Fin_DNotification.objects.filter(status = 'New',Distributor_id = data.id)
        n = len(noti)
        return render(request,'Distributor/Fin_DClients.html',{'data':data,'data1':data1,'noti':noti,'n':n})
    else:
       return redirect('/')  
   
def Fin_DClients_overview(request,id):
    data = Fin_Company_Details.objects.get(id=id)
    allmodules = Fin_Modules_List.objects.get(company_id = id,status = "New")
    noti = Fin_DNotification.objects.filter(status = 'New',Distributor_id = data.id)
    n = len(noti)
    return render(request,'Distributor/Fin_DClients_overview.html',{'data':data,'allmodules':allmodules,'noti':noti,'n':n})

def Fin_DClient_remove(request,id):
   data = Fin_Company_Details.objects.get(id=id)
   data.Login_Id.delete()
   data.delete()
   return redirect('Fin_DClients') 
    
def Fin_DProfile(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Distributors_Details.objects.get(Login_Id = s_id)
        data1 = Fin_Company_Details.objects.filter(Registration_Type = "distributor",Distributor_approval_status = "Accept",Distributor_id = data.id)
        terms = Fin_Payment_Terms.objects.all()
        noti = Fin_DNotification.objects.filter(status = 'New',Distributor_id = data.id)
        n = len(noti)
        return render(request,'Distributor/Fin_DProfile.html',{'data':data,'data1':data1,'terms':terms,'noti':noti,'n':n})
    else:
       return redirect('/')  
    
def Fin_Dnotification(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Distributors_Details.objects.get(Login_Id = s_id)

        noti = Fin_DNotification.objects.filter(status = 'New',Distributor_id = data.id)
        n = len(noti)
        context = {
            'noti':noti,
            'n':n,
            'data':data
        }
        return render(request,'Distributor/Fin_Dnotification.html',context)  
    else:
       return redirect('/') 
    
def  Fin_Dnoti_Overview(request,id):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        d = Fin_Distributors_Details.objects.get(Login_Id = s_id)
        noti = Fin_DNotification.objects.filter(status = 'New',Distributor_id = d.id)
        n = len(noti)

        

        data = Fin_DNotification.objects.get(id=id)

        if data.Modules_List :
            allmodules = Fin_Modules_List.objects.get(Login_Id = data.Login_Id,status = "New")
            allmodules1 = Fin_Modules_List.objects.get(Login_Id = data.Login_Id,status = "pending")

        
            context = {
                'noti':noti,
                'n':n,
                'data':data,
                'allmodules':allmodules,
                'allmodules1':allmodules1,
            }
            return render(request,'Distributor/Fin_Dnoti_Overview.html',context)
        else:
            data1 = Fin_Company_Details.objects.get(Login_Id = data.Login_Id)
            context = {
                'noti':noti,
                'n':n,
                'data1':data1,
                'data':data,
                
            }
            return render(request,'Distributor/Fin_Dnoti_Overview.html',context)    
    else:
       return redirect('/') 
    
def  Fin_DModule_Updation_Accept(request,id):
    data = Fin_DNotification.objects.get(id=id)
    allmodules = Fin_Modules_List.objects.get(Login_Id = data.Login_Id,status = "New")
    allmodules.delete()

    allmodules1 = Fin_Modules_List.objects.get(Login_Id = data.Login_Id,status = "pending")
    allmodules1.status = "New"
    allmodules1.save()

    data.status = 'old'
    data.save()

    return redirect('Fin_Dnotification')

def  Fin_DModule_Updation_Reject(request,id):
    data = Fin_DNotification.objects.get(id=id)
    allmodules = Fin_Modules_List.objects.get(Login_Id = data.Login_Id,status = "pending")
    allmodules.delete()

    data.delete()

    return redirect('Fin_Dnotification')

def  Fin_Dpayment_terms_Updation_Accept(request,id):
    data = Fin_DNotification.objects.get(id=id)
    com = Fin_Company_Details.objects.get(Login_Id = data.Login_Id)
    terms=Fin_Payment_Terms.objects.get(id=data.PaymentTerms_updation.Payment_Term.id)
    
    
    com.Start_Date =date.today()
    days=int(terms.days)

    end= date.today() + timedelta(days=days)
    com.End_date = end
    com.Payment_Term = terms
    com.save()

    data.status = 'old'
    data.save()

    upt = Fin_Payment_Terms_updation.objects.get(id = data.PaymentTerms_updation.id)
    upt.status = 'old'
    upt.save()

    return redirect('Fin_Dnotification')

def  Fin_Dpayment_terms_Updation_Reject(request,id):
    data = Fin_DNotification.objects.get(id=id)

    upt = Fin_Payment_Terms_updation.objects.get(id = data.PaymentTerms_updation.id)

    upt.delete()
    data.delete()

    return redirect('Fin_Dnotification')    

def Fin_DChange_payment_terms(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        
        if request.method == 'POST':
            data = Fin_Login_Details.objects.get(id = s_id)
            com = Fin_Distributors_Details.objects.get(Login_Id = s_id)
            pt = request.POST['payment_term']

            pay = Fin_Payment_Terms.objects.get(id=pt)

            data1 = Fin_Payment_Terms_updation(Login_Id = data,Payment_Term = pay)
            data1.save()

            
            noti = Fin_ANotification(Login_Id = data,PaymentTerms_updation = data1,Title = "Change Payment Terms",Discription = com.Login_Id.First_name + " is change Payment Terms")
            noti.save()
              


        
            return redirect('Fin_DProfile')
    else:
       return redirect('/') 
    

def Fin_Edit_Dprofile(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        com = Fin_Distributors_Details.objects.get(Login_Id = s_id)
        data = Fin_Distributors_Details.objects.get(Login_Id = s_id)

        noti = Fin_DNotification.objects.filter(status = 'New',Distributor_id = data.id)
        n = len(noti)

        context ={
            'com':com,
            'data':data,
            'n':n,
            'noti':noti
        }

        return render(request,"Distributor/Fin_Edit_Dprofile.html",context)    
    else:
       return redirect('/')    
    
def Fin_Edit_Dprofile_Action(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        com = Fin_Distributors_Details.objects.get(Login_Id = s_id)
        if request.method == 'POST':
            com.Login_Id.First_name = request.POST['first_name']
            com.Login_Id.Last_name = request.POST['last_name']
            com.Email = request.POST['email']
            com.Contact = request.POST['contact']
            
            com.Image  = request.FILES.get('img')
            

            com.Login_Id.save()
            com.save()

            return redirect('Fin_DProfile')
        return redirect('Fin_Edit_Dprofile')     
    else:
       return redirect('/')     

      
# ---------------------------end distributor------------------------------------  


             
# ---------------------------start staff------------------------------------   
    

def Fin_StaffReg(request):
    return render(request,'company/Fin_StaffReg.html')

def Fin_staffReg_action(request):
   if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_name = request.POST['cusername']
        password = request.POST['cpassword'] 
        cid = request.POST['Company_Code']
        if Fin_Company_Details.objects.filter(Company_Code = cid ).exists():
            com =Fin_Company_Details.objects.get(Company_Code = cid )

            if Fin_Staff_Details.objects.filter(company_id=com,Login_Id__User_name=user_name).exists():
                messages.info(request, 'This username already exists. Sign up again')
                return redirect('Fin_StaffReg')

            if Fin_Login_Details.objects.filter(User_name=user_name,password = password).exists():
                messages.info(request, 'This username and password already exists. Sign up again')
                return redirect('Fin_StaffReg')
        
            elif Fin_Staff_Details.objects.filter(Email=email).exists():
                messages.info(request, 'This email already exists. Sign up again')
                return redirect('Fin_StaffReg')
            else:
                dlog = Fin_Login_Details(First_name = first_name,Last_name = last_name,
                                    User_name = user_name,password = password,
                                    User_Type = 'Staff')
                dlog.save()

                ddata = Fin_Staff_Details(Email = email,Login_Id = dlog,Company_approval_status = "NULL",company_id = com)
                ddata.save()
                return redirect('Fin_StaffReg2',dlog.id)
        else:
            messages.info(request, 'This company code  not exists. Sign up again')  
            return redirect('Fin_StaffReg')    
        
def Fin_StaffReg2(request,id):
    dlog = Fin_Login_Details.objects.get(id = id)
    ddata = Fin_Staff_Details.objects.get(Login_Id = id)
    context = {
       'dlog':dlog,
       'ddata':ddata
    }
    return render(request,'company/Fin_StaffReg2.html',context)

def Fin_StaffReg2_Action(request,id):
    if request.method == 'POST':
        
        staff = Fin_Staff_Details.objects.get(Login_Id = id)
        log = Fin_Login_Details.objects.get(id = id)

        staff.Login_Id = log
           
        staff.contact = request.POST['phone']
        staff.img=request.FILES.get('img')
        staff.Company_approval_status = "Null"
        staff.save()
        print("Staff Registration Complete")
    
        return redirect('Fin_StaffReg')
        
    else:
        return redirect('Fin_StaffReg2',id)
# ---------------------------end staff------------------------------------ 


    
# ---------------------------start company------------------------------------ 

def Fin_Com_Home(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        if data.User_Type == "Company":
            com = Fin_Company_Details.objects.get(Login_Id = s_id)
            allmodules = Fin_Modules_List.objects.get(Login_Id = s_id,status = 'New')

            current_day=date.today() 
            diff = (com.End_date - current_day).days
            num = 20
            print(diff)
            if diff <= 20:
                n=Fin_CNotification(Login_Id = data,Company_id = com,Title = "Payment Terms Alert",Discription = "Your Payment Terms End Soon")
                n.save()    

            noti = Fin_CNotification.objects.filter(status = 'New',Company_id = com)
            n = len(noti)

            context = {
                'allmodules':allmodules,
                'com':com,
                'data':data,
                'noti':noti,
                'n':n
                }

            return render(request,'company/Fin_Com_Home.html',context)
        else:
            com = Fin_Staff_Details.objects.get(Login_Id = s_id)
            allmodules = Fin_Modules_List.objects.get(company_id = com.company_id,status = 'New')
            return render(request,'company/Fin_Com_Home.html',{'allmodules':allmodules,'com':com,'data':data})
    else:
       return redirect('/') 
    
def Fin_Cnotification(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        if data.User_Type == "Company":
            com = Fin_Company_Details.objects.get(Login_Id = s_id)
            allmodules = Fin_Modules_List.objects.get(Login_Id = s_id,status = 'New')

            noti = Fin_CNotification.objects.filter(status = 'New',Company_id = com)
            n = len(noti)
            context = {
                'allmodules':allmodules,
                'com':com,
                'data':data,
                'noti':noti,
                'n':n
            }
            return render(request,'company/Fin_Cnotification.html',context)  
        else:
            com = Fin_Staff_Details.objects.get(Login_Id = s_id)
            allmodules = Fin_Modules_List.objects.get(company_id = com.company_id,status = 'New')
            context = {
                'allmodules':allmodules,
                'com':com,
                'data':data,
                
            }
            return render(request,'company/Fin_Cnotification.html',context)
    else:
       return redirect('/')     
     

def Fin_CompanyReg(request):
    return render(request,'company/Fin_CompanyReg.html')

def Fin_companyReg_action(request):
   if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_name = request.POST['cusername']
        password = request.POST['cpassword']


        if Fin_Login_Details.objects.filter(User_name=user_name).exists():
            messages.info(request, 'This username already exists. Sign up again')
            return redirect('Fin_CompanyReg')
      
        elif Fin_Company_Details.objects.filter(Email=email).exists():
            messages.info(request, 'This email already exists. Sign up again')
            return redirect('Fin_CompanyReg')
        else:
            dlog = Fin_Login_Details(First_name = first_name,Last_name = last_name,
                                User_name = user_name,password = password,
                                User_Type = 'Company')
            dlog.save()

        code_length = 8  
        characters = string.ascii_letters + string.digits  # Letters and numbers

        while True:
            unique_code = ''.join(random.choice(characters) for _ in range(code_length))
        
            # Check if the code already exists in the table
            if not Fin_Company_Details.objects.filter(Company_Code = unique_code).exists():
              break  

        ddata = Fin_Company_Details(Email = email,Login_Id = dlog,Company_Code = unique_code,Admin_approval_status = "NULL",Distributor_approval_status = "NULL")
        ddata.save()
        return redirect('Fin_CompanyReg2',dlog.id)      

        # code=get_random_string(length=6)
        # if Fin_Company_Details.objects.filter( Company_Code = code).exists():
        #     code2=get_random_string(length=6)

        #     ddata = Fin_Company_Details(Email = email,Login_Id = dlog,Company_Code = code2,Admin_approval_status = "NULL",Distributor_approval_status = "NULL")
        #     ddata.save()
        #     return redirect('Fin_CompanyReg2',dlog.id)
        # else:
        #     ddata = Fin_Company_Details(Email = email,Login_Id = dlog,Company_Code = code,Admin_approval_status = "NULL",Distributor_approval_status = "NULL")
        #     ddata.save()
        #     return redirect('Fin_CompanyReg2',dlog.id)
 
   return redirect('Fin_DistributorReg')

def Fin_CompanyReg2(request,id):
    data = Fin_Login_Details.objects.get(id=id)
    terms = Fin_Payment_Terms.objects.all()
    return render(request,'company/Fin_CompanyReg2.html',{'data':data,'terms':terms})

def Fin_CompanyReg2_action2(request,id):
    if request.method == 'POST':
        data = Fin_Login_Details.objects.get(id=id)
        com = Fin_Company_Details.objects.get(Login_Id=data.id)

        com.Company_name = request.POST['cname']
        com.Address = request.POST['caddress']
        com.City = request.POST['city']
        com.State = request.POST['state']
        com.Pincode = request.POST['pincode']
        com.Country = request.POST['ccountry']
        com.Image  = request.FILES.get('img1')
        com.Business_name = request.POST['bname']
        com.Industry = request.POST['industry']
        com.Company_Type = request.POST['ctype']
        com.Accountant = request.POST['staff']
        com.Payment_Type = request.POST['paid']
        com.Registration_Type = request.POST['reg_type']
        com.Contact = request.POST['phone']

        dis_code = request.POST['dis_code']
        if dis_code != '':
            if Fin_Distributors_Details.objects.filter(Distributor_Code = dis_code).exists():
                com.Distributor_id = Fin_Distributors_Details.objects.get(Distributor_Code = dis_code)
            else :
                messages.info(request, 'Sorry, distributor id does not exists')
                return redirect('Fin_CompanyReg2',id)
            
        
        payment_term = request.POST['payment_term']
        terms=Fin_Payment_Terms.objects.get(id=payment_term)
        com.Payment_Term =terms
        com.Start_Date=date.today()
        days=int(terms.days)

        end= date.today() + timedelta(days=days)
        com.End_date=end

        com.save()
        return redirect('Fin_Modules',id)
   
def Fin_Modules(request,id):
    data = Fin_Login_Details.objects.get(id=id)
    return render(request,'company/Fin_Modules.html',{'data':data})   

def Fin_Add_Modules(request,id):
    if request.method == 'POST':
        data = Fin_Login_Details.objects.get(id=id)
        com = Fin_Company_Details.objects.get(Login_Id=data.id)

        # -----ITEMS----

        Items = request.POST.get('c1')
        Price_List = request.POST.get('c2')
        Stock_Adjustment = request.POST.get('c3')


        # --------- CASH & BANK-----
        Cash_in_hand = request.POST.get('c4')
        Offline_Banking = request.POST.get('c5')
        # Bank_Reconciliation = request.POST.get('c6')
        UPI = request.POST.get('c7')
        Bank_Holders = request.POST.get('c8')
        Cheque = request.POST.get('c9')
        Loan_Account = request.POST.get('c10')

        #  ------SALES MODULE -------
        Customers = request.POST.get('c11')
        Invoice  = request.POST.get('c12')
        Estimate = request.POST.get('c13')
        Sales_Order = request.POST.get('c14')
        Recurring_Invoice = request.POST.get('c15')
        Retainer_Invoice = request.POST.get('c16')
        Credit_Note = request.POST.get('c17')
        Payment_Received = request.POST.get('c18')
        Delivery_Challan = request.POST.get('c19')

        #  ---------PURCHASE MODULE--------- 
        Vendors = request.POST.get('c20') 
        Bills  = request.POST.get('c21')
        Recurring_Bills = request.POST.get('c22')
        Debit_Note = request.POST.get('c23')
        Purchase_Order = request.POST.get('c24')
        Expenses = request.POST.get('c25')
        Payment_Made = request.POST.get('c27')

        #  ---------EWay_Bill---------
        EWay_Bill = request.POST.get('c28')

        #  -------ACCOUNTS--------- 
        Chart_of_Accounts = request.POST.get('c29') 
        Manual_Journal = request.POST.get('c30')
        # Reconcile  = request.POST.get('c36')


        # -------PAYROLL------- 
        Employees = request.POST.get('c31')
        Employees_Loan = request.POST.get('c32')
        Holiday = request.POST.get('c33') 
        Attendance = request.POST.get('c34')
        Salary_Details = request.POST.get('c35')

        modules = Fin_Modules_List(Items = Items,Price_List = Price_List,Stock_Adjustment = Stock_Adjustment,
            Cash_in_hand = Cash_in_hand,Offline_Banking = Offline_Banking,
            UPI = UPI,Bank_Holders = Bank_Holders,Cheque = Cheque,Loan_Account = Loan_Account,
            Customers = Customers,Invoice = Invoice,Estimate = Estimate,Sales_Order = Sales_Order,
            Recurring_Invoice = Recurring_Invoice,Retainer_Invoice = Retainer_Invoice,Credit_Note = Credit_Note,
            Payment_Received = Payment_Received,Delivery_Challan = Delivery_Challan,
            Vendors = Vendors,Bills = Bills,Recurring_Bills = Recurring_Bills,Debit_Note = Debit_Note,
            Purchase_Order = Purchase_Order,Expenses = Expenses,
            Payment_Made = Payment_Made,EWay_Bill = EWay_Bill,
            Chart_of_Accounts = Chart_of_Accounts,Manual_Journal = Manual_Journal,
            Employees = Employees,Employees_Loan = Employees_Loan,Holiday = Holiday,
            Attendance = Attendance,Salary_Details = Salary_Details,
            Login_Id = data,company_id = com)
        
        modules.save()

        print("add modules")
        return redirect('Fin_CompanyReg')
    return redirect('Fin_Modules',id)

def Fin_Edit_Modules(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        
        com = Fin_Company_Details.objects.get(Login_Id = s_id)
        allmodules = Fin_Modules_List.objects.get(Login_Id = s_id,status = 'New')
        return render(request,'company/Fin_Edit_Modules.html',{'allmodules':allmodules,'com':com})
       
    else:
       return redirect('/') 
def Fin_Edit_Modules_Action(request): 
    if 's_id' in request.session:
        s_id = request.session['s_id']
        
        if request.method == 'POST':
            data = Fin_Login_Details.objects.get(id = s_id)
        
            com = Fin_Company_Details.objects.get(Login_Id = s_id)

            # -----ITEMS----

            Items = request.POST.get('c1')
            Price_List = request.POST.get('c2')
            Stock_Adjustment = request.POST.get('c3')


            # --------- CASH & BANK-----
            Cash_in_hand = request.POST.get('c4')
            Offline_Banking = request.POST.get('c5')
            # Bank_Reconciliation = request.POST.get('c6')
            UPI = request.POST.get('c7')
            Bank_Holders = request.POST.get('c8')
            Cheque = request.POST.get('c9')
            Loan_Account = request.POST.get('c10')

            #  ------SALES MODULE -------
            Customers = request.POST.get('c11')
            Invoice  = request.POST.get('c12')
            Estimate = request.POST.get('c13')
            Sales_Order = request.POST.get('c14')
            Recurring_Invoice = request.POST.get('c15')
            Retainer_Invoice = request.POST.get('c16')
            Credit_Note = request.POST.get('c17')
            Payment_Received = request.POST.get('c18')
            Delivery_Challan = request.POST.get('c19')

            #  ---------PURCHASE MODULE--------- 
            Vendors = request.POST.get('c20') 
            Bills  = request.POST.get('c21')
            Recurring_Bills = request.POST.get('c22')
            Debit_Note = request.POST.get('c23')
            Purchase_Order = request.POST.get('c24')
            Expenses = request.POST.get('c25')
            
            Payment_Made = request.POST.get('c27')

            # ----------EWay_Bill-----
            EWay_Bill = request.POST.get('c28')

            #  -------ACCOUNTS--------- 
            Chart_of_Accounts = request.POST.get('c29') 
            Manual_Journal = request.POST.get('c30')
            # Reconcile  = request.POST.get('c36')


            # -------PAYROLL------- 
            Employees = request.POST.get('c31')
            Employees_Loan = request.POST.get('c32')
            Holiday = request.POST.get('c33') 
            Attendance = request.POST.get('c34')
            Salary_Details = request.POST.get('c35')

            modules = Fin_Modules_List(Items = Items,Price_List = Price_List,Stock_Adjustment = Stock_Adjustment,
                Cash_in_hand = Cash_in_hand,Offline_Banking = Offline_Banking,
                UPI = UPI,Bank_Holders = Bank_Holders,Cheque = Cheque,Loan_Account = Loan_Account,
                Customers = Customers,Invoice = Invoice,Estimate = Estimate,Sales_Order = Sales_Order,
                Recurring_Invoice = Recurring_Invoice,Retainer_Invoice = Retainer_Invoice,Credit_Note = Credit_Note,
                Payment_Received = Payment_Received,Delivery_Challan = Delivery_Challan,
                Vendors = Vendors,Bills = Bills,Recurring_Bills = Recurring_Bills,Debit_Note = Debit_Note,
                Purchase_Order = Purchase_Order,Expenses = Expenses,
                Payment_Made = Payment_Made,EWay_Bill = EWay_Bill,
                Chart_of_Accounts = Chart_of_Accounts,Manual_Journal = Manual_Journal,
                Employees = Employees,Employees_Loan = Employees_Loan,Holiday = Holiday,
                Attendance = Attendance,Salary_Details = Salary_Details,
                Login_Id = data,company_id = com,status = 'pending')
            
            modules.save()
            data1=Fin_Modules_List.objects.filter(company_id = com).update(update_action=1)

            if com.Registration_Type == 'self':
                noti = Fin_ANotification(Login_Id = data,Modules_List = modules,Title = "Module Updation",Discription = com.Company_name + " is change Modules")
                noti.save()
            else:
                noti = Fin_DNotification(Distributor_id = com.Distributor_id,Login_Id = data,Modules_List = modules,Title = "Module Updation",Discription = com.Company_name + " is change Modules")
                noti.save()   

            print("edit modules")
            return redirect('Fin_Company_Profile')
        return redirect('Fin_Edit_Modules')
       
    else:
       return redirect('/')    
    


def Fin_Company_Profile(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        if data.User_Type == "Company":
            com = Fin_Company_Details.objects.get(Login_Id = s_id)
            allmodules = Fin_Modules_List.objects.get(Login_Id = s_id,status = 'New')
            terms = Fin_Payment_Terms.objects.all()
            noti = Fin_CNotification.objects.filter(status = 'New',Company_id = com)
            n = len(noti)
            return render(request,'company/Fin_Company_Profile.html',{'allmodules':allmodules,'com':com,'data':data,'terms':terms,'noti':noti,'n':n})
        else:
            com = Fin_Staff_Details.objects.get(Login_Id = s_id)
            allmodules = Fin_Modules_List.objects.get(company_id = com.company_id,status = 'New')
            return render(request,'company/Fin_Company_Profile.html',{'allmodules':allmodules,'com':com,'data':data})
        
    else:
       return redirect('/') 
    
def Fin_Staff_Req(request): 
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        com = Fin_Company_Details.objects.get(Login_Id = s_id)
        data1 = Fin_Staff_Details.objects.filter(company_id = com.id,Company_approval_status = "NULL")
        allmodules = Fin_Modules_List.objects.get(Login_Id = s_id,status = 'New')
        noti = Fin_CNotification.objects.filter(status = 'New',Company_id = com)
        n = len(noti)
        return render(request,'company/Fin_Staff_Req.html',{'com':com,'data':data,'allmodules':allmodules,'data1':data1,'noti':noti,'n':n})
    else:
       return redirect('/') 

def Fin_Staff_Req_Accept(request,id):
   data = Fin_Staff_Details.objects.get(id=id)
   data.Company_approval_status = 'Accept'
   data.save()
   return redirect('Fin_Staff_Req')

def Fin_Staff_Req_Reject(request,id):
   data = Fin_Staff_Details.objects.get(id=id)
   data.Login_Id.delete()
   data.delete()
   return redirect('Fin_Staff_Req')  

def Fin_Staff_delete(request,id):
   data = Fin_Staff_Details.objects.get(id=id)
   data.Login_Id.delete()
   data.delete()
   return redirect('Fin_All_Staff')  

def Fin_All_Staff(request): 
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        com = Fin_Company_Details.objects.get(Login_Id = s_id)
        data1 = Fin_Staff_Details.objects.filter(company_id = com.id,Company_approval_status = "Accept")
        allmodules = Fin_Modules_List.objects.get(Login_Id = s_id,status = 'New')
        noti = Fin_CNotification.objects.filter(status = 'New',Company_id = com)
        n = len(noti)
        return render(request,'company/Fin_All_Staff.html',{'com':com,'data':data,'allmodules':allmodules,'data1':data1,'noti':noti,'n':n})
    else:
       return redirect('/') 


def Fin_Change_payment_terms(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        
        if request.method == 'POST':
            data = Fin_Login_Details.objects.get(id = s_id)
            com = Fin_Company_Details.objects.get(Login_Id = s_id)
            pt = request.POST['payment_term']

            pay = Fin_Payment_Terms.objects.get(id=pt)

            data1 = Fin_Payment_Terms_updation(Login_Id = data,Payment_Term = pay)
            data1.save()

            if com.Registration_Type == 'self':
                noti = Fin_ANotification(Login_Id = data,PaymentTerms_updation = data1,Title = "Change Payment Terms",Discription = com.Company_name + " is change Payment Terms")
                noti.save()
            else:
                noti = Fin_DNotification(Distributor_id = com.Distributor_id,Login_Id = data,PaymentTerms_updation = data1,Title = "Change Payment Terms",Discription = com.Company_name + " is change Payment Terms")
                noti.save()    


        
            return redirect('Fin_Company_Profile')
    else:
       return redirect('/') 
    
def Fin_Wrong(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        if data.User_Type == "Company":
            com = Fin_Company_Details.objects.get(Login_Id = s_id)
        else:
           com = Fin_Distributors_Details.objects.get(Login_Id = s_id)     
        terms = Fin_Payment_Terms.objects.all()
        context= {
            'com':com,
            'terms':terms
        }
        return render(request,"company/Fin_Wrong.html",context)    
    else:
       return redirect('/') 
    
def Fin_Wrong_Action(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        
        if request.method == 'POST':
            data = Fin_Login_Details.objects.get(id = s_id)

            if data.User_Type == "Company":
                com = Fin_Company_Details.objects.get(Login_Id = s_id)
                pt = request.POST['payment_term']

                pay = Fin_Payment_Terms.objects.get(id=pt)

                data1 = Fin_Payment_Terms_updation(Login_Id = data,Payment_Term = pay)
                data1.save()

                if com.Registration_Type == 'self':
                    noti = Fin_ANotification(Login_Id = data,PaymentTerms_updation = data1,Title = "Change Payment Terms",Discription = com.Company_name + " is change Payment Terms")
                    noti.save()
                else:
                    noti = Fin_DNotification(Distributor_id = com.Distributor_id,Login_Id = data,PaymentTerms_updation = data1,Title = "Change Payment Terms",Discription = com.Company_name + " is change Payment Terms")
                    noti.save()    


            
                return redirect('Fin_CompanyReg')
            else:
                com = Fin_Distributors_Details.objects.get(Login_Id = s_id)
                pt = request.POST['payment_term']

                pay = Fin_Payment_Terms.objects.get(id=pt)

                data1 = Fin_Payment_Terms_updation(Login_Id = data,Payment_Term = pay)
                data1.save()

                noti = Fin_ANotification(Login_Id = data,PaymentTerms_updation = data1,Title = "Change Payment Terms",Discription = com.Login_Id.First_name + com.Login_Id.Last_name + " is change Payment Terms")
                noti.save()

                return redirect('Fin_DistributorReg')



    else:
       return redirect('/')  

def Fin_Edit_Company_profile(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        data = Fin_Login_Details.objects.get(id = s_id)
        com = Fin_Company_Details.objects.get(Login_Id = s_id)
        noti = Fin_CNotification.objects.filter(status = 'New',Company_id = com)
        n = len(noti)

        context ={
            'com':com,
            'data':data,
            'n':n,
            'noti':noti


        }

        return render(request,"company/Fin_Edit_Company_profile.html",context)    
    else:
       return redirect('/') 
    

def Fin_Edit_Company_profile_Action(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        com = Fin_Company_Details.objects.get(Login_Id = s_id)
        if request.method == 'POST':
            com.Login_Id.First_name = request.POST['first_name']
            com.Login_Id.Last_name = request.POST['last_name']
            com.Email = request.POST['email']
            com.Contact = request.POST['contact']
            com.Company_name = request.POST['cname']
            com.Address = request.POST['caddress']
            com.City = request.POST['city']
            com.State = request.POST['state']
            com.Pincode = request.POST['pincode']
            com.Business_name = request.POST['bname']
            com.Pan_NO = request.POST['pannum']
            com.GST_Type = request.POST.get('gsttype')
            com.GST_NO = request.POST['gstnum']
            com.Industry = request.POST['industry']
            com.Company_Type = request.POST['ctype']
            com.Image = request.FILES.get('img')
            

            com.Login_Id.save()
            com.save()

            return redirect('Fin_Company_Profile')
        return redirect('Fin_Edit_Company_profile')     
    else:
       return redirect('/') 
    
def Fin_Edit_Staff_profile(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        com = Fin_Staff_Details.objects.get(Login_Id = s_id)

        context ={
            'com':com
        }

        return render(request,"company/Fin_Edit_Staff_profile.html",context)    
    else:
       return redirect('/')    
    
def Fin_Edit_Staff_profile_Action(request):
    if 's_id' in request.session:
        s_id = request.session['s_id']
        com = Fin_Staff_Details.objects.get(Login_Id = s_id)
        if request.method == 'POST':
            com.Login_Id.First_name = request.POST['first_name']
            com.Login_Id.Last_name = request.POST['last_name']
            com.Email = request.POST['email']
            com.contact = request.POST['contact']
            
            com.img = request.FILES.get('img')
            

            com.Login_Id.save()
            com.save()

            return redirect('Fin_Company_Profile')
        return redirect('Fin_Edit_Staff_profile')     
    else:
       return redirect('/')     
      
    
# ---------------------------end company------------------------------------     
    

# harikrishnan start------------------------------
    
def employee_list(request):
    sid = request.session['s_id']
    loginn = Fin_Login_Details.objects.get(id=sid)
    if loginn.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        employee = Employee.objects.filter(company_id=com.id)
    elif loginn.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        employee = Employee.objects.filter(company_id=staf.company_id_id)
    else:
        distributor = Fin_Distributors_Details.objects.get(Login_Id = sid)

    return render(request,'company/Employee_List.html',{'employee':employee,'allmodules':allmodules})

def employee_create_page(request):
    sid = request.session['s_id']
    loginn = Fin_Login_Details.objects.get(id=sid)
    
    if loginn.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        bloodgroup = Employee_Blood_Group.objects.filter(company_id=com.id,login_id=sid).values('blood_group').distinct()
        
    elif loginn.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        bloodgroup = Employee_Blood_Group.objects.filter(company_id=staf.company_id_id,login_id=sid).values('blood_group').distinct()

    return render(request,'company/Employee_Create_Page.html',{'allmodules':allmodules,'bloodgroup':bloodgroup})    

def employee_save(request):

    if request.method == 'POST':

        title = request.POST['Title']
        firstname = request.POST['First_Name'].capitalize()
        lastname = request.POST['Last_Name'].capitalize()
        alias = request.POST['Alias']
        joiningdate = request.POST['Joining_Date']
        salarydate = request.POST['Salary_Date']
        salaryamount = request.POST['Salary_Amount']

        if request.POST['Salary_Amount'] == '':
            salaryamount = None
        else:
            salaryamount = request.POST['Salary_Amount']

        amountperhour = request.POST['perhour']
        if amountperhour == '' or amountperhour == '0':
            amountperhour = 0
        else:
            amountperhour = request.POST['perhour']

        workinghour = request.POST['workhour']
        if workinghour == '' or workinghour == '0':
            workinghour = 0
        else:
            workinghour = request.POST['workhour']

        salary_type = request.POST['Salary_Type']
        
        employeenumber = request.POST['Employee_Number']
        designation = request.POST['Designation']
        location = request.POST['Location']
        gender = request.POST['Gender']
        image = request.FILES.get('Image', None)
        if image:
            image = request.FILES['Image']
        else:
            if gender == 'Male':
                image = 'media/male_default.png'
            elif gender == 'Female':
                image = 'media/female_default.png'
            else:
                image = 'media/male_default.png'

        dob = request.POST['DOB']
        blood = request.POST['Blood']
        parent = request.POST['Parent'].capitalize()
        spouse = request.POST['Spouse'].capitalize()
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        tempStreet = request.POST['tempStreet']
        tempCity = request.POST['tempCity']
        tempState = request.POST['tempState']
        tempPincode = request.POST['tempPincode']
        tempCountry = request.POST['tempCountry']
        
        
        contact = request.POST['Contact_Number']
        emergencycontact = request.POST['Emergency_Contact']
        email = request.POST['Email']
        file = request.FILES.get('File', None)
        if file:
            file = request.FILES['File']
        else:
            file=''
        bankdetails = request.POST['Bank_Details']
        accoutnumber = request.POST['Account_Number']
        ifsc = request.POST['IFSC']
        bankname = request.POST['BankName']
        branchname = request.POST['BranchName']
        transactiontype = request.POST['Transaction_Type']

        

        if request.POST['tds_applicable'] == 'Yes':
            tdsapplicable = request.POST['tds_applicable']
            tdstype = request.POST['TDS_Type']
            
            if tdstype == 'Amount':
                tdsvalue = request.POST['TDS_Amount']
            elif tdstype == 'Percentage':
                tdsvalue = request.POST['TDS_Percentage']
            else:
                tdsvalue = 0
        elif request.POST['tds_applicable'] == 'No':
            tdsvalue = 0
            tdstype = ''
            tdsapplicable = request.POST['tds_applicable']
        else:
            tdsvalue = 0
            tdstype = ''
            tdsapplicable = ''

        
        
        incometax = request.POST['Income_Tax']
        aadhar = request.POST['Aadhar']
        uan = request.POST['UAN']
        pf = request.POST['PF']
        pan = request.POST['PAN']
        pr = request.POST['PR']

        if dob == '':
            age = 2
        else:
            dob2 = date.fromisoformat(dob)
            today = date.today()
            age = int(today.year - dob2.year - ((today.month, today.day) < (dob2.month, dob2.day)))
        
        sid = request.session['s_id']
        employee = Fin_Login_Details.objects.get(id=sid)
        
        if employee.User_Type == 'Company':
            companykey =  Fin_Company_Details.objects.get(Login_Id_id=sid)
        elif employee.User_Type == 'Staff':
            staffkey = Fin_Staff_Details.objects.get(Login_Id=sid)
            companykey = Fin_Company_Details.objects.get(id=staffkey.company_id_id)
        else:
            distributorkey = Fin_Distributors_Details.objects.get(login_Id=sid)
            companykey = Fin_Company_Details.objects.get(id=distributorkey.company_id_id)

        
        if Employee.objects.filter(employee_mail=email,mobile = contact,employee_number=employeenumber,company_id = companykey.id).exists():
            messages.error(request,'user exist')
            return render(request,'company/Employee_Create_Page.html')
        
        elif Employee.objects.filter(mobile = contact,company_id = companykey.id).exists():
            messages.error(request,'phone number exist')
            return render(request,'company/Employee_Create_Page.html')
        
        elif Employee.objects.filter(employee_mail=email,company_id = companykey.id).exists():
            messages.error(request,'email exist')
            return render(request,'company/Employee_Create_Page.html')
        
        elif Employee.objects.filter(employee_number=employeenumber,company_id = companykey.id).exists():
            messages.error(request,'employee id exist')
            return render(request,'company/Employee_Create_Page.html')
        
        else:
            if employee.User_Type == 'Company':
                

                new = Employee(upload_image=image,title = title,first_name = firstname,last_name = lastname,alias = alias,
                        employee_mail = email,employee_number = employeenumber,employee_designation = designation,
                        employee_current_location = location,mobile = contact,date_of_joining = joiningdate,
                        employee_status = 'Active' ,company_id = companykey.id,login_id=sid,salary_amount = salaryamount ,
                        amount_per_hour = amountperhour ,total_working_hours = workinghour,gender = gender ,date_of_birth = dob ,
                        age = age,blood_group = blood,fathers_name_mothers_name = parent,spouse_name = spouse,
                        emergency_contact = emergencycontact,provide_bank_details = bankdetails,account_number = accoutnumber,
                        ifsc = ifsc,name_of_bank = bankname,branch_name = branchname,bank_transaction_type = transactiontype,
                        tds_applicable = tdsapplicable, tds_type = tdstype,percentage_amount = tdsvalue,pan_number = pan,
                        income_tax_number = incometax,aadhar_number = aadhar,universal_account_number = uan,pf_account_number = pf,
                        pr_account_number = pr,upload_file = file,employee_salary_type =salary_type,salary_effective_from=salarydate,
                        city=city,street=street,state=state,country=country,pincode=pincode,temporary_city=tempCity,
                        temporary_street=tempStreet,temporary_state=tempState,temporary_pincode=tempPincode,temporary_country=tempCountry)
                new.save()

                history = Employee_History(company_id = companykey.id,login_id=sid,employee_id = new.id,date = date.today(),action = 'Created')
                history.save()
        
            elif employee.User_Type == 'Staff':
                

                new =  Employee(upload_image=image,title = title,first_name = firstname,last_name = lastname,alias = alias,
                            employee_mail = email,employee_number = employeenumber,employee_designation = designation,
                            employee_current_location = location,mobile = contact,date_of_joining = joiningdate,
                            employee_salary_type = salary_type,employee_status = 'Active' ,company_id = companykey.id,login_id=sid ,
                            amount_per_hour = amountperhour ,total_working_hours = workinghour,gender = gender ,date_of_birth = dob ,
                            age = age,blood_group = blood,fathers_name_mothers_name = parent,spouse_name = spouse,
                            emergency_contact = emergencycontact,provide_bank_details = bankdetails,account_number = accoutnumber,
                            ifsc = ifsc,name_of_bank = bankname,branch_name = branchname,bank_transaction_type = transactiontype,
                            tds_applicable = tdsapplicable, tds_type = tdstype,percentage_amount = tdsvalue,pan_number = pan,
                            income_tax_number = incometax,aadhar_number = aadhar,universal_account_number = uan,pf_account_number = pf,
                            pr_account_number = pr,upload_file = file,salary_amount = salaryamount,salary_effective_from=salarydate,
                            city=city,street=street,state=state,country=country,pincode=pincode,temporary_city=tempCity,
                            temporary_street=tempStreet,temporary_state=tempState,temporary_pincode=tempPincode,temporary_country=tempCountry)
                
                new.save()

                history = Employee_History(company_id = companykey.id,login_id=sid,employee_id = new.id,date = date.today(),action = 'Created')
                history.save()

        sid = request.session['s_id']
        loginn = Fin_Login_Details.objects.get(id=sid)
        if loginn.User_Type == 'Company':
            com = Fin_Company_Details.objects.get(Login_Id = sid)
            allmodules = Fin_Modules_List.objects.get(company_id = com.id)
            employee = Employee.objects.filter(company_id=com.id)
            
        elif loginn.User_Type == 'Staff' :
            staf = Fin_Staff_Details.objects.get(Login_Id = sid)
            allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
            employee = Employee.objects.filter(company_id=staf.company_id_id)
        return render(request,'company/Employee_List.html',{'allmodules':allmodules,'employee':employee})

def bloodgroup_data(request):
    sid = request.session.get('s_id')
    loginn = Fin_Login_Details.objects.get(id=sid)
    
    if loginn.User_Type == 'Company' :
            com = Fin_Company_Details.objects.get(Login_Id=sid)
            bloodgroup = Employee_Blood_Group.objects.filter(company_id=com.id,login_id=sid).values('blood_group').distinct()
            return JsonResponse({'success': True,'bloodgroup': list(bloodgroup)})

    elif loginn.User_Type == 'Staff' :
            staf = Fin_Staff_Details.objects.get(Login_Id=sid)
            bloodgroup = Employee_Blood_Group.objects.filter(company_id=staf.company_id_id,login_id=sid).values('blood_group').distinct()
            return JsonResponse({'success': True,'bloodgroup': list(bloodgroup)})

    else:
        return JsonResponse({'success': False,'bloodgroup': list(bloodgroup)})
    

def employee_blood_group(request):
    if request.method == 'POST':
        bloodGroup = request.POST.get('bloodGroup', '').upper()
        sid = request.session.get('s_id')
        loginn = Fin_Login_Details.objects.get(id=sid)
        invalid_group = ['A+', 'A-', 'B+', 'O+']

        if loginn.User_Type == 'Company' and bloodGroup not in invalid_group:
            com = Fin_Company_Details.objects.get(Login_Id=sid)
            allmodules = Fin_Modules_List.objects.get(company_id=com.id)
            group = Employee_Blood_Group(blood_group=bloodGroup, company_id=com.id, login_id=sid)
            group.save()
            bloodgroup = Employee_Blood_Group.objects.filter(company_id=com.id,login_id=sid).values('blood_group').distinct()
            return JsonResponse({'success': True,'bloodgroup': list(bloodgroup)})

        elif loginn.User_Type == 'Staff' and bloodGroup not in invalid_group:
            staf = Fin_Staff_Details.objects.get(Login_Id=sid)
            allmodules = Fin_Modules_List.objects.get(company_id=staf.company_id_id)
            group = Employee_Blood_Group(blood_group=bloodGroup, company_id=staf.company_id_id, login_id=sid)
            group.save()
            bloodgroup = Employee_Blood_Group.objects.filter(company_id=staf.company_id_id,login_id=sid).values('blood_group').distinct()
            return JsonResponse({'success': True,'bloodgroup': list(bloodgroup)})

    return JsonResponse({'success': False, 'error': 'Invalid blood group or user type'})

# hari end



#tinto views

    
def employee_loan_list(request):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    if login.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        employee = Employee.objects.filter(company_id=com.id)
        loan = Loan.objects.filter(company_id=com.id)
    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        
        employee = Employee.objects.filter(company_id=staf.company_id_id)
        loan = Loan.objects.filter(company_id=staf.company_id.id)
    else:
        distributor = Fin_Distributors_Details.objects.get(Login_Id = sid)

    return render(request,'company/Employee_loan_list.html',{'employee':employee,'allmodules':allmodules,'loan':loan})

def employee_loan_sort_by_balance(request):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    if login.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        employee = Employee.objects.filter(company_id=com.id)
        loan = Loan.objects.filter(company_id=com.id).order_by('-balance')

    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        employee = Employee.objects.filter(company_id=staf.company_id_id)
        loan = Loan.objects.filter(company_id=com.id).order_by('-balance')

    else:
        distributor = Fin_Distributors_Details.objects.get(Login_Id = sid)

    return render(request,'company/Employee_loan_list.html',{'employee':employee,'allmodules':allmodules,'loan':loan})


def employee_loan_sort_by_employeename(request):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    if login.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        employee = Employee.objects.filter(company_id=com.id)
        loan = Loan.objects.filter(company_id=com.id).order_by('-employee_name')

    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        employee = Employee.objects.filter(company_id=staf.company_id_id)
        loan = Loan.objects.filter(company_id=com.id).order_by('-employee_name')

    else:
        distributor = Fin_Distributors_Details.objects.get(Login_Id = sid)

    return render(request,'company/Employee_loan_list.html',{'employee':employee,'allmodules':allmodules,'loan':loan})

def employee_loan_filter_by_active(request):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    if login.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        employee = Employee.objects.filter(company_id=com.id)
        loan = Loan.objects.filter(company_id=com.id,status='Active')

    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        employee = Employee.objects.filter(company_id=staf.company_id_id)
        loan = Loan.objects.filter(company_id=com.id,status='Active')

    else:
        distributor = Fin_Distributors_Details.objects.get(Login_Id = sid)

    return render(request,'company/Employee_loan_list.html',{'employee':employee,'allmodules':allmodules,'loan':loan})

def employee_loan_filter_by_inactive(request):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    if login.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        employee = Employee.objects.filter(company_id=com.id)
        loan = Loan.objects.filter(company_id=com.id,status='Inactive')

    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        employee = Employee.objects.filter(company_id=staf.company_id_id)
        loan = Loan.objects.filter(company_id=com.id,status='Inactive')

    else:
        distributor = Fin_Distributors_Details.objects.get(Login_Id = sid)

    return render(request,'company/Employee_loan_list.html',{'employee':employee,'allmodules':allmodules,'loan':loan})

def employee_loan_create_page(request):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    
    if login.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        employee = Employee.objects.filter(company_id=com.id)
        term=Employee_Loan_Term.objects.filter(company=com)
      
        
    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        employee = Employee.objects.filter(company_id=staf.company_id_id)
        term=Employee_Loan_Term.objects.filter(company=com)
      

    return render(request,'company/Employee_loan_create.html',{'allmodules':allmodules,'employee':employee,'term':term})    

def employeedata(request):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    
    if login.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        customer_id = request.GET.get('id')
        cust = Employee.objects.get(id=customer_id,company_id=com.id)
        data7 = {'email': cust.employee_mail,'salary':cust.salary_amount,'jdate':cust.date_of_joining,'empid':cust.employee_number}
        return JsonResponse(data7)

      
        
    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        cust = Employee.objects.get(id=customer_id,company_id=staf.company_id_id)
        data7 = {'email': cust.employee_mail,'salary':cust.salary_amount,'jdate':cust.date_of_joining,'empid':cust.employee_number}
        return JsonResponse(data7)





def employee_loan_save(request):


    

    if request.method == 'POST':


        employeename = request.POST['employee']
        empid = request.POST['empid']
        empemail = request.POST['empemail']
        salary = request.POST['salary']
        join_date = request.POST['Joining_Date']

        loan_Date = request.POST.get('loan_date1', None)
        loan_amount = request.POST['loan_amount']
        loanduration = request.POST['loanduration']
        duration=Employee_Loan_Term.objects.get(id=loanduration)
        

        expdate = request.POST['expdate']
        select_payment = request.POST['select_payment']
        cheque_no = request.POST['cheque_no']
        upi_id = request.POST['upi_id']
        acc_no = request.POST['acc_no']
        cutingamount = request.POST['cutingamount']
        cuttingPercentage = request.POST['cuttingPercentage']
        amount1 = request.POST['pamount']
        amount2 = request.POST['amount5']
        if amount1 != '':
            amount=amount1
        elif amount2 != '':
            amount=amount2



        Note = request.POST['Note']
     
        file = request.FILES.get('File', None)
        if file:
            file = request.FILES['File']
        else:
            file=''
        
        sid = request.session['s_id']
        employee = Fin_Login_Details.objects.get(id=sid)
        companykey =  Fin_Company_Details.objects.get(Login_Id_id=sid)
        emp=Employee.objects.get(id=employeename)
        
        if employee.User_Type == 'Company':
                if Loan.objects.filter(employeeid=empid, company=companykey).exists():
                    messages.error(request,'Already a loan  exsits for this employee !!!')
                    return redirect('employee_loan_create_page')
                else:
                

                    new = Loan(employee=emp,employeeid=empid,employee_email=empemail,salary=salary,join_date=join_date,loan_date=loan_Date,loan_amount=loan_amount,total_loan=loan_amount,
                            expiry_date=expdate,payment_method=select_payment,cheque_number=cheque_no,upi_id=upi_id,bank_account=acc_no,monthly_cutting_percentage=cuttingPercentage,loan_duration=duration,
                            monthly_cutting_amount=amount,note=Note,attach_file=file,company=companykey,login_details=employee,balance=loan_amount,employee_name =emp.title +" " + emp.first_name + " " + emp.last_name,monthly_cutting=cutingamount)
                    
                        
                    new.save()

                    com = Loan.objects.get(id=new.id)
                    history = Employee_Loan_History(company = companykey,login_details=employee,employee_loan =com,date = date.today(),action = 'Created')
                    history.save()
                    trans = Employee_Loan_Transactions(company = companykey,login_details=employee,employee_loan =com,date = date.today(),particulars = 'LOAN ISSUED',employee=emp,balance=loan_amount)
                    trans.save()
        
        elif employee.User_Type == 'Staff':
                

                new =  Employee(employee=emp,employeeid=empid,employee_email=empemail,salary=salary,join_date=join_date,loan_date=loan_Date,loan_amount=loan_amount,total_loan=loan_amount,
                           expiry_date=expdate,payment_method=select_payment,cheque_number=cheque_no,upi_id=upi_id,bank_account=acc_no,monthly_cutting_percentage=cuttingPercentage,loan_duration=loanduration,
                           monthly_cutting_amount=amount,note=Note,attach_file=file,company=companykey,login_details=employee,balance=loan_amount,employee_name =emp.title +" " + emp.first_name + " " + emp.last_name,monthly_cutting=cutingamount)
                
                new.save()
                com = Loan.objects.get(id=new.id)
                history = Employee_Loan_History(company = companykey,login_details=employee,employee_loan = com,date = date.today(),action = 'Created')
                history.save()
                trans = Employee_Loan_Transactions(company = companykey,login_details=employee,employee_loan =com,date = date.today(),particulars = 'LOAN ISSUED',employee=emp,balance=loan_amount)
                trans.save()

   
        return redirect(employee_loan_list)
    


def emploanoverview(request,pk):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    
    if login.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        loan = Loan.objects.get(id=pk)
        est_comments = Employee_loan_comments.objects.filter(employee_loan=loan)
        employee = Employee.objects.get(id=loan.employee.id)
        trans=Employee_Loan_Transactions.objects.filter(employee_loan=loan)
        latest_item_id=Employee_Loan_History.objects.filter(employee_loan=loan,company=com)
      
        
    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        employee = Employee.objects.filter(company_id=staf.company_id_id)
        loan = Loan.objects.get(id=pk)
        est_comments = Employee_loan_comments.objects.filter(employee_loan=loan)
        trans=Employee_Loan_Transactions.objects.filter(employee_loan=loan)
        latest_item_id=Employee_Loan_History.objects.filter(employee_loan=loan,company=staf.company_id)
      

    return render(request,'company/employee_loan_overview.html',{'allmodules':allmodules,'loan':loan,'employee':employee,'trans':trans,'est_comments':est_comments,'latest_item_id':latest_item_id})    

        
def emploanedit(request, pk):                                                                #new by tinto mt
  
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)

    
    # Retrieve the chart of accounts entry
    # loan = get_object_or_404(Loan, id=pk)
    

    # Check if 'company_id' is in the session

   
    if login.User_Type == 'Company':
      
     
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        loan = Loan.objects.get(id=pk)
        employee = Employee.objects.filter(company=com)
        term=Employee_Loan_Term.objects.filter(company=com)
        context = {
                    'allmodules':allmodules,
                    'loan':loan,
                    'employee':employee,
                    'term':term,
            }
       
    
        
        if request.method=='POST':
        
    
        

            loan = Loan.objects.get(id=pk)
            c=Employee_Loan_Transactions.objects.get(employee_loan=pk)
            c.balance=loan_amount=request.POST.get("loan_amount",None)
            c.save()
   
        
            loan.login_details=login
            loan.company=com
            emp=request.POST["employee"]
            emp1=Employee.objects.get(id=emp)
            employee_name1 =emp1.title +" " + emp1.first_name + " " + emp1.last_name
            loan.employee_name = employee_name1
            
            
            loanduration=request.POST.get("loanduration",None)
            term=Employee_Loan_Term.objects.get(id=loanduration)
            loan.loan_duration=term
            loan.employeeid = request.POST.get("empid",None)
            loan.employee_email = request.POST.get("empemail",None)
            loan.salary=request.POST.get("salary",None)
            loan.join_date=request.POST.get("join_date",None)
            loan.loan_date=request.POST.get("loan_date",None)
            loan.loan_amount=request.POST.get("loan_amount",None)
            loan.expiry_date=request.POST.get("expdate",None)
            loan.payment_method=request.POST.get("select_payment",None)
            loan.cheque_number=request.POST.get("cheque_no",None)
            loan.upi_id=request.POST.get("upi_id",None)
            loan.bank_account=request.POST.get("acc_no",None)
            loan.monthly_cutting=request.POST.get("cutingamount",None)
            if request.POST.get("cutingamount",None) == 'Yes':
                loan.monthly_cutting_percentage = 0
            else:
                loan.monthly_cutting_percentage=request.POST.get("cuttingPercentage",None)
            loan.monthly_cutting_amount=request.POST.get("monthly_cutting_amount",None)
            loan.bank_account=request.POST.get("acc_no",None)
            loan.monthly_cutting=request.POST.get("cutingamount",None)
            loan.monthly_cutting_percentage=request.POST.get("cuttingPercentage",None)
            amount1 = request.POST['pamount']
            amount2 = request.POST['amount5']
            if amount1 != '':
                loan.monthly_cutting_amount=amount1
            elif amount2 != '':
                loan.monthly_cutting_amount=amount2
            
            loan.note=request.POST.get('Note')
            loan.attach_file = request.FILES.get('File', None)
            loan.save()
            t=Loan.objects.get(id=loan.id)
      
            history=Employee_Loan_History(company = com,login_details=login,employee_loan = loan,date = date.today(),action = 'Edited')
            history.save()
            # Save the changes
        
            # Redirect to another page after successful update
            return redirect('employee_loan_list')
        return render(request, 'company/Employee_loan_edit.html',context)
    if login.User_Type == 'Staff':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        loan = Loan.objects.get(id=pk)
        employee = Employee.objects.filter(company=com)
        context = {
                    'allmodules':allmodules,
                    'loan':loan,
                    'employee':employee
            }
 
        if request.method=='POST':
            b=Employee_Loan_History.objects.get(employee_loan=pk)
            c=Employee_Loan_Transactions.objects.get(employee_loan=pk)
            c.balance=loan_amount=request.POST.get("loan_amount",None)
            c.save()
            loan = Loan.objects.get(id=pk)
   
            b.company=com
            b.login_details=login
            b.action="Edited"
            b.date=date.today()
            loan.login_details=login
            loan.company=com
            emp=request.POST["employee"]
            emp1=Employee.objects.get(id=emp)
            employee_name1 =emp1.title +" " + emp1.first_name + " " + emp1.last_name
            loan.employee_name = employee_name1
            loan.employeeid = request.POST.get("empid",None)
            loan.employee_email = request.POST.get("empemail",None)
            loan.salary=request.POST.get("salary",None)
            loan.join_date=request.POST.get("join_date",None)
            loan.loan_date=request.POST.get("loan_date",None)
            loan.loan_amount=request.POST.get("loan_amount",None)
            loan.expiry_date=request.POST.get("expdate",None)
            loan.payment_method=request.POST.get("select_payment",None)
            loan.cheque_number=request.POST.get("cheque_no",None)
            loan.upi_id=request.POST.get("upi_id",None)
            loan.bank_account=request.POST.get("acc_no",None)
            loan.monthly_cutting=request.POST.get("cutingamount",None)
            if request.POST.get("cutingamount",None) == 'Yes':
                loan.monthly_cutting_percentage = 0
            else:
                loan.monthly_cutting_percentage=request.POST.get("cuttingPercentage",None)
            loan.monthly_cutting_amount=request.POST.get("monthly_cutting_amount",None)
            loan.bank_account=request.POST.get("acc_no",None)
            loan.monthly_cutting=request.POST.get("cutingamount",None)
            loan.monthly_cutting_percentage=request.POST.get("cuttingPercentage",None)
            amount1 = request.POST['pamount']
            amount2 = request.POST['amount5']
            if amount1 != '':
                loan.monthly_cutting_amount=amount1
            elif amount2 != '':
                loan.monthly_cutting_amount=amount2
            
            loan.note=request.POST.get('Note')
            loan.attach_file = request.FILES.get('File', None)
            loan.save()
            t=Loan.objects.get(id=loan.id)
            b.employee_loan=t
            b.save()

            return redirect('employee_loan_list')
        return render(request, 'company/Employee_loan_edit.html',context)



def emploanrepayment(request,pk):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    
    if login.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        loan = Loan.objects.get(id=pk)
        employee = Employee.objects.get(id=loan.employee.id)
        trans=Employee_Loan_Transactions.objects.filter(employee=employee)
      
        
    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        loan = Loan.objects.get(id=pk)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        employee = Employee.objects.get(id=loan.employee.id)
        trans=Employee_Loan_Transactions.objects.filter(employee=loan.employee)
      

    return render(request,'company/Employee_loan_repayment.html',{'allmodules':allmodules,'loan':loan,'employee':employee,'trans':trans})    



def emploanrepaymentsave(request,pk):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    if login.User_Type == 'Company':

            if request.method == 'POST':


                principle_amount = request.POST['principal']
                interest_amount= request.POST['interest']
                principle_amount = request.POST['principal']
                payment_date= request.POST['date']
                payment_method = request.POST['recieved']
                total_amount= request.POST['total']
                cheque_number = request.POST['paid_cheque_id']
                upi_id = request.POST['paid_upi_id']
                bank_account= request.POST['paid_bnk_id']
                
                
                
            
                
                sid = request.session['s_id']
                employee = Fin_Login_Details.objects.get(id=sid)
                companykey =  Fin_Company_Details.objects.get(Login_Id=sid)
                loan=Loan.objects.get(id=pk)
                emp=Employee.objects.get(id=loan.employee.id)
                # Assuming principle_amount is a string, convert it to an integer
                principle_amount_int = int(principle_amount)

                # Perform the subtraction
                balance = loan.balance - principle_amount_int
                

                
                loan.balance=balance
                loan.save()

        # Update the loan balance and save
        

        
                

                new = Employee_Loan_Repayment(employee=emp,company=companykey,login_details=employee,principle_amount=principle_amount,interest_amount=interest_amount,
                                              payment_date=payment_date,payment_method=payment_method,total_amount=total_amount,cheque_number=cheque_number,upi_id=upi_id,
                                              bank_account=bank_account,employee_loan=loan,balance=balance
                                              )
                new.save()
              

                com = Employee_Loan_Repayment.objects.get(id=new.id)
                # history = Employee_Loan_History(company = companykey,login_details=employee,employee_loan =com,date = date.today(),action = 'Created')
                # history.save()
                trans = Employee_Loan_Transactions(company = companykey,login_details=employee,employee_loan =loan,date = date.today(),particulars = 'EMI PAID',employee=emp,repayment=com,balance=balance)
                trans.save()
        
    elif login.User_Type == 'Staff':
            staf = Fin_Staff_Details.objects.get(Login_Id = sid)
            allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
            employee = Employee.objects.filter(company_id=staf.company_id_id)
                

            if request.method == 'POST':


                    principle_amount = request.POST['principal']
                    interest_amount= request.POST['interest']
                    principle_amount = request.POST['principal']
                    payment_date= request.POST['date']
                    payment_method = request.POST['recieved']
                    total_amount= request.POST['total']
                    cheque_number = request.POST['paid_cheque_id']
                    upi_id = request.POST['paid_upi_id']
                    bank_account= request.POST['paid_bnk_id']
                    
                    
                    
                
                    
                    sid = request.session['s_id']
                    employee = Fin_Login_Details.objects.get(id=sid)
                    # companykey =  Fin_Company_Details.objects.get(Login_Id=sid)
                    loan=Loan.objects.get(id=pk)
                    emp=Employee.objects.get(id=loan.employee.id)
                    # Assuming principle_amount is a string, convert it to an integer
                    principle_amount_int = int(principle_amount)

                    # Perform the subtraction
                    balance = loan.balance - principle_amount_int
                    

                    
                    loan.balance=balance
                    loan.save()

            # Update the loan balance and save
            

            
                    

                    new = Employee_Loan_Repayment(employee=emp,company=staf.company_id,login_details=employee,principle_amount=principle_amount,interest_amount=interest_amount,
                                                payment_date=payment_date,payment_method=payment_method,total_amount=total_amount,cheque_number=cheque_number,upi_id=upi_id,
                                                bank_account=bank_account,employee_loan=loan,balance=balance
                                                )
                    new.save()
                

                    com = Employee_Loan_Repayment.objects.get(id=new.id)
                    # history = Employee_Loan_History(company = companykey,login_details=employee,employee_loan =com,date = date.today(),action = 'Created')
                    # history.save()
                    trans = Employee_Loan_Transactions(company = staf.company_id,login_details=employee,employee_loan =loan,date = date.today(),particulars = 'EMI PAID',employee=emp,repayment=com,balance=balance)
                    trans.save()

   
    return redirect(emploanoverview,pk)
    

    
def emploanrepaymentedit(request, pk):                                                                #new by tinto mt
  
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)

    
    # Retrieve the chart of accounts entry
    # loan = get_object_or_404(Loan, id=pk)
    

    # Check if 'company_id' is in the session

   
    if login.User_Type == 'Company':
      
     
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        loan = Loan.objects.get(id=pk)
        loan_re = Employee_Loan_Repayment.objects.get(id=pk)
        employee = Employee.objects.get(id=loan_re.employee.id)
        context = {
                    'allmodules':allmodules,
                    'loan':loan,
                    'employee':employee,
                    'loan_re':loan_re
            }
       
    
        
        if request.method=='POST':
        
    
     
            loan1 = Employee_Loan_Repayment.objects.get(id=pk)
            c=Employee_Loan_Transactions.objects.get(repayment=loan1)
            loan2 = Loan.objects.get(id=loan_re.employee_loan.id)
            
   
       
            loan1.login_details=login
            loan1.company=com
         
    
           
            

            previous_principle_amount=loan1.principle_amount
            previous_principle_amount=int(previous_principle_amount) #5000

            principle_amount=request.POST.get("principal",None)
            principle_amount_new=int(principle_amount)
            previousbalance=c.balance
            previousbalance=int(previousbalance)


            if previous_principle_amount == principle_amount_new:
                newbalance=previousbalance
                c.balance=newbalance
                loan1.balance=newbalance
                loan2.balance=newbalance
            elif previous_principle_amount < principle_amount_new:
                newprincipleamount=principle_amount_new-previous_principle_amount
                newbalance=previousbalance-newprincipleamount
                c.balance=newbalance
                loan1.balance=newbalance
                loan2.balance=newbalance
            elif previous_principle_amount > principle_amount_new:
                newprincipleamount=previous_principle_amount-principle_amount_new
                newbalance=previousbalance+newprincipleamount
                c.balance=newbalance
                loan1.balance=newbalance
                loan2.balance=newbalance
            



        # Assuming principle_amount is a string, convert it to an integer
            # prevbalance=c.balance
            # print(prevbalance)
            # # Assuming prevbalance, loan1.total_amount, and loan1.interest_amount are strings
            # prevbalance = int(prevbalance)
            # loan_total_amount = int(loan1.total_amount)
            # interest_amount = int(loan1.interest_amount)
            # print(prevbalance)
            # currentloan = prevbalance + (loan_total_amount - interest_amount)
            # print(currentloan)
            # principle_amount_int = int(principle_amount)
            # print(principle_amount_int)
            # loan2 = Loan.objects.get(id=loan_re.employee_loan.id)
            # # Perform the subtraction
            # balance1 = currentloan - principle_amount_int
            # print(balance1)

            # # Update the loan balance and save
            # loan1.balance=balance1
            # loan2.balance=balance1
            # c.balance=balance1
            # c.save()

            loan1.principle_amount=request.POST.get("principal",None)
            loan1.interest_amount=request.POST.get("interest",None)
            loan1.payment_date=request.POST.get("date",None)
            loan1.total_amount=request.POST.get("total",None)
            loan1.principle_amount=request.POST.get("principal",None)

            loan1.payment_method=request.POST.get("recieved",None)
            loan1.cheque_number=request.POST.get("paid_cheque_id",None)
            loan1.upi_id=request.POST.get("paid_upi_id",None)
            loan1.bank_account=request.POST.get("paid_bnk_id",None)
            loan2.save()
            loan1.save()
            c.save()

            return redirect('emploanoverview',loan2.id)
        return render(request, 'company/Employee_loan_repayment_edit.html',context)
    if login.User_Type == 'Staff':
            staf = Fin_Staff_Details.objects.get(Login_Id = sid)
            allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
            # employee = Employee.objects.filter(company_id=staf.company_id_id)
            allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
            # loan = Loan.objects.get(id=pk)
            loan_re = Employee_Loan_Repayment.objects.get(id=pk)
            employee = Employee.objects.get(id=loan_re.employee.id)
            context = {
                        'allmodules':allmodules,
                        # 'loan':loan,
                        'employee':employee,
                        'loan_re':loan_re
                }
        
        
            
            if request.method=='POST':
            
        
        
                loan1 = Employee_Loan_Repayment.objects.get(id=pk)
                c=Employee_Loan_Transactions.objects.get(repayment=loan1)
                loan2 = Loan.objects.get(id=loan_re.employee_loan.id)
   
       
                loan1.login_details=login
                loan1.company=staf.company_id
                previous_principle_amount=loan1.principle_amount
                previous_principle_amount=int(previous_principle_amount) #5000

                principle_amount=request.POST.get("principal",None)
                principle_amount_new=int(principle_amount)
                previousbalance=c.balance
                previousbalance=int(previousbalance)


                if previous_principle_amount == principle_amount_new:
                    newbalance=previousbalance
                    c.balance=newbalance
                    loan1.balance=newbalance
                    loan2.balance=newbalance
                elif previous_principle_amount < principle_amount_new:
                    newprincipleamount=principle_amount_new-previous_principle_amount
                    newbalance=previousbalance-newprincipleamount
                    c.balance=newbalance
                    loan1.balance=newbalance
                    loan2.balance=newbalance
                elif previous_principle_amount > principle_amount_new:
                    newprincipleamount=previous_principle_amount-principle_amount_new
                    newbalance=previousbalance+newprincipleamount
                    c.balance=newbalance
                    loan1.balance=newbalance
                    loan2.balance=newbalance
        #         principle_amount=request.POST.get("principal",None)
        # # Assuming principle_amount is a string, convert it to an integer
        #         prevbalance=loan1.balance
        #         print(prevbalance)
        #         # Assuming prevbalance, loan1.total_amount, and loan1.interest_amount are strings
        #         prevbalance = int(prevbalance)
        #         loan_total_amount = int(loan1.total_amount)
        #         interest_amount = int(loan1.interest_amount)
        #         print(prevbalance)
        #         currentloan = prevbalance + (loan_total_amount - interest_amount)
        #         print(currentloan)
        #         principle_amount_int = int(principle_amount)
        #         print(principle_amount_int)
        #         loan2 = Loan.objects.get(id=loan_re.employee_loan.id)
        #         # Perform the subtraction
        #         balance1 = currentloan - principle_amount_int
        #         print(balance1)

        #         # Update the loan balance and save
        #         loan1.balance=balance1
        #         loan2.balance=balance1
            
        
                loan1.principle_amount=request.POST.get("principal",None)
                loan1.interest_amount=request.POST.get("interest",None)
                loan1.payment_date=request.POST.get("date",None)
                loan1.total_amount=request.POST.get("total",None)
                loan1.principle_amount=request.POST.get("principal",None)

                loan1.payment_method=request.POST.get("recieved",None)
                loan1.cheque_number=request.POST.get("paid_cheque_id",None)
                loan1.upi_id=request.POST.get("paid_upi_id",None)
                loan1.bank_account=request.POST.get("paid_bnk_id",None)
            #     principle_amount=request.POST.get("principal",None)
            # # Assuming principle_amount is a string, convert it to an integer
            #     principle_amount_int = int(principle_amount)
            #     loan2 = loan1.objects.get(id=loan.employee_loan.id)
            #     # Perform the subtraction
            #     balance = loan2.loan_amount - principle_amount_int

            #     # Update the loan balance and save
            #     loan1.balance=balance
            #     loan.balance=balance
                loan2.save()
                loan1.save()
                c.save()

                return redirect('emploanoverview',loan2.id)
            return render(request, 'company/Employee_loan_repayment_edit.html',context)


def emploanaddtional(request,pk):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    
    if login.User_Type == 'Company':
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        loan = Loan.objects.get(id=pk)
        employee = Employee.objects.get(id=loan.employee.id)
        trans=Employee_Loan_Transactions.objects.filter(employee_loan=loan)
      
        
    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        loan = Loan.objects.get(id=pk)
        employee = Employee.objects.filter(company_id=staf.company_id_id)
        trans=Employee_Loan_Transactions.objects.filter(employee_loan=loan)
      

    return render(request,'company/Employee_loan_addtional.html',{'allmodules':allmodules,'loan':loan,'employee':employee,'trans':trans})    



def emploanadditionalsave(request,pk):
    sid = request.session['s_id']
    employee = Fin_Login_Details.objects.get(id=sid)

    if request.method == 'POST':


        balance_loan = request.POST['remain_loan']
        new_loan= request.POST['new']
        total_loan = request.POST['amount']
        payment_date= request.POST['adjdate']
        payment_method = request.POST['payment_method']
        
        cheque_number = request.POST['cheque_id']
        upi_id = request.POST['upi_id']
        bank_account= request.POST['bnk_id']
        
        
        
    
        
        sid = request.session['s_id']
        employee = Fin_Login_Details.objects.get(id=sid)
        
        # Assuming principle_amount is a string, convert it to an integer
      

        # Update the loan balance and save
        

        if employee.User_Type == 'Company':
                companykey =  Fin_Company_Details.objects.get(Login_Id_id=sid)
                loan=Loan.objects.get(id=pk)
                emp=Employee.objects.get(id=loan.employee.id)

                loan.balance=total_loan
                print(loan.balance)
                loan_amount=int(loan.total_loan)
                print(loan_amount)
                new=int(new_loan)
                print(new)
                loan.total_loan=loan_amount+new
                print(loan.total_loan)
                loan.save()
                        

                new = Employee_Additional_Loan(company=companykey,login_details=employee,
                                            payment_method=payment_method,total_loan=total_loan,cheque_number=cheque_number,upi_id=upi_id,
                                              bank_account=bank_account,employee_loan=loan,new_loan=new_loan,balance_loan=balance_loan,new_date=payment_date
                                              )
                new.save()
                

                com = Employee_Additional_Loan.objects.get(id=new.id)
                trans = Employee_Loan_Transactions(company = companykey,login_details=employee,employee_loan =loan,date = date.today(),particulars = 'ADDITIONAL LOAN',employee=emp,additional=com,balance=total_loan)
                trans.save()
        
        elif employee.User_Type == 'Staff':
                staf = Fin_Staff_Details.objects.get(Login_Id = sid)
                loan=Loan.objects.get(id=pk)
                emp=Employee.objects.get(id=loan.employee.id)

                loan.balance=total_loan
                print(loan.balance)
                loan_amount=int(loan.total_loan)
                print(loan_amount)
                new=int(new_loan)
                print(new)
                loan.total_loan=loan_amount+new
                print(loan.total_loan)
                loan.save()
                

                new = Employee_Additional_Loan(company=staf.company_id,login_details=employee,
                                              payment_method=payment_method,total_loan=total_loan,cheque_number=cheque_number,upi_id=upi_id,
                                              bank_account=bank_account,employee_loan=loan,new_loan=new_loan,balance_loan=balance_loan,new_date=payment_date
                                              )
                new.save()

                com = Employee_Additional_Loan.objects.get(id=new.id)
                trans = Employee_Loan_Transactions(company = staf.company_id,login_details=employee,employee_loan =loan,date = date.today(),particulars = 'ADDITIONAL LOAN',employee=emp,additional=com,balance=total_loan)
                trans.save()

   
        return redirect(emploanoverview,pk)


def emploanadditionedit(request, pk):                                                                #new by tinto mt
  
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)

    
    # Retrieve the chart of accounts entry
    # loan = get_object_or_404(Loan, id=pk)
    

    # Check if 'company_id' is in the session

   
    if login.User_Type == 'Company':
      
     
        com = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com.id)
        
        loan_ad = Employee_Additional_Loan.objects.get(id=pk)
        loan = Loan.objects.get(id=loan_ad.employee_loan.id)
        # employee = Employee.objects.get(id=loan_ad.employee.id)
        context = {
                    'allmodules':allmodules,
                    'loan':loan,
                    # 'employee':employee,
                    'loan_ad':loan_ad
            }
       
    
        
        if request.method=='POST':
        
    
     
            loan1 = Employee_Additional_Loan.objects.get(id=pk)
            c=Employee_Loan_Transactions.objects.get(additional=loan1)
   
       
            loan1.login_details=login
            loan1.company=com
            loan1.employee_loan=loan
            new_loan_amount=request.POST.get("new",None)
            new_loan_amount=int(new_loan_amount)
        # Assuming principle_amount is a string, convert it to an integer
            prevbalance=loan1.balance_loan
            print(prevbalance)
            # Assuming prevbalance, loan1.total_amount, and loan1.interest_amount are strings
            prevbalance = int(prevbalance)
        
            print(prevbalance)
        
            prevnewloan=loan1.new_loan
            prevnewloan=int(prevnewloan)


            loan2 = Loan.objects.get(id=loan_ad.employee_loan.id)

            prebalanceinloan=loan2.balance
            prebalanceinloan=int(prebalanceinloan)
            print(prebalanceinloan)

            # Perform the subtraction
            currentbalance1 = prebalanceinloan - prevnewloan
            print(currentbalance1)
            actualbalance=currentbalance1+new_loan_amount
            c.balance=actualbalance
            c.save()
            print(actualbalance)
            

            # Update the loan balance and save
            
            loan2.balance=actualbalance

            total_loan=loan2.total_loan
            total_loan=int(total_loan)
            prevtotalloan=total_loan-prevnewloan
            loan2.total_loan=prevtotalloan+new_loan_amount



            loan1.balance_loan=request.POST.get("remain_loan",None)
            loan1.new_loan=request.POST.get("new",None)
            loan1.total_loan=request.POST.get("amount",None)
            loan1.payment_method=request.POST.get("payment_method",None)
           

            loan1.new_date=request.POST.get("adjdate",None)
            loan1.cheque_number=request.POST.get("cheque_id",None)
            loan1.upi_id=request.POST.get("upi_id",None)
            loan1.bank_account=request.POST.get("bnk_id",None)
            loan3 = Loan.objects.get(id=loan_ad.employee_loan.id)

            loan1.save()
            loan2.save()
        
            return redirect('emploanoverview',loan3.id)
        return render(request, 'company/Employee_loan_additional_edit.html',context)
    if login.User_Type == 'Staff':

        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id)
        
        loan_ad = Employee_Additional_Loan.objects.get(id=pk)
        loan = Loan.objects.get(id=loan_ad.employee_loan.id)
        # employee = Employee.objects.get(id=loan_ad.employee.id)
        context = {
                    'allmodules':allmodules,
                    'loan':loan,
                    # 'employee':employee,
                    'loan_ad':loan_ad
            }
       
    
        
        if request.method=='POST':
        
    
     
            loan1 = Employee_Additional_Loan.objects.get(id=pk)
            c=Employee_Loan_Transactions.objects.get(additional=loan1)
   
       
            loan1.login_details=login
            loan1.company=staf.company_id
            loan1.employee_loan=loan
            new_loan_amount=request.POST.get("new",None)
            new_loan_amount=int(new_loan_amount)
        # Assuming principle_amount is a string, convert it to an integer
            prevbalance=loan1.balance_loan
            print(prevbalance)
            # Assuming prevbalance, loan1.total_amount, and loan1.interest_amount are strings
            prevbalance = int(prevbalance)
        
            print(prevbalance)
        
            prevnewloan=loan1.new_loan
            prevnewloan=int(prevnewloan)


            loan2 = Loan.objects.get(id=loan_ad.employee_loan.id)

            prebalanceinloan=loan2.balance
            prebalanceinloan=int(prebalanceinloan)
            print(prebalanceinloan)

            # Perform the subtraction
            currentbalance1 = prebalanceinloan - prevnewloan
            print(currentbalance1)
            actualbalance=currentbalance1+new_loan_amount
            c.balance=actualbalance
            c.save()
            print(actualbalance)
            

            # Update the loan balance and save
            
            loan2.balance=actualbalance

            total_loan=loan2.total_loan
            total_loan=int(total_loan)
            prevtotalloan=total_loan-prevnewloan
            loan2.total_loan=prevtotalloan+new_loan_amount



            loan1.balance_loan=request.POST.get("remain_loan",None)
            loan1.new_loan=request.POST.get("new",None)
            loan1.total_loan=request.POST.get("amount",None)
            loan1.payment_method=request.POST.get("payment_method",None)
           

            loan1.new_date=request.POST.get("adjdate",None)
            loan1.cheque_number=request.POST.get("cheque_id",None)
            loan1.upi_id=request.POST.get("upi_id",None)
            loan1.bank_account=request.POST.get("bnk_id",None)
            loan3 = Loan.objects.get(id=loan_ad.employee_loan.id)

            loan1.save()
            loan2.save()
        
            return redirect('emploanoverview',loan3.id)
        return render(request, 'company/Employee_loan_additional_edit.html',context)




def addemp(request):                                                                #new by tinto mt (item)
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)

    
    # Retrieve the chart of accounts entry
    # loan = get_object_or_404(Loan, id=pk)
    

    # Check if 'company_id' is in the session

   
    # if login.User_Type == 'Company':
    if request.method == 'POST':
            com = Fin_Company_Details.objects.get(Login_Id = sid)
            allmodules = Fin_Modules_List.objects.get(company_id = com.id)
            title = request.POST['Title']
            firstname = request.POST['First_Name'].capitalize()
            lastname = request.POST['Last_Name'].capitalize()
            # alias = request.POST['Alias']
            joiningdate = request.POST['Joining_Date']
            salarydate = request.POST['Salary_Date']
            salaryamount = request.POST['Salary_Amount']

            if request.POST['Salary_Amount'] == '':
                salaryamount = None
            else:
                salaryamount = request.POST['Salary_Amount']

            amountperhour = request.POST['perhour']
            if amountperhour == '' or amountperhour == '0':
                amountperhour = 0
            else:
                amountperhour = request.POST['perhour']

            workinghour = request.POST['workhour']
            if workinghour == '' or workinghour == '0':
                workinghour = 0
            else:
                workinghour = request.POST['workhour']

            salary_type = request.POST['Salary_Type']
            
            employeenumber = request.POST['Employee_Number']
            designation = request.POST['Designation']
            location = request.POST['Location']
            gender = request.POST['Gender']
            image = request.FILES.get('Image', None)
            if image:
                image = request.FILES['Image']
            else:
                if gender == 'Male':
                    image = 'media/male_default.png'
                elif gender == 'Female':
                    image = 'media/female_default.png'
                else:
                    image = 'media/male_default.png'

            dob = request.POST['DOB']
            blood = request.POST['Blood']
            parent = request.POST['Parent'].capitalize()
            spouse = request.POST['Spouse'].capitalize()
            street = request.POST['street']
            city = request.POST['city']
            state = request.POST['state']
            pincode = request.POST['pincode']
            country = request.POST['country']
            # tempStreet = request.POST['tempStreet']
            # tempCity = request.POST['tempCity']
            # tempState = request.POST['tempState']
            # tempPincode = request.POST['tempPincode']
            # tempCountry = request.POST['tempCountry']
            
            
            contact = request.POST['Contact_Number']
            emergencycontact = request.POST['Emergency_Contact']
            email = request.POST['Email']
            # file = request.FILES.get('File', None)
            # if file:
            #     file = request.FILES['File']
            # else:
            #     file=''
            bankdetails = request.POST['Bank_Details']
            accoutnumber = request.POST['Account_Number']
            ifsc = request.POST['IFSC']
            bankname = request.POST['BankName']
            branchname = request.POST['BranchName']
            transactiontype = request.POST['Transaction_Type']

            

            if request.POST['tds_applicable'] == 'Yes':
                tdsapplicable = request.POST['tds_applicable']
                tdstype = request.POST['TDS_Type']
                
                if tdstype == 'Amount':
                    tdsvalue = request.POST['TDS_Amount']
                elif tdstype == 'Percentage':
                    tdsvalue = request.POST['TDS_Percentage']
                else:
                    tdsvalue = 0
            elif request.POST['tds_applicable'] == 'No':
                tdsvalue = 0
                tdstype = ''
                tdsapplicable = request.POST['tds_applicable']
            else:
                tdsvalue = 0
                tdstype = ''
                tdsapplicable = ''

            
            
            incometax = request.POST['Income_Tax']
            # aadhar = request.POST['Aadhar']
            uan = request.POST['UAN']
            pf = request.POST['PF']
            pan = request.POST['PAN']
            pr = request.POST['PR']

            if dob == '':
                age = 2
            else:
                dob2 = date.fromisoformat(dob)
                today = date.today()
                age = int(today.year - dob2.year - ((today.month, today.day) < (dob2.month, dob2.day)))
            
            # if Employee.objects.filter(first_name=firstname, company=com).exists():
            #     return JsonResponse({"message": "error"})
            # else:
            new = Employee(first_name = firstname,last_name = lastname,upload_image=image,title = title,date_of_joining = joiningdate,gender = gender ,
                        amount_per_hour = amountperhour ,total_working_hours = workinghour,salary_amount = salaryamount ,employee_salary_type =salary_type,salary_effective_from=salarydate,
                        employee_mail = email,
                        employee_number = employeenumber,employee_designation = designation,
                        employee_current_location = location,
                        mobile = contact,
                        # temporary_street=tempStreet,temporary_state=tempState,temporary_pincode=tempPincode,temporary_country=tempCountry,
                        city=city,street=street,state=state,country=country,pincode=pincode,
                        # temporary_city=tempCity,
                        employee_status = 'Active' ,company_id = com.id,login_id=sid,date_of_birth = dob ,
                        age = age,
                        blood_group = blood,
                        fathers_name_mothers_name = parent,spouse_name = spouse,
                        emergency_contact = emergencycontact,
                        provide_bank_details = bankdetails,account_number = accoutnumber,
                        ifsc = ifsc,name_of_bank = bankname,branch_name = branchname,bank_transaction_type = transactiontype,
                        tds_applicable = tdsapplicable, tds_type = tdstype,percentage_amount = tdsvalue,
                        pan_number = pan,
                        income_tax_number = incometax,
                        # aadhar_number = aadhar,
                        universal_account_number = uan,pf_account_number = pf,
                        pr_account_number = pr,
                        # upload_file = file
                        
                      )
                    #   
                #
          
            new.save()

            history = Employee_History(company_id = com.id,login_id=sid,employee_id = new.id,date = date.today(),action = 'Created')
            history.save()
            return JsonResponse({"message": "success"})

    # elif login.User_Type == 'Staff':
    #     if request.method == 'POST':
    #         staff = LoginDetails.objects.get(id=login_id)
    #         sf = StaffDetails.objects.get(login_details=staff)
    #         c = sf.company
    #         unit_name = request.POST['units']
            
    #         if Unit.objects.filter(unit_name=unit_name, company=c).exists():
    #             return JsonResponse({"message": "error"})
    #         else:
    #             unit = Unit(unit_name=unit_name, company=c)  
    #             unit.save()  
    #             return JsonResponse({"message": "success"})

    # return JsonResponse({"message": "success"})


def add_term(request):                                                                #new by tinto mt (item)
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)

    if login.User_Type == 'Company':
        if request.method == 'POST':
            com = Fin_Company_Details.objects.get(Login_Id = sid)
            allmodules = Fin_Modules_List.objects.get(company_id = com.id)
            duration = request.POST['duration']
            number = request.POST['number']
            
            if Employee_Loan_Term.objects.filter(duration=duration, company=com,term=number).exists():
                return JsonResponse({"message": "error"})
            else:
                term = Employee_Loan_Term(duration=duration, company=com,term=number)  
                term.save()  
                return JsonResponse({"message": "success"})
    if login.User_Type == 'Staff':
        if request.method == 'POST':
            com = Fin_Company_Details.objects.get(Login_Id = sid)
            allmodules = Fin_Modules_List.objects.get(company_id = com.id)
            duration = request.POST['duration']
            number = request.POST['number']
            
            if Employee_Loan_Term.objects.filter(duration=duration, company=com,term=number).exists():
                return JsonResponse({"message": "error"})
            else:
                term = Employee_Loan_Term(duration=duration, company=com,term=number)  
                term.save()  
                return JsonResponse({"message": "success"})
def term_dropdown(request):                                                                 #new by tinto mt (item)
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    if login.User_Type == 'Company':
            com = Fin_Company_Details.objects.get(Login_Id = sid)
            options = {}
            option_objects = Employee_Loan_Term.objects.filter(company=com)
            for option in option_objects:
                duration=option.duration
                term=option.term
            options[option.id] = [duration,term,f"{duration}"]
            return JsonResponse(options)
    
def emp_dropdown(request):                                                                 #new by tinto mt (item)
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    if login.User_Type == 'Company':
            com = Fin_Company_Details.objects.get(Login_Id = sid)
            options = {}
            option_objects = Employee.objects.filter(company=com)
            for option in option_objects:
                title=option.title
                first_name=option.first_name
                last_name=option.last_name
            options[option.id] = [title,first_name,last_name,f"{title}"]
            return JsonResponse(options)


def laon_status_edit(request, pk):                                                                #new by tinto mt
    
    loan = Loan.objects.get(id=pk)

    if loan.status == 'Active':
        loan.status = 'Inactive'
        loan.save()
    elif loan.status != 'Active':
        loan.status = 'Active'
        loan.save()

    loan.save()

    return redirect('emploanoverview',pk)



def add_loan_comment(request,pk):
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    
    if login.User_Type == 'Company':
        com1 = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com1.id)
        loan = Loan.objects.get(id=pk)
        if request.method=="POST":
                    
                    com=Employee_loan_comments()
                    
            
                    comment_comments=request.POST['comment']
                    com.company=com1
                    com.logindetails=login
                    com.comments=comment_comments
                    acc=Loan.objects.get(id=pk)
                    com.employee_loan=acc
                    
                    com.save()
                    return redirect('emploanoverview',pk)
      
        
    elif login.User_Type == 'Staff' :
        staf = Fin_Staff_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
        if request.method=="POST":
                    
                    com=Employee_loan_comments()
                    
            
                    comment_comments=request.POST['comment']
                    com.company=com1
                    com.logindetails=login
                    com.comments=comment_comments
                    acc=Loan.objects.get(id=pk)
                    com.employee_loan=acc
                    
                    com.save()
                    return redirect('emploanoverview',pk)
        

def delete_loan_comment(request,ph,pr):                                                                #new by tinto mt
    acc=Employee_loan_comments.objects.get(id=ph)
    acc.delete()
    ac=Loan.objects.get(id=pr)
    
    return redirect(emploanoverview,ac.id)

def attach_loan_file(request,pk):                       
    estobj= Loan.objects.get(id=pk)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            estobj.attach_file=request.FILES.get('file')
            estobj.save()
            return redirect('emploanoverview',estobj.id)
    
    return redirect(emploanoverview,pk)
    
def delete_loan(request,pk):                                                                #new by tinto mt
    acc=Loan.objects.get(id=pk)
    acc.delete()
  
    
    return redirect(employee_loan_list)


def shareloanToEmail(request,pk):   
    sid = request.session['s_id']
    login = Fin_Login_Details.objects.get(id=sid)
    
    if login.User_Type == 'Company':
        com1 = Fin_Company_Details.objects.get(Login_Id = sid)
        allmodules = Fin_Modules_List.objects.get(company_id = com1.id)
        loan = Loan.objects.get(id=pk)
        try:
            if request.method == 'POST':
                emails_string = request.POST['email_ids']
                # Split the string by commas and remove any leading or trailing whitespace
                emails_list = [email.strip() for email in emails_string.split(',')]
                email_message = request.POST['email_message']
                print(emails_list)
                print('1')
           
           
                loan = Loan.objects.get(id=pk)
                est_comments = Employee_loan_comments.objects.filter(employee_loan=loan)
                employee = Employee.objects.get(id=loan.employee.id)
                trans=Employee_Loan_Transactions.objects.filter(employee_loan=loan)
                latest_item_id=Employee_Loan_History.objects.filter(employee_loan=loan,company=com1)
                context = {
                
                    'loan':loan,
                    'est_comments':est_comments,
                    'employee':employee,
                    'trans':trans,
                    'latest_item_id':latest_item_id


                }
                print('2')
                template_path = 'company/Employee_loan_emailpdf.html'
                print('3')
                template = get_template(template_path)
                print('4')
                html  = template.render(context)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                pdf = result.getvalue()
                print('5')
                filename = f'Item Transactions.pdf'
                subject = f"Transactipns"
                email = EmailMessage(subject, f"Hi,\nPlease find the attached Item transactions. \n{email_message}\n\n--\nRegards,\n", from_email=settings.EMAIL_HOST_USER,to=emails_list)
                email.attach(filename,pdf,"application/pdf")
                email.send(fail_silently=False)
                msg = messages.success(request, 'Details has been shared via email successfully..!')
                return redirect(emploanoverview,pk)
        except Exception as e:
            print(e)
            messages.error(request, f'{e}')
            return redirect(emploanoverview,pk)   
      
        
    # elif login.User_Type == 'Staff' :
    #     staf = Fin_Staff_Details.objects.get(Login_Id = sid)
    #     allmodules = Fin_Modules_List.objects.get(company_id = staf.company_id_id)
    #     try:
    #         if request.method == 'POST':
    #             emails_string = request.POST['email_ids']
    #             # Split the string by commas and remove any leading or trailing whitespace
    #             emails_list = [email.strip() for email in emails_string.split(',')]
    #             email_message = request.POST['email_message']
    #             print(emails_list)
    #             print('1')
           
           
    #             item = Items.objects.get(id=pt)
    #             context = {
                
    #                 'selitem':item,
    #             }
    #             print('2')
    #             template_path = 'zohomodules/items/itememailpdf.html'
    #             print('3')
    #             template = get_template(template_path)
    #             print('4')
    #             html  = template.render(context)
    #             result = BytesIO()
    #             pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    #             pdf = result.getvalue()
    #             print('5')
    #             filename = f'Item Transactions.pdf'
    #             subject = f"Transactipns"
    #             email = EmailMessage(subject, f"Hi,\nPlease find the attached Item transactions. \n{email_message}\n\n--\nRegards,\n{item.item_name}\n{item.item_type}", from_email=settings.EMAIL_HOST_USER,to=emails_list)
    #             email.attach(filename,pdf,"application/pdf")
    #             email.send(fail_silently=False)
    #             msg = messages.success(request, 'Details has been shared via email successfully..!')
    #             return redirect(itemsoverview,pt)
    #     except Exception as e:
    #         print(e)
    #         messages.error(request, f'{e}')
    #         return redirect(itemsoverview,pt)                                                              #new by tinto mt
 