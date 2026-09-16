from django.shortcuts import render,redirect
from Admin.models import *
from Company.models import *
from User.models import *
from ServiceProvider.models import *
from django.db.models import Sum, Count
from itertools import chain
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.functions import ExtractMonth
import json


def homepage(request):

    if "aid" not in request.session:
        return redirect("Guest:Login")

    admin = tbl_admin.objects.get(id=request.session['aid'])

    shop_pending = tbl_shop.objects.filter(shop_status=0).count()
    company_pending = tbl_company.objects.filter(company_status=0).count()
    sp_pending = tbl_serviceprovider.objects.filter(serviceprovider_status=0).count()

    total_pending = shop_pending + company_pending + sp_pending

    complaintuserdata = tbl_complaint.objects.filter(user__isnull=False).order_by('-complaint_date')[:5]
    complaintcompanydata = tbl_complaint.objects.filter(company__isnull=False).order_by('-complaint_date')[:5]
    complaintserviceproviderdata = tbl_complaint.objects.filter(serviceprovider__isnull=False).order_by('-complaint_date')[:5]
    complaintshopdata = tbl_complaint.objects.filter(shop__isnull=False).order_by('-complaint_date')[:5]

    feedbackdata = tbl_feedback.objects.all().order_by('-feedback_date')[:5]

    context = {
        'admin': admin,
        'usercount': tbl_user.objects.count(),
        'companycount': tbl_company.objects.count(),
        'shopcount': tbl_shop.objects.count(),
        'techniciancount': tbl_technician.objects.count(),
        'serviceprovidercount': tbl_serviceprovider.objects.count(),
        'serviceproviderreq': tbl_servicerequest.objects.count(),
        'companyservice': tbl_companyservice.objects.count(),
        'booking': tbl_booking.objects.count(),

        'shop_pending': shop_pending,
        'company_pending': company_pending,
        'sp_pending': sp_pending,
        'total_pending': total_pending,

        'complaintuserdata': complaintuserdata,
        'complaintcompanydata': complaintcompanydata,
        'complaintserviceproviderdata': complaintserviceproviderdata,
        'complaintshopdata': complaintshopdata,
        'feedbackdata': feedbackdata
    }

    month_map = {
        1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
        7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'
    }

    c_raw = tbl_companyservice.objects.annotate(
        m=ExtractMonth('companyservice_date')
    ).values('m').annotate(c=Count('id')).order_by('m')

    context['c_labels'] = json.dumps([month_map.get(x['m'],'NA') for x in c_raw])
    context['c_counts'] = json.dumps([x['c'] for x in c_raw])

    r_raw = tbl_servicerequest.objects.annotate(
        m=ExtractMonth('servicerequest_date')
    ).values('m').annotate(c=Count('id')).order_by('m')

    context['r_labels'] = json.dumps([month_map.get(x['m'],'NA') for x in r_raw])
    context['r_counts'] = json.dumps([x['c'] for x in r_raw])

    b_raw = tbl_booking.objects.values(
        'tbl_cart__product__shop__shop_name'
    ).annotate(c=Count('id')).order_by('tbl_cart__product__shop__shop_name')

    b_l = []
    b_c = []

    for b in b_raw:
        b_l.append(b['tbl_cart__product__shop__shop_name'])
        b_c.append(b['c'])

    context['b_labels'] = json.dumps(b_l)
    context['b_counts'] = json.dumps(b_c)

    bookings = tbl_booking.objects.exclude(booking_date=None)

    month_counter = {
        'Jan':0,'Feb':0,'Mar':0,'Apr':0,'May':0,'Jun':0,
        'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0
    }

    for b in bookings:
        m = b.booking_date.month
        month_name = month_map.get(m)
        if month_name:
            month_counter[month_name] += 1

    m_labels = []
    m_counts = []

    for k,v in month_counter.items():
        if v > 0:
            m_labels.append(k)
            m_counts.append(v)

    context['m_labels'] = json.dumps(m_labels)
    context['m_counts'] = json.dumps(m_counts)

    return render(request,"Admin/HomePage.html",context)



