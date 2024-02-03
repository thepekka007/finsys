from django.db import models


class Fin_Payment_Terms(models.Model):
    payment_terms_number = models.IntegerField(null=True,blank=True)  
    payment_terms_value = models.CharField(max_length=100,null=True,blank=True) 
    days = models.CharField(max_length=100,null=True,blank=True) 

class Fin_Login_Details(models.Model):
    First_name = models.CharField(max_length=255,null=True,blank=True)
    Last_name = models.CharField(max_length=255,null=True,blank=True)
    User_name = models.CharField(max_length=255,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    User_Type = models.CharField(max_length=255,null=True,blank=True) 

class Fin_Distributors_Details(models.Model):  
    Login_Id = models.ForeignKey(Fin_Login_Details, on_delete=models.CASCADE,null=True,blank=True)
    Payment_Term =  models.ForeignKey(Fin_Payment_Terms, on_delete=models.CASCADE,null=True,blank=True)
    Distributor_Code = models.CharField(max_length=100,null=True,blank=True)
    Email = models.CharField(max_length=255,null=True,blank=True) 
    Contact = models.CharField(max_length=255,null=True,blank=True)
    Image = models.ImageField(null=True,blank = True,upload_to = 'image/distributor') 
    Start_Date = models.DateField(auto_now_add=True,null=True)
    End_date = models.DateField(max_length=255,null=True,blank=True)
    Admin_approval_status = models.CharField(max_length=255,null=True,blank=True)   

class Fin_Company_Details(models.Model): 
    Payment_Term = models.ForeignKey(Fin_Payment_Terms, on_delete=models.CASCADE,null=True,blank=True)
    Distributor_id = models.ForeignKey(Fin_Distributors_Details, on_delete=models.CASCADE,null=True,blank=True)
    Login_Id = models.ForeignKey(Fin_Login_Details, on_delete=models.CASCADE,null=True,blank=True)
    Company_name = models.CharField(max_length=255,null=True,blank=True)
    Business_name = models.CharField(max_length=255,null=True,blank=True)
    Industry = models.CharField(max_length=255,null=True,blank=True)
    Company_Type = models.CharField(max_length=255,null=True,blank=True)

    Company_Code = models.CharField(max_length=100,null=True,blank=True)
    Email = models.CharField(max_length=255,null=True,blank=True) 
    Contact = models.CharField(max_length=255,null=True,blank=True)
    Address = models.TextField(max_length=255,null=True,blank=True)
    City = models.CharField(max_length=255,null=True,blank=True)
    State = models.CharField(max_length=255,null=True,blank=True)
    Country = models.CharField(max_length=255,null=True,blank=True)
    Pincode = models.IntegerField(null=True,blank=True)
    Pan_NO = models.CharField(max_length=255,null=True,blank=True)
    GST_Type = models.CharField(max_length=255,null=True,blank=True)
    GST_NO = models.CharField(max_length=255,null=True,blank=True)
    Image = models.ImageField(null=True,blank = True,upload_to = 'image/company') 
    Start_Date = models.DateField(auto_now_add=True,null=True)
    End_date = models.DateField(max_length=255,null=True,blank=True)
    Payment_Type = models.CharField(max_length=255,null=True,blank=True)
    Accountant = models.CharField(max_length=255,null=True,blank=True)
    Admin_approval_status = models.CharField(max_length=255,null=True,blank=True)
    Distributor_approval_status = models.CharField(max_length=255,null=True,blank=True)
    Registration_Type = models.CharField(max_length=255,null=True,blank=True)


class Fin_Modules_List(models.Model):
    Login_Id = models.ForeignKey(Fin_Login_Details, on_delete=models.CASCADE,null=True,blank=True)
    company_id = models.ForeignKey(Fin_Company_Details, on_delete=models.CASCADE,null=True,blank=True)

    # -----items-----
    Items = models.IntegerField(null=True,default=0) 
    Price_List = models.IntegerField(null=True,default=0) 
    Stock_Adjustment = models.IntegerField(null=True,default=0) 

    # --------- CASH & BANK-----
    Cash_in_hand = models.IntegerField(null=True,default=0) 
    Offline_Banking = models.IntegerField(null=True,default=0)
    Bank_Reconciliation = models.IntegerField(null=True,default=0)
    UPI = models.IntegerField(null=True,default=0)
    Bank_Holders = models.IntegerField(null=True,default=0)
    Cheque = models.IntegerField(null=True,default=0)
    Loan_Account = models.IntegerField(null=True,default=0)

    #  ------SALES MODULE -------
    Customers  = models.IntegerField(null=True,default=0)
    Invoice = models.IntegerField(null=True,default=0) 
    Estimate = models.IntegerField(null=True,default=0) 
    Sales_Order = models.IntegerField(null=True,default=0) 
    Recurring_Invoice = models.IntegerField(null=True,default=0) 
    Retainer_Invoice = models.IntegerField(null=True,default=0) 
    Credit_Note = models.IntegerField(null=True,default=0) 
    Payment_Received = models.IntegerField(null=True,default=0) 
    Delivery_Challan = models.IntegerField(null=True,default=0)


    #  ---------PURCHASE MODULE--------- 
    Vendors = models.IntegerField(null=True,default=0) 
    Bills = models.IntegerField(null=True,default=0) 
    Recurring_Bills = models.IntegerField(null=True,default=0) 
    Debit_Note = models.IntegerField(null=True,default=0) 
    Purchase_Order = models.IntegerField(null=True,default=0) 
    Expenses = models.IntegerField(null=True,default=0) 
    Recurring_Expenses = models.IntegerField(null=True,default=0) 
    Payment_Made = models.IntegerField(null=True,default=0) 

    # --------EWay_Bill-----
    EWay_Bill = models.IntegerField(null=True,default=0) 


    #  -------ACCOUNTS--------- 
    Chart_of_Accounts = models.IntegerField(null=True,default=0)  
    Manual_Journal = models.IntegerField(null=True,default=0)  
    Reconcile = models.IntegerField(null=True,default=0) 


    # -------PAYROLL------- 
    Employees = models.IntegerField(null=True,default=0) 
    Employees_Loan = models.IntegerField(null=True,default=0)  
    Holiday = models.IntegerField(null=True,default=0) 
    Attendance = models.IntegerField(null=True,default=0) 
    Salary_Details = models.IntegerField(null=True,default=0) 


    update_action = models.IntegerField(null=True,default=0) 
    status = models.CharField(max_length=100,null=True,default='New')  


class Fin_Staff_Details(models.Model):
    company_id = models.ForeignKey(Fin_Company_Details, on_delete=models.CASCADE,null=True,blank=True)
    Login_Id = models.ForeignKey(Fin_Login_Details, on_delete=models.CASCADE,null=True,blank=True)
    contact = models.CharField(max_length=255,null=True,blank=True)
    Email = models.CharField(max_length=255,null=True,blank=True) 
    img = models.ImageField(null=True,blank = True,upload_to = 'image/staff')    
    Company_approval_status = models.CharField(max_length=255,null=True,blank=True)  

class Fin_Payment_Terms_updation(models.Model):
    Login_Id = models.ForeignKey(Fin_Login_Details, on_delete=models.CASCADE,null=True,blank=True)
    Payment_Term = models.ForeignKey(Fin_Payment_Terms, on_delete=models.CASCADE,null=True,blank=True)

    status = models.CharField(max_length=100,null=True,default='New') 


class Fin_ANotification(models.Model): 
    Login_Id = models.ForeignKey(Fin_Login_Details, on_delete=models.CASCADE,null=True,blank=True)
    Modules_List = models.ForeignKey(Fin_Modules_List, on_delete=models.CASCADE,null=True,blank=True)
    PaymentTerms_updation = models.ForeignKey(Fin_Payment_Terms_updation, on_delete=models.CASCADE,null=True,blank=True)
    
    Title = models.CharField(max_length=255,null=True,blank=True)
    Discription = models.CharField(max_length=255,null=True,blank=True) 
    Noti_date = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=100,null=True,default='New')  

