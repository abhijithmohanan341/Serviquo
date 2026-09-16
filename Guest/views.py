from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *
from ServiceProvider.models import *
from Company.models import *
from Shop.models import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def UserRegistration(request):
    userregistrationdata=tbl_user.objects.all()
    districtdata=tbl_district.objects.all().order_by('district_name')
    placedata=tbl_place.objects.all().order_by('place_name')
    if request.method=='POST':
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        address=request.POST.get('txt_address')
        district=tbl_district.objects.get(id=request.POST.get('sel_district'))
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))
        photo=request.FILES.get('file_photo')
        proof=request.FILES.get('file_proof')
        password=request.POST.get('txt_password')
        conpassword=request.POST.get('txt_conpassword')
        if password == conpassword:
            checkemail=tbl_admin.objects.filter(admin_email=email).count()
            checkuseremail=tbl_user.objects.filter(user_email=email).count()
            checkcompanyemail=tbl_company.objects.filter(company_email=email).count()
            checkserviceprovideremail=tbl_serviceprovider.objects.filter(serviceprovider_email=email).count()
            checkshopemail=tbl_shop.objects.filter(shop_email=email).count()
            checktechnicianemail=tbl_technician.objects.filter(technician_email=email).count()
            if checkemail > 0 :
                return render(request,"Guest/UserRegistration.html",{'msg':"Email Already Exist"})
            elif checkuseremail > 0 :
                return render(request,"Guest/UserRegistration.html",{'msg':"Email Already Exist"})
            elif checkcompanyemail > 0 :
                return render(request,"Guest/UserRegistration.html",{'msg':"Email Already Exist"})
            elif checkserviceprovideremail > 0 :
                return render(request,"Guest/UserRegistration.html",{'msg':"Email Already Exist"})
            elif checkshopemail > 0 :
                return render(request,"Guest/UserRegistration.html",{'msg':"Email Already Exist"})
            elif checktechnicianemail > 0 :
                return render(request,"Guest/UserRegistration.html",{'msg':"Email Already Exist"})
            else:
                tbl_user.objects.create(user_name=name,user_email=email,user_contact=contact,user_address=address,place=place,user_photo=photo,user_proof=proof,user_password=password)
                return render(request,"Guest/Login.html",{'msg':"Registration Sucessfilly Completed"})
        else:
            return render(request,"Guest/UserRegistration.html",{'msg':"Confirm Password Mismatch"})
    else:
        return render(request,'Guest/UserRegistration.html',{'userregistration':userregistrationdata,'district':districtdata,'place':placedata})
    


def ajaxplace(request):
    districtid=tbl_district.objects.get(id=request.GET.get('did'))
    placedata=tbl_place.objects.filter(district=districtid)
    return render(request,'Guest/Ajaxplace.html',{'place':placedata})