def district(request):
        if "aid" not in  request.session :
            return redirect("Guest:Login")
        else:
            districtdata = tbl_district.objects.order_by('district_name')
            if request.method == 'POST':
                dis = request.POST.get('txt_district')
                if tbl_district.objects.filter(district_name=dis):
                    return render(request,"Admin/District.html",{'dis':dis,'msg':"District Already Exists"})
                else:
                    tbl_district.objects.create(district_name=dis)
                    return render(request, "Admin/District.html", {'dis':dis,'msg': "District Added Successfully"})
            else:
                return render(request, 'Admin/District.html', {'district': districtdata})

    
    
def deletedistrict(request, did):
    tbl_district.objects.get(id=did).delete()
    districtdata = tbl_district.objects.order_by('district_name')
    return render(request, "Admin/District.html", {'msg': "Data Deleted.",'district': districtdata})




def editdistrict(request, eid):
    editdata = tbl_district.objects.get(id=eid)
    districtdata = tbl_district.objects.order_by('district_name')

    if request.method == "POST":
        dis = request.POST.get('txt_district')
        editdata.district_name = dis
        editdata.save()
        return render(request, "Admin/District.html", {'msg': "Data Updated.."})
    else:
        return render(request, "Admin/District.html", {'editdata': editdata,'district': districtdata})

    