class Fin_DNotification(models.Model): 
    Login_Id = models.ForeignKey(Fin_Login_Details, on_delete=models.CASCADE,null=True,blank=True)
    Distributor_id = models.ForeignKey(Fin_Distributors_Details, on_delete=models.CASCADE,null=True,blank=True)
    Modules_List = models.ForeignKey(Fin_Modules_List, on_delete=models.CASCADE,null=True,blank=True)
    PaymentTerms_updation = models.ForeignKey(Fin_Payment_Terms_updation, on_delete=models.CASCADE,null=True,blank=True)
    
    Title = models.CharField(max_length=255,null=True,blank=True)
    Discription = models.CharField(max_length=255,null=True,blank=True) 
    Noti_date = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=100,null=True,default='New')     

class Fin_CNotification(models.Model): 
    Login_Id = models.ForeignKey(Fin_Login_Details, on_delete=models.CASCADE,null=True,blank=True)
    Company_id = models.ForeignKey(Fin_Company_Details, on_delete=models.CASCADE,null=True,blank=True)
  
    
    Title = models.CharField(max_length=255,null=True,blank=True)
    Discription = models.CharField(max_length=255,null=True,blank=True) 
    Noti_date = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=100,null=True,default='New')      
       

class Employee(models.Model):
    upload_file = models.FileField(upload_to='file/',blank=True) 
    upload_image = models.ImageField(upload_to='media/',blank=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    alias = models.CharField(max_length=255,null=True,blank=True)
    employee_mail = models.EmailField(null=True,blank=True)
    employee_number = models.CharField(max_length=255,null=True,blank=True)
    employee_designation = models.CharField(max_length=255,null=True,blank=True)
    function = models.CharField(max_length=255,null=True,blank=True)
    employee_current_location = models.CharField(max_length=255,null=True,blank=True)
    mobile = models.CharField(max_length=255,null=True,blank=True)
    date_of_joining = models.DateField(null=True,blank=True)
    employee_salary_type = models.CharField(max_length=255,null=True,blank=True)
    salary_details = models.CharField(max_length=10,null=True,blank=True)
    salary_effective_from = models.CharField(max_length=255,null=True,blank=True)

    pay_head = models.CharField(max_length=255,null=True,blank=True)
    salary_amount = models.FloatField(null=True,blank=True)
    amount_per_hour = models.IntegerField(null=True,blank=True)
    total_working_hours = models.IntegerField(null=True,blank=True)
    gender = models.CharField(max_length=255,null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    blood_group = models.CharField(max_length=255,null=True,blank=True)
    fathers_name_mothers_name = models.CharField(max_length=255,null=True,blank=True)
    spouse_name = models.CharField(max_length=255,null=True,blank=True)
    emergency_contact = models.CharField(max_length=255,null=True,blank=True)
    provide_bank_details = models.CharField(max_length=255,null=True,blank=True)
    account_number = models.CharField(max_length=255,null=True,blank=True)
    ifsc = models.CharField(max_length=255,null=True,blank=True)
    name_of_bank = models.CharField(max_length=255,null=True,blank=True)
    branch_name = models.CharField(max_length=255,null=True,blank=True)
    bank_transaction_type = models.CharField(max_length=255,null=True,blank=True)
    tds_applicable = models.CharField(max_length=255,null=True,blank=True)
    tds_type = models.CharField(max_length=255,null=True,blank=True)
    percentage_amount = models.IntegerField(null=True,blank=True)
    pan_number = models.CharField(max_length=255,null=True,blank=True)
    income_tax_number = models.CharField(max_length=255,null=True,blank=True)
    aadhar_number = models.CharField(max_length=255,null=True,blank=True)
    universal_account_number = models.CharField(max_length=255,null=True,blank=True)
    pf_account_number = models.CharField(max_length=255,null=True,blank=True)
    pr_account_number = models.CharField(max_length=255,null=True,blank=True)
    esi_number = models.CharField(max_length=255,null=True,blank=True)

    street = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    pincode = models.CharField(max_length=255,null=True,blank=True)
    country = models.CharField(max_length=255,null=True,blank=True)
    temporary_street = models.CharField(max_length=255,null=True,blank=True)
    temporary_city = models.CharField(max_length=255,null=True,blank=True)
    temporary_state = models.CharField(max_length=255,null=True,blank=True)
    temporary_pincode = models.CharField(max_length=255,null=True,blank=True)
    temporary_country = models.CharField(max_length=255,null=True,blank=True)
    employee_status = models.CharField(max_length=30,null=True,blank=True)
    company = models.ForeignKey(Fin_Company_Details,on_delete=models.CASCADE,null=True,blank=True)
    login = models.ForeignKey(Fin_Login_Details,on_delete=models.CASCADE,null=True,blank=True)

class Employee_History(models.Model):
    company = models.ForeignKey(Fin_Company_Details,on_delete=models.CASCADE,null=True,blank=True)
    login = models.ForeignKey(Fin_Login_Details,on_delete=models.CASCADE,null=True,blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,blank=True,null=True)
    
    date = models.DateField(null=True,blank=True)
    action = models.CharField(max_length=255,null=True,blank=True)
class Employee_Blood_Group(models.Model):
    blood_group = models.CharField(max_length=255,null=True,blank=True)
    company = models.ForeignKey(Fin_Company_Details,on_delete=models.CASCADE,null=True,blank=True)
    login = models.ForeignKey(Fin_Login_Details,on_delete=models.CASCADE,null=True,blank=True)



# tinto modals
class Employee_Loan_Term(models.Model):
    duration= models.IntegerField(null=True,blank=True)
    term = models.CharField(max_length=255,null=True,blank=True)
    company = models.ForeignKey(Fin_Company_Details,on_delete=models.CASCADE,null=True,blank=True)
    

    

class Loan(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    employee_name = models.CharField(max_length=255,null=True,blank=True)
    employeeid = models.CharField(max_length=255,null=True,blank=True)
    employee_email = models.EmailField(max_length=255,null=True,blank=True)
    salary = models.IntegerField(null=True,blank=True)
    join_date = models.DateField(null=True,blank=True)
    loan_date = models.DateField(null=True,blank=True)
    loan_amount = models.IntegerField(null=True,blank=True)
    total_loan=models.IntegerField(null=True,blank=True)
    loan_duration = models.ForeignKey(Employee_Loan_Term,on_delete=models.CASCADE,null=True,blank=True)
    expiry_date = models.DateField(null=True,blank=True)
    payment_method = models.CharField(max_length=255,null=True,blank=True)
    cheque_number = models.CharField(max_length=255,null=True,blank=True)
    upi_id = models.CharField(max_length=255,null=True,blank=True)
    
    bank_account = models.CharField(max_length=255,null=True,blank=True)
    monthly_cutting= models.CharField(max_length=255,null=True,blank=True)
    monthly_cutting_percentage = models.IntegerField(null=True,blank=True)
    monthly_cutting_amount = models.IntegerField(null=True,blank=True)
    note = models.CharField(max_length=255,null=True,blank=True)
    attach_file = models.FileField(upload_to='file/',blank=True) 
    company = models.ForeignKey(Fin_Company_Details,on_delete=models.CASCADE,null=True,blank=True)
    login_details = models.ForeignKey(Fin_Login_Details,on_delete=models.CASCADE,null=True,blank=True)
    
    status = models.CharField(max_length=255,null=True,blank=True,default='Active')
    balance = models.IntegerField(null=True,blank=True)


class Employee_Loan_History(models.Model):
    company = models.ForeignKey(Fin_Company_Details,on_delete=models.CASCADE,null=True,blank=True)
    login_details = models.ForeignKey(Fin_Login_Details,on_delete=models.CASCADE,null=True,blank=True)
    employee_loan = models.ForeignKey(Loan,on_delete=models.CASCADE,blank=True,null=True)
    date = models.DateField(null=True,blank=True)
    action = models.CharField(max_length=255,null=True,blank=True)

class Employee_Additional_Loan(models.Model):
    balance_loan=models.IntegerField(null=True,blank=True)
    new_loan=models.IntegerField(null=True,blank=True)
    total_loan=models.IntegerField(null=True,blank=True)
    payment_method=models.CharField(max_length=255,null=True,blank=True)
    cheque_number = models.CharField(max_length=255,null=True,blank=True)
    upi_id = models.CharField(max_length=255,null=True,blank=True)
    bank_account = models.CharField(max_length=255,null=True,blank=True)
    new_date=models.DateField(null=True,blank=True)

    company = models.ForeignKey(Fin_Company_Details,on_delete=models.CASCADE,null=True,blank=True)
    login_details = models.ForeignKey(Fin_Login_Details,on_delete=models.CASCADE,null=True,blank=True)
    employee_loan = models.ForeignKey(Loan,on_delete=models.CASCADE,blank=True,null=True)

class Employee_Loan_Repayment(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    principle_amount=models.IntegerField(null=True,blank=True)
    new_loan=models.IntegerField(null=True,blank=True)
    interest_amount=models.IntegerField(null=True,blank=True)
    payment_date = models.DateField(null=True,blank=True)
    payment_method=models.CharField(max_length=255,null=True,blank=True)
    total_amount=models.IntegerField(null=True,blank=True)
    cheque_number = models.CharField(max_length=255,null=True,blank=True)
    upi_id = models.CharField(max_length=255,null=True,blank=True)
    bank_account = models.CharField(max_length=255,null=True,blank=True)
    company = models.ForeignKey(Fin_Company_Details,on_delete=models.CASCADE,null=True,blank=True)
    login_details = models.ForeignKey(Fin_Login_Details,on_delete=models.CASCADE,null=True,blank=True)
    employee_loan = models.ForeignKey(Loan,on_delete=models.CASCADE,blank=True,null=True)
    balance = models.IntegerField(null=True,blank=True)

class Employee_Loan_Transactions(models.Model):
    company = models.ForeignKey(Fin_Company_Details,on_delete=models.CASCADE,null=True,blank=True)
    login_details = models.ForeignKey(Fin_Login_Details,on_delete=models.CASCADE,null=True,blank=True)
    employee_loan = models.ForeignKey(Loan,on_delete=models.CASCADE,blank=True,null=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,blank=True,null=True)
    particulars = models.CharField(max_length=255,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    repayment = models.ForeignKey(Employee_Loan_Repayment,on_delete=models.CASCADE,null=True,blank=True)
    additional = models.ForeignKey(Employee_Additional_Loan,on_delete=models.CASCADE,null=True,blank=True)
    balance= models.IntegerField(null=True,blank=True)

class Employee_loan_comments(models.Model):                                         
    company=models.ForeignKey(Fin_Company_Details,on_delete=models.CASCADE)
    logindetails=models.ForeignKey(Fin_Login_Details,on_delete=models.CASCADE)
    employee_loan=models.ForeignKey(Loan,on_delete=models.CASCADE)
    comments = models.CharField(max_length=255,null=True,blank=True)