def Login(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")

        admincount = tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        usercount = tbl_user.objects.filter(user_email=email,user_password=password).count()
        companycount=tbl_company.objects.filter(company_email=email,company_password=password).count()
        serviceprovidercount=tbl_serviceprovider.objects.filter(serviceprovider_email=email,serviceprovider_password=password).count()
        techniciancount=tbl_technician.objects.filter(technician_email=email,technician_password=password).count()
        shopcount=tbl_shop.objects.filter(shop_email=email,shop_password=password).count()
        
        if admincount > 0:
            admindata = tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session['aid'] = admindata.id
            request.session['aname'] = admindata.admin_name
            return redirect("Admin:homepage")
        
        elif usercount > 0:
            userdata = tbl_user.objects.get(user_email=email,user_password=password)
            if userdata.user_status == 1:
                return render(request,'Guest/Login.html',{'msg':"Your account has been suspended. Please contact support."})
            else:
                request.session['uid'] = userdata.id
                request.session['uname'] = userdata.user_name
                return redirect("User:homepage")
        
        elif companycount > 0:
            companydata = tbl_company.objects.get(company_email=email,company_password=password)
            if companydata.company_status == 0:
                return render(request,'Guest/Login.html',{'msg':"Account pending approval. Status will be send your email"})
            elif companydata.company_status == 2:
                return render(request,'Guest/Login.html',{'msg':"Registration Rejected, Please Contact Serviquo Team"})
            else:
                request.session['cid'] = companydata.id
                request.session['cname'] = companydata.company_name
                return redirect("Company:homepage")
        
    
        elif serviceprovidercount > 0:
            serviceproviderdata = tbl_serviceprovider.objects.get(serviceprovider_email=email,serviceprovider_password=password)
            if serviceproviderdata.serviceprovider_status == 0:
                return render(request,'Guest/Login.html',{'msg':"Account pending approval. Status will be send your email"})
            elif serviceproviderdata.serviceprovider_status == 2:
                return render(request,'Guest/Login.html',{'msg':"Registration Rejected, Please Contact Serviquo Team"})
            else:
                request.session['sid'] = serviceproviderdata.id
                request.session['sname'] = serviceproviderdata.serviceprovider_name
                return redirect("ServiceProvider:homepage")
        
        elif techniciancount > 0:
            techniciandata = tbl_technician.objects.get(technician_email=email,technician_password=password)
            request.session['tid'] = techniciandata.id
            request.session['tname'] = techniciandata.technician_name
            return redirect("Technician:homepage")
        

        elif shopcount > 0:
            shopdata = tbl_shop.objects.get(shop_email=email,shop_password=password)
            if shopdata.shop_status == 0:
                return render(request,'Guest/Login.html',{'msg':"Account pending approval. Status will be send your email."})
            elif shopdata.shop_status == 2:
                return render(request,'Guest/Login.html',{'msg':"Registration Rejected, Please Contact Serviquo Team"})
            else:
                request.session['shopid'] = shopdata.id
                request.session['shopname'] = shopdata.shop_name
                return redirect("Shop:homepage")
        else:
            return render(request,'Guest/Login.html',{'msg':"Invalid Email Or Password"})
    else:
        return render(request,'Guest/Login.html')
    



def CompanyRegistration(request):
    companyregistrationdata=tbl_company.objects.all()
    districtdata=tbl_district.objects.all().order_by('district_name')
    placedata=tbl_place.objects.all().order_by('place_name')
    branddata=tbl_brand.objects.all().order_by('brand_name')
    if request.method=='POST':
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        address=request.POST.get('txt_address')
        district=tbl_district.objects.get(id=request.POST.get('sel_district'))
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))
        brand=tbl_brand.objects.get(id=request.POST.get('sel_brand'))
        logo=request.FILES.get('file_logo')
        proof=request.FILES.get('file_proof')
        password=request.POST.get('txt_password')
        conpassword=request.POST.get('txt_conpassword')
        if password == conpassword:
            checkemail=tbl_admin.objects.filter(admin_email=email).count()
            checkuseremail=tbl_user.objects.filter(user_email=email).count()
            checkcompanyemail=tbl_company.objects.filter(company_email=email).count()
            checkserviceprovideremail=tbl_serviceprovider.objects.filter(serviceprovider_email=email).count()
            checkshopemail=tbl_shop.objects.filter(shop_email=email).count()
            checktechnicianemail=tbl_technician.objects.filter(technician_email=email).count()
            if checkemail > 0 :
                return render(request,"Guest/CompanyRegistration.html",{'msg':"Email Already Exist"})
            elif checkuseremail > 0 :
                return render(request,"Guest/CompanyRegistration.html",{'msg':"Email Already Exist"})
            elif checkcompanyemail > 0 :
                return render(request,"Guest/CompanyRegistration.html",{'msg':"Email Already Exist"})
            elif checkserviceprovideremail > 0 :
                return render(request,"Guest/CompanyRegistration.html",{'msg':"Email Already Exist"})
            elif checkshopemail > 0 :
                return render(request,"Guest/CompanyRegistration.html",{'msg':"Email Already Exist"})
            elif checktechnicianemail > 0 :
                return render(request,"Guest/CompanyRegistration.html",{'msg':"Email Already Exist"})
            else:
                tbl_company.objects.create(company_name=name,company_email=email,company_contact=contact,company_address=address,place=place,brand=brand,company_logo=logo,company_proof=proof,company_password=password)
                return render(request,"Guest/Login.html",{'msg':"Registration Sucessfilly Completed"})
        else:
            return render(request,"Guest/CompanyRegistration.html",{'msg':"Confirm Password Mismatch"})
    else:
        return render(request,'Guest/CompanyRegistration.html',{'companyregistration':companyregistrationdata,'district':districtdata,'place':placedata,'brand':branddata})
        