def AdminRegistration(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        admindata=tbl_admin.objects.all()
        if request.method=='POST':
            name=request.POST.get('txt_name')
            email=request.POST.get('txt_email')
            password=request.POST.get('txt_password')
            checkemail=tbl_admin.objects.filter(admin_email=email).count()
            checkuseremail=tbl_user.objects.filter(user_email=email).count()
            checkcompanyemail=tbl_company.objects.filter(company_email=email).count()
            checkserviceprovideremail=tbl_serviceprovider.objects.filter(serviceprovider_email=email).count()
            checkshopemail=tbl_shop.objects.filter(shop_email=email).count()
            checktechnicianemail=tbl_technician.objects.filter(technician_email=email).count()
            if checkemail > 0 :
                return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
            elif checkuseremail > 0 :
                return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
            elif checkcompanyemail > 0 :
                return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
            elif checkserviceprovideremail > 0 :
                return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
            elif checkshopemail > 0 :
                return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
            elif checktechnicianemail > 0 :
                return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
            else:
                tbl_admin.objects.create(admin_name=name,admin_email=email,admin_password=password)
                return render(request,"Admin/AdminRegistration.html",{'msg':"Registration completed successfully"})
        else:
            return render(request,'Admin/AdminRegistration.html',{'admin':admindata})
    


def deleteAdmin(request,did):
    tbl_admin.objects.get(id=did).delete()
    return render(request,"Admin/AdminRegistration.html",{'msg':"Data Deleted"})



def editAdmin(request, eid):
    editdata = tbl_admin.objects.get(id=eid)
    admindata = tbl_admin.objects.all()

    if request.method == 'POST':
        name = request.POST.get('txt_name')
        email = request.POST.get('txt_email')
        password = request.POST.get('txt_password')

        checkemail = tbl_admin.objects.filter(admin_email=email).exclude(id=eid).count()
        checkuseremail = tbl_user.objects.filter(user_email=email).count()
        checkcompanyemail = tbl_company.objects.filter(company_email=email).count()
        checkserviceprovideremail = tbl_serviceprovider.objects.filter(serviceprovider_email=email).count()
        checkshopemail = tbl_shop.objects.filter(shop_email=email).count()
        checktechnicianemail = tbl_technician.objects.filter(technician_email=email).count()

        if checkemail > 0:
            return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
        elif checkuseremail > 0:
            return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
        elif checkcompanyemail > 0:
            return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
        elif checkserviceprovideremail > 0:
            return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
        elif checkshopemail > 0:
            return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
        elif checktechnicianemail > 0:
            return render(request,"Admin/AdminRegistration.html",{'msg':"Email Already Exist"})
        else:
            editdata.admin_name = name
            editdata.admin_email = email
            editdata.admin_password = password
            editdata.save()
            return render(request,"Admin/AdminRegistration.html",{'msg':"Data Updated Successfully",'admindata':admindata})
    else:
        return render(request,"Admin/AdminRegistration.html",{'editdata':editdata,'admin':admindata})


    

def Category(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        categorydata=tbl_category.objects.all()
        if request.method=='POST':
            name=request.POST.get('txt_category')
            if tbl_category.objects.filter(category_name=name):
                return render(request,"Admin/Category.html",{'category':categorydata,'msg':"Category Already Exists"})
            else:
                tbl_category.objects.create(category_name=name)
                return render(request,"Admin/Category.html",{'category':categorydata,'msg':"Category Added Successfully"})
        else:
            return render(request,'Admin/Category.html',{'Category':categorydata})
    

    
def deleteCategory(request,did):
    tbl_category.objects.get(id=did).delete()
    return render(request,"Admin/Category.html",{'msg':"Data Deleted."})



def editCategory(request,eid):
    editdata=tbl_category.objects.get(id=eid)
    categorydata=tbl_category.objects.all()
    if request.method=='POST':
        category=request.POST.get('txt_category')
        editdata.category_name=category
        editdata.save()
        return render(request,"Admin/Category.html",{'msg':"Data Updated.."})
    else:
        return render(request,"Admin/Category.html",{'editdata':editdata,'Category':categorydata})

    

def Place(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        districtdata=tbl_district.objects.all().order_by('district_name')
        placedata=tbl_place.objects.all().order_by('place_name')
        if request.method=='POST':
            place=request.POST.get('txt_place')
            district=tbl_district.objects.get(id=request.POST.get('sel_district'))
            tbl_place.objects.create(place_name=place,district=district)
            return render(request,"Admin/Place.html",{'msg':"Place added Successfully"})
        else:
            return render(request,'Admin/Place.html',{'district':districtdata,'place':placedata})



def deletePlace(request,did):
    tbl_place.objects.get(id=did).delete()
    return render(request,"Admin/Place.html",{'msg':"Data Deleted."})




def editplace(request,eid):
    editdata=tbl_place.objects.get(id=eid)
    Palcedata=tbl_place.objects.all()
    district=tbl_district.objects.all()
    if request.method=='POST':
        place=request.POST.get('txt_place')
        district=tbl_district.objects.get(id=request.POST.get('sel_district'))
        editdata.place_name=place
        editdata.district=district
        editdata.save()
        return render(request,"Admin/Place.html",{'msg':"Data Updated.."})
    else:
        return render(request,"Admin/Place.html",{'editdata':editdata,'district':district,'place':Palcedata})



    
def SubCategory(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        categorydata=tbl_category.objects.all()
        subcategorydata=tbl_subcategory.objects.all()
        if request.method=='POST':
            subcategory=request.POST.get('txt_subcategory')
            category=tbl_category.objects.get(id=request.POST.get('sel_category'))
            tbl_subcategory.objects.create(subcategory_name=subcategory,category=category)
            return render(request,"Admin/SubCategory.html",{'msg':"Data Inserted"})
        else:
            return render(request,'Admin/SubCategory.html',{'category':categorydata,'subcategory':subcategorydata})
    


def deletesubcategory(request,did):
    tbl_subcategory.objects.get(id=did).delete()
    return render(request,"Admin/SubCategory.html",{'msg':"Data Deleted."})



def editsubcategory(request,eid):
    editdata=tbl_subcategory.objects.get(id=eid)
    SubCategorydata=tbl_subcategory.objects.all()
    category=tbl_category.objects.all()
    if request.method=='POST':
        Subcategory=request.POST.get('txt_subcategory')
        category=tbl_category.objects.get(id=request.POST.get('sel_category'))
        editdata.subcategory_name=Subcategory
        editdata.category=category
        editdata.save()
        return render(request,"Admin/SubCategory.html",{'msg':"Data Updated.."})
    else:
        return render(request,"Admin/SubCategory.html",{'editdata':editdata,'category':category,'subcategory':SubCategorydata})
    


def Brand(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        branddata=tbl_brand.objects.all()
        if request.method=='POST':
            brand=request.POST.get('txt_brand')

            if tbl_brand.objects.filter(brand_name=brand):
                return render(request, "Admin/Brand.html", {'msg': "Already Exists"})
            else:
                tbl_brand.objects.create(brand_name=brand)
                return render(request,"Admin/Brand.html",{'msg':"Brand Inserted"})
        else:
            return render(request,'Admin/Brand.html',{'Brand':branddata})
        
    

def deletebrand(request,did):
    tbl_brand.objects.get(id=did).delete()
    return render(request,"Admin/Brand.html",{'msg':"Data Deleted"})



def editbrand(request,eid):
    editdata=tbl_brand.objects.get(id=eid)
    branddata=tbl_brand.objects.all()
    if request.method == "POST":
        brand=request.POST.get('txt_brand')

        if tbl_brand.objects.filter(brand_name=brand):
            return render(request, "Admin/Brand.html", {'msg': "Already Exists"})
        else:
            editdata.brand_name = brand
            editdata.save()
            return render(request,"Admin/Brand.html",{'msg':"Brand Updated.."})
    else:
        return render(request,"Admin/Brand.html",{'editdata':editdata,'Brand':branddata})
    


def Experience(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        experiencedata = tbl_experience.objects.all()

        if request.method == 'POST':

            experience = request.POST.get('txt_experience')

            if tbl_experience.objects.filter(experience_range=experience):
                return render(request,"Admin/Experience.html",{'msg':"Already Exists"})
            else:
                tbl_experience.objects.create(experience_range=experience)
                return render(request,"Admin/Experience.html",{'msg':"Experience Inserted"})
        else:
            return render(request,"Admin/Experience.html",{'Experience':experiencedata})
        

def deleteexperience(request, id):
    tbl_experience.objects.get(id=id).delete()
    return redirect("Admin:Experience")

def Services(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        servicesdata = tbl_servicetype.objects.all()
        if request.method == 'POST':
            service = request.POST.get('txt_services')

            if tbl_servicetype.objects.filter(servicetype_name=service):
                return render(request, "Admin/Services.html", {'msg': "Already Exists"})
            else:
                tbl_servicetype.objects.create(servicetype_name=service)
                return render(request, "Admin/Services.html", {'msg': "Inserted"})
        else:
            return render(request, 'Admin/Services.html', {'Services': servicesdata})

    


def deleteservices(request,did):
    tbl_servicetype.objects.get(id=did).delete()
    return render(request,"Admin/Services.html",{'msg':"Data Deleted"})



def editservices(request,eid):
    editdata=tbl_servicetype.objects.get(id=eid)
    servicesdata=tbl_servicetype.objects.all()
    if request.method == "POST":
        service=request.POST.get('txt_services')

        if tbl_servicetype.objects.filter(servicetype_name=service):
            return render(request, "Admin/Services.html", {'msg': "Already Exists"})
       
        editdata.servicetype_name = service
        editdata.save()
        return render(request,"Admin/Services.html",{'msg':"Data Updated.."})
    else:
        return render(request,"Admin/Services.html",{'editdata':editdata,'Services':servicesdata})
    

    
def ViewCompany(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        companydata=tbl_company.objects.filter(company_status=0)
        companyacceptdata=tbl_company.objects.filter(company_status=1)
        companyrejectdata=tbl_company.objects.filter(company_status=2)
        branddata=tbl_brand.objects.all()
        return render(request, "Admin/ViewCompany.html",{'companydata':companydata,'branddata':branddata,'ac':companyacceptdata,'rj':companyrejectdata})



def CompanyAccept(request, aid):
    reqdata = tbl_company.objects.get(id=aid)
    reqdata.company_status = 1
    reqdata.save()

    
    subject = "Serviquo | Company Registration Approved"

    message = (
        f"Dear {reqdata.company_name},\n\n"
        
        f"We are pleased to inform you that your company registration request has "
        f"been successfully approved.\n\n"
        
        f"You can now log in to your Serviquo account and start using the platform "
        f"to manage your services and operations.\n\n"
        
        f"If you require any assistance, please feel free to contact our support team.\n\n"
        
        f"We look forward to working with you.\n\n"
        
        f"Best regards,\n\n"
        f"Serviquo Team"
    )

    send_mail(subject,message,settings.EMAIL_HOST_USER,[reqdata.company_email],fail_silently=False,)

    return render(request, "Admin/ViewCompany.html",{'msg': "Request Accepted and Email Sent"})


def CompanyReject(request, aid):
    reqdata = tbl_company.objects.get(id=aid)
    reqdata.company_status = 2
    reqdata.save()

    subject = "Serviquo | Company Registration Rejected"

    message = (
        f"Dear {reqdata.company_name},\n\n"
        
        f"We regret to inform you that your company registration request on Serviquo "
        f"has been rejected.\n\n"
        
        f"If you believe this decision was made in error or require further clarification, "
        f"please contact our support team for assistance.\n\n"
        
        f"We appreciate your interest in Serviquo and encourage you to reapply after "
        f"addressing any necessary requirements.\n\n"
        
        f"Thank you for your understanding.\n\n"
        
        f"Regards,\n\n"
        f"Serviquo Team"
    )

    send_mail(subject,message,settings.EMAIL_HOST_USER,[reqdata.company_email],fail_silently=False,)

    return render(request, "Admin/ViewCompany.html",{'msg': "Request Rejected and Email Sent"})



def ViewServiceProvider(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        serviceproviderdata=tbl_serviceprovider.objects.filter(serviceprovider_status=0)
        serviceprovideracceptdata=tbl_serviceprovider.objects.filter(serviceprovider_status=1)
        serviceproviderrejectdata=tbl_serviceprovider.objects.filter(serviceprovider_status=2)
        return render(request, "Admin/ViewServiceProvider.html",{'serviceproviderdata':serviceproviderdata,'ac':serviceprovideracceptdata,'rj':serviceproviderrejectdata})




def ServiceProviderAccept(request, aid):
    reqdata = tbl_serviceprovider.objects.get(id=aid)
    reqdata.serviceprovider_status = 1
    reqdata.save()

    subject = "Serviquo | Service Provider Registration Approved"

    message = (
        f"Dear {reqdata.serviceprovider_name},\n\n"
        
        f"We are pleased to inform you that your service provider registration "
        f"request has been successfully approved.\n\n"
        
        f"You can now log in to your Serviquo account and start offering your "
        f"services through our platform.\n\n"
        
        f"If you require any assistance, please feel free to contact our support team.\n\n"
        
        f"We look forward to working with you.\n\n"
        
        f"Best regards,\n\n"
        f"Serviquo Team"
    )

    send_mail(subject,message,settings.EMAIL_HOST_USER,[reqdata.serviceprovider_email],fail_silently=False,)

    return render(request, "Admin/ViewServiceProvider.html",
                  {'msg': "Request Accepted and Email Sent"})


def ServiceProviderReject(request, aid):
    reqdata = tbl_serviceprovider.objects.get(id=aid)
    reqdata.serviceprovider_status = 2
    reqdata.save()

    subject = "Serviquo | Service Provider Registration Update"

    message = (
        f"Dear {reqdata.serviceprovider_name},\n\n"
        
        f"We regret to inform you that your service provider registration request "
        f"has  been rejected at this time.\n\n"
        
        f"If you believe this decision was made in error or require further clarification, "
        f"please contact our support team for assistance.\n\n"
        
        f"We appreciate your interest in Serviquo and encourage you to reapply after "
        f"addressing any necessary requirements.\n\n"
        
        f"Thank you for your understanding.\n\n"
        
        f"Regards,\n\n"
        f"Serviquo Team"
    )

    send_mail(subject,message,settings.EMAIL_HOST_USER,[reqdata.serviceprovider_email],fail_silently=False,
              )
    return render(request, "Admin/ViewServiceProvider.html",{'msg': "Request Rejected and Email Sent"})


    

def ViewUser(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        active_users = tbl_user.objects.filter(user_status=0)
        suspended_users = tbl_user.objects.filter(user_status=1)
        return render(request,"Admin/UserList.html",{'active_users': active_users,'suspended_users': suspended_users})
    



def Banned(request, bid):
    userdata = tbl_user.objects.get(id=bid)
    userdata.user_status = 1
    userdata.save()

    subject = "Account Suspended"
    message = f"""
    Dear {userdata.user_name},

    Your account has been suspended by the administrator due to policy violations.

    If you believe this action was taken by mistake, please contact support.

    Thank You.
    """

    send_mail(subject,message,settings.EMAIL_HOST_USER,[userdata.user_email],fail_silently=False,)

    return render(request, "Admin/UserList.html", {'msg': "User Banned Successfully and Email Sent"})


def Unbanned(request, bid):
    userdata = tbl_user.objects.get(id=bid)
    userdata.user_status = 0
    userdata.save()

    subject = "Account Reactivated"
    message = f"""
    Dear {userdata.user_name},

    Your account has been successfully reactivated by the administrator.

    You can now login and continue using the system.

    Thank You.
    """

    send_mail(subject,message,settings.EMAIL_HOST_USER,[userdata.user_email],fail_silently=False,)

    return render(request, "Admin/UserList.html", {'msg': "User Unbanned Successfully and Email Sent"})



def ViewComplaint(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        user= tbl_user.objects.all()
        company= tbl_company.objects.all()
        technician= tbl_technician.objects.all()
        serviceprovider=tbl_serviceprovider.objects.all()
        shop= tbl_shop.objects.all()
        product = tbl_product.objects.all()
        complaintuserdata = tbl_complaint.objects.filter(user__in=user,servicerequest__isnull=True,companyservice__isnull=True,product__isnull=True).order_by('-id')
        complaintcompanydata = tbl_complaint.objects.filter(company__in=company,servicerequest__isnull=True,product__isnull=True).order_by('-id')
        complainttechniciandata = tbl_complaint.objects.filter(technician__in=technician,companyservice__isnull=True,servicerequest__isnull=True,product__isnull=True).order_by('-id')
        complaintserviceproviderdata = tbl_complaint.objects.filter(serviceprovider__in=serviceprovider,companyservice__isnull=True,product__isnull=True).order_by('-id')
        complaintshopdata = tbl_complaint.objects.filter(shop__in=shop,companyservice__isnull=True,servicerequest__isnull=True,product__isnull=True).order_by('-id')
        productdata = tbl_complaint.objects.filter(product__in=product,servicerequest__isnull=True,companyservice__isnull=True).order_by('-id')
        return render(request, "Admin/ViewComplaints.html",{'complaintuserdata':complaintuserdata,'complaintcompanydata':complaintcompanydata,
        'complainttechniciandata':complainttechniciandata,'complaintserviceproviderdata':complaintserviceproviderdata,'complaintshopdata':complaintshopdata,'productdata':productdata})



def ComplaintReply(request,id):
    replydata = tbl_complaint.objects.get(id=id)
    if request.method == 'POST':
        reply = request.POST.get('txt_reply')
        replydata.complaint_reply=reply
        replydata.complaint_status=1
        replydata.save()
        return render(request, "Admin/ViewComplaints.html", {'msg': "Replied"})
    else:
        return render(request, 'Admin/ComplaintReply.html', {'replydata': replydata})
    


def ViewFeedback(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        feedbackdata = tbl_feedback.objects.all().order_by('-id') 
        return render(request, "Admin/ViewFeedback.html", {"feedbackdata": feedbackdata})



def ViewShop(request):
    if "aid" not in  request.session :
        return redirect("Guest:Login")
    else:
        shopdata=tbl_shop.objects.filter(shop_status=0)
        shopacceptdata=tbl_shop.objects.filter(shop_status=1)
        shoprejectdata=tbl_shop.objects.filter(shop_status=2)
        return render(request, "Admin/ViewShop.html",{'shopdata':shopdata,'ac':shopacceptdata,'rj':shoprejectdata})



def ShopAccept(request, aid):
    reqdata = tbl_shop.objects.get(id=aid)
    reqdata.shop_status = 1
    reqdata.save()

    subject = "Serviquo | Shop Registration Approved"

    message = (
        f"Dear {reqdata.shop_name},\n\n"
        
        f"We are pleased to inform you that your shop registration request has been "
        f"successfully approved.\n\n"
        
        f"You can now log in to your Serviquo account and start using the platform "
        f"to manage your services efficiently.\n\n"
        
        f"If you have any questions or require assistance, please feel free to "
        f"contact our support team.\n\n"
        
        f"We look forward to working with you.\n\n"
        
        f"Best regards,\n\n\n"

        f"Serviquo Team"
    )

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [reqdata.shop_email],
        fail_silently=False,
    )

    return render(request, "Admin/ViewShop.html", {'msg': "Request Accepted and Email Sent"})


def ShopReject(request, aid):
    reqdata = tbl_shop.objects.get(id=aid)
    reqdata.shop_status = 2
    reqdata.save()

    subject = "Serviquo | Shop Registration Request Update"

    message = (
        f"Dear {reqdata.shop_name},\n\n"
        
        f"We regret to inform you that your shop registration request on Serviquo "
        f"has not been approved at this time.\n\n"
        
        f"If you believe this decision was made in error or require further clarification, "
        f"please contact our support team for assistance.\n\n"
        
        f"We appreciate your interest in Serviquo and encourage you to reapply after "
        f"addressing any necessary requirements.\n\n"
        
        f"Thank you for your understanding.\n\n"
        
        f"Regards,\n\n\n"
        f"Serviquo Team"
    )

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [reqdata.shop_email],
        fail_silently=False,
    )

    return render(request, "Admin/ViewShop.html", {'msg': "Request Rejected and Email Sent"})

    

def Logout(request):
      del request.session["aid"]
      return redirect('Guest:Index')





def admin_report(request):

    report_type = request.GET.get('type') or "all"
    from_date = request.GET.get('from_date', "")
    to_date = request.GET.get('to_date', "")
    search = request.GET.get('search', "")
    data = []
    total_count = 0
    total_amount = 0

    company_data = tbl_companyservice.objects.filter(companyservice_status=9).select_related('user','company').order_by('-id')
    booking_data = tbl_booking.objects.filter(booking_status__range=(2,6)).select_related('user').prefetch_related('tbl_cart_set__product__shop').order_by('-id')
    service_data = tbl_servicerequest.objects.filter(servicerequest_status=8).select_related('user','serviceprovider')

    if from_date and to_date:

        company_data = company_data.filter(companyservice_date__date__range=[from_date,to_date])
        booking_data = booking_data.filter(booking_date__range=[from_date,to_date])
        service_data = service_data.filter(servicerequest_date__date__range=[from_date,to_date])


    if search:

        company_data = (company_data.filter(user__user_name__icontains=search)| company_data.filter(company__company_name__icontains=search)).distinct()
        booking_data = (booking_data.filter(user__user_name__icontains=search)| booking_data.filter(tbl_cart_set__product__shop__shop_name__icontains=search)).distinct()
        service_data = (service_data.filter(user__user_name__icontains=search)| service_data.filter(serviceprovider__serviceprovider_name__icontains=search)).distinct()


    def get_date(obj):

        d = (getattr(obj, 'companyservice_date', None)or getattr(obj, 'booking_date', None)or getattr(obj, 'servicerequest_date', None))

        if d:
            return d.date() if hasattr(d, 'date') else d

        return None


    if report_type == "company":

        data = sorted(company_data, key=get_date, reverse=True)
        total_count = len(data)
        total_amount = company_data.aggregate( total=Sum('companyservice_amount'))['total'] or 0


    elif report_type == "booking":

        data = sorted(booking_data, key=get_date, reverse=True)
        total_count = len(data)
        total_amount = booking_data.aggregate(total=Sum('booking_amount') )['total'] or 0

    elif report_type == "service":

        data = sorted(service_data, key=get_date, reverse=True)
        total_count = len(data)
        total_amount = service_data.aggregate( total=Sum('servicerequest_amount'))['total'] or 0

    else:

        data = list(chain(company_data, booking_data, service_data))
        data = sorted(data, key=get_date, reverse=True)
        total_count = len(data)
        company_total = company_data.aggregate(total=Sum('companyservice_amount'))['total'] or 0
        booking_total = booking_data.aggregate(total=Sum('booking_amount'))['total'] or 0
        service_total = service_data.aggregate(total=Sum('servicerequest_amount') )['total'] or 0
        total_amount = company_total + booking_total + service_total

    context = {"data": data,"type": report_type,"search": search,"from_date": from_date,"to_date": to_date,"total_count": total_count,"total_amount": total_amount, }

    return render(request,"Admin/report.html",context)