def ServiceProviderRegistration(request):
    serviceproviderdata=tbl_serviceprovider.objects.all()
    districtdata=tbl_district.objects.all().order_by('district_name')
    placedata=tbl_place.objects.all().order_by('place_name')
    experiencedata = tbl_experience.objects.all()
    if request.method=='POST':
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        address=request.POST.get('txt_address')
        district=tbl_district.objects.get(id=request.POST.get('sel_district'))
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))
        photo=request.FILES.get('file_photo')
        proof=request.FILES.get('file_proof')
        password=request.POST.get('txt_password')
        conpassword=request.POST.get('txt_conpassword')
        experience = tbl_experience.objects.get(id=request.POST.get('sel_experience'))
        if password == conpassword:
            checkemail=tbl_admin.objects.filter(admin_email=email).count()
            checkuseremail=tbl_user.objects.filter(user_email=email).count()
            checkcompanyemail=tbl_company.objects.filter(company_email=email).count()
            checkserviceprovideremail=tbl_serviceprovider.objects.filter(serviceprovider_email=email).count()
            checkshopemail=tbl_shop.objects.filter(shop_email=email).count()
            checktechnicianemail=tbl_technician.objects.filter(technician_email=email).count()
            if checkemail > 0 :
                return render(request,"Guest/ServiceProviderRegistration.html",{'msg':"Email Already Exist"})
            elif checkuseremail > 0 :
                return render(request,"Guest/ServiceProviderRegistration.html",{'msg':"Email Already Exist"})
            elif checkcompanyemail > 0 :
                return render(request,"Guest/ServiceProviderRegistration.html",{'msg':"Email Already Exist"})
            elif checkserviceprovideremail > 0 :
                return render(request,"Guest/ServiceProviderRegistration.html",{'msg':"Email Already Exist"})
            elif checkshopemail > 0 :
                return render(request,"Guest/ServiceProviderRegistration.html",{'msg':"Email Already Exist"})
            elif checktechnicianemail > 0 :
                return render(request,"Guest/ServiceProviderRegistration.html",{'msg':"Email Already Exist"})
            else:
                tbl_serviceprovider.objects.create(serviceprovider_name=name,serviceprovider_email=email,serviceprovider_contact=contact,serviceprovider_address=address,place=place,experience=experience,serviceprovider_photo=photo,serviceprovider_proof=proof,serviceprovider_password=password)
                return render(request,"Guest/Login.html",{'msg':"Registration Sucessfilly Completed"})
        else:
            return render(request,"Guest/ServiceProviderRegistration.html",{'msg':"Confirm Password Mismatch"})
    else:
        return render(request,'Guest/ServiceProviderRegistration.html',{'serviceproviderregistration':serviceproviderdata,'district':districtdata,'place':placedata,'experience':experiencedata})
    


def ShopRegistration(request):
    shopdata=tbl_shop.objects.all()
    districtdata=tbl_district.objects.all().order_by('district_name')
    placedata=tbl_place.objects.all().order_by('place_name')
    if request.method=='POST':
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        address=request.POST.get('txt_address')
        district=tbl_district.objects.get(id=request.POST.get('sel_district'))
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))
        photo=request.FILES.get('file_photo')
        proof=request.FILES.get('file_proof')
        password=request.POST.get('txt_password')
        conpassword=request.POST.get('txt_conpassword')
        if password == conpassword:
            checkemail=tbl_admin.objects.filter(admin_email=email).count()
            checkuseremail=tbl_user.objects.filter(user_email=email).count()
            checkcompanyemail=tbl_company.objects.filter(company_email=email).count()
            checkserviceprovideremail=tbl_serviceprovider.objects.filter(serviceprovider_email=email).count()
            checkshopemail=tbl_shop.objects.filter(shop_email=email).count()
            checktechnicianemail=tbl_technician.objects.filter(technician_email=email).count()
            if checkemail > 0 :
                return render(request,"Guest/ShopRegistration.html",{'msg':"Email Already Exist"})
            elif checkuseremail > 0 :
                return render(request,"Guest/ShopRegistration.html",{'msg':"Email Already Exist"})
            elif checkcompanyemail > 0 :
                return render(request,"Guest/ShopRegistration.html",{'msg':"Email Already Exist"})
            elif checkserviceprovideremail > 0 :
                return render(request,"Guest/ShopRegistration.html",{'msg':"Email Already Exist"})
            elif checkshopemail > 0 :
                return render(request,"Guest/ShopRegistration.html",{'msg':"Email Already Exist"})
            elif checktechnicianemail > 0 :
                return render(request,"Guest/ShopRegistration.html",{'msg':"Email Already Exist"})
            else:
                tbl_shop.objects.create(shop_name=name,shop_email=email,shop_contact=contact,shop_address=address,place=place,shop_photo=photo,shop_proof=proof,shop_password=password)
                return render(request,"Guest/Login.html",{'msg':"Registration Sucessfilly Completed"})
        else:
            return render(request,"Guest/ShopRegistration.html",{'msg':"Confirm Password Mismatch"})
    else:
        return render(request,'Guest/ShopRegistration.html',{'shopregistration':shopdata,'district':districtdata,'place':placedata})


def Index(request):
    return render(request,'Guest/index.html')


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        otp = random.randint(111111, 999999)

        usertype = None
        userid = None

        if tbl_user.objects.filter(user_email=email).exists():
            data = tbl_user.objects.get(user_email=email)
            usertype = "user"
            userid = data.id

        elif tbl_admin.objects.filter(admin_email=email).exists():
            data = tbl_admin.objects.get(admin_email=email)
            usertype = "admin"
            userid = data.id

        elif tbl_company.objects.filter(company_email=email).exists():
            data = tbl_company.objects.get(company_email=email)
            usertype = "company"
            userid = data.id

        elif tbl_serviceprovider.objects.filter(serviceprovider_email=email).exists():
            data = tbl_serviceprovider.objects.get(serviceprovider_email=email)
            usertype = "serviceprovider"
            userid = data.id

        elif tbl_technician.objects.filter(technician_email=email).exists():
            data = tbl_technician.objects.get(technician_email=email)
            usertype = "technician"
            userid = data.id

        elif tbl_shop.objects.filter(shop_email=email).exists():
            data = tbl_shop.objects.get(shop_email=email)
            usertype = "shop"
            userid = data.id

        else:
            return render(request,"Guest/ForgotPassword.html",{"msg":"Email not found"})

        request.session["otp"] = otp
        request.session["fid"] = userid
        request.session["usertype"] = usertype


        send_mail(
            subject='Serviquo | Password Reset OTP',
            message=(
                f"Dear User,\n\n"
                f"We received a request to reset your password for your Serviquo account.\n\n"
                f"Your One-Time Password (OTP) is: {otp}\n\n"
                f"This OTP is valid for a limited time. Please do not share it with anyone for security reasons.\n\n"
                f"If you did not request this, please ignore this email or contact our support team.\n\n"
                f"Regards,\n"
                f"Serviquo Team"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return redirect("Guest:otp")

    else:
        return render(request,"Guest/ForgotPassword.html")

def otp(request):
    if request.method == "POST":
        inp_otp = int(request.POST.get("txt_otp"))

        if inp_otp == request.session["otp"]:
            return redirect("Guest:newpass")
        else:
            return render(request,"Guest/OTP.html",{"msg":"OTP Does not Match"})

    else:
        return render(request,"Guest/OTP.html")


def newpass(request):
    if request.method == "POST":

        newpass = request.POST.get("txt_new_pass")
        conpass = request.POST.get("txt_con_pass")

        if newpass != conpass:
            return render(request,"Guest/NewPassword.html",{"msg":"Password mismatch"})

        userid = request.session["fid"]
        usertype = request.session["usertype"]

        if usertype == "user":
            data = tbl_user.objects.get(id=userid)
            data.user_password = newpass
            data.save()

        elif usertype == "admin":
            data = tbl_admin.objects.get(id=userid)
            data.admin_password = newpass
            data.save()

        elif usertype == "company":
            data = tbl_company.objects.get(id=userid)
            data.company_password = newpass
            data.save()

        elif usertype == "serviceprovider":
            data = tbl_serviceprovider.objects.get(id=userid)
            data.serviceprovider_password = newpass
            data.save()

        elif usertype == "technician":
            data = tbl_technician.objects.get(id=userid)
            data.technician_password = newpass
            data.save()

        elif usertype == "shop":
            data = tbl_shop.objects.get(id=userid)
            data.shop_password = newpass
            data.save()

        return render(request,"Guest/Login.html",{"msg":"Password Updated Successfully"})

    else:
        return render(request,"Guest/NewPassword.html")


def allregistrations(request):
    return render(request,'Guest/AllRegistrations.html')



def AjaxEmailCheck(request):
    email = request.GET.get('email')
    
    check_admin = tbl_admin.objects.filter(admin_email=email).exists()
    check_user = tbl_user.objects.filter(user_email=email).exists()
    check_company = tbl_company.objects.filter(company_email=email).exists()
    check_provider = tbl_serviceprovider.objects.filter(serviceprovider_email=email).exists()
    check_shop = tbl_shop.objects.filter(shop_email=email).exists()
    check_technician = tbl_technician.objects.filter(technician_email=email).exists()
    
    if check_admin or check_user or check_company or check_provider or check_shop or check_technician:
        exists = True
    else:
        exists = False
        
    return JsonResponse({'exists': exists})




