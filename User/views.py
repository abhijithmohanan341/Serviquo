from django.shortcuts import render,redirect
from User.models import *
from Guest.models import *
from Admin.models import *
from Company.models import *
from ServiceProvider.models import *
from Shop.models import *
from datetime import datetime
from django.db.models import Sum
from django.http import JsonResponse 
from django.utils import timezone

# Create your views here.

def homepage(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    else:
        userdata = tbl_user.objects.get(id=request.session['uid'])
        booking = tbl_booking.objects.filter(user=userdata,booking_status=0).first()
        
        if booking:
            cart_count = tbl_cart.objects.filter(booking=booking,cart_status=0).count()
        else:
            cart_count = 0
        return render(request,"User/HomePage.html",{'userdata': userdata,'cart_count': cart_count})



def myprofile(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        userdata=tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        return render(request,"User/MyProfile.html",{'userdata':userdata,'cart_count': cartcount})



def EditProfile(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        userdata=tbl_user.objects.get(id=request.session['uid'])
        Placedata=tbl_place.objects.get(id=userdata.place.id)
        Pla=tbl_place.objects.filter(district=Placedata.district)
        districtdata=tbl_district.objects.all().order_by('district_name')
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()

        if request.method=='POST':
            name=request.POST.get('txt_name')
            email=request.POST.get('txt_email')
            contact=request.POST.get('txt_contact')
            address=request.POST.get('txt_address')
            district = tbl_district.objects.get(id=request.POST.get('sel_district'))
            place = tbl_place.objects.get(id=request.POST.get('sel_place'))

            checkadmin = tbl_admin.objects.filter(admin_email=email).count()
            checkuser = tbl_user.objects.filter(user_email=email).exclude(id=request.session['uid']).count()
            checkcompany = tbl_company.objects.filter(company_email=email).count()
            checkserviceprovider = tbl_serviceprovider.objects.filter(serviceprovider_email=email).count()
            checkshop = tbl_shop.objects.filter(shop_email=email).count()
            checktechnician = tbl_technician.objects.filter(technician_email=email).count()

            if checkadmin > 0:
                return render(request,"User/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkuser > 0:
                return render(request,"User/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkcompany > 0:
                return render(request,"User/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkserviceprovider > 0:
                return render(request,"User/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkshop > 0:
                return render(request,"User/EditProfile.html",{'msg':"Email Already Exist"})
            elif checktechnician > 0:
                return render(request,"User/EditProfile.html",{'msg':"Email Already Exist"})
            else:
                userdata.user_name=name
                userdata.user_email=email
                userdata.user_contact=contact
                userdata.user_address=address
                userdata.district=district
                userdata.place=place
                userdata.save()
                return render(request,"User/EditProfile.html",{'msg':"Profile updated successfully",'userdata':userdata,'district':districtdata,'place':Pla,'cart_count': cartcount,})
        else:
            return render(request,"User/EditProfile.html",{'userdata':userdata,'district':districtdata,'place':Pla,'cart_count': cartcount})
        


def ChangePassword(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        userdata=tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        dbpassword = userdata.user_password
        if request.method=='POST':
            oldpassword=request.POST.get('txt_oldpassword')
            newpassword=request.POST.get('txt_newpassword')
            retypepassword=request.POST.get('txt_retypepassword')
            if dbpassword==oldpassword:
                if newpassword==retypepassword:
                    userdata.user_password=newpassword
                    userdata.save()
                    return render(request,"User/MyProfile.html",{'msg':"Password Changed..",'userdata':userdata,'cart_count': cartcount})
                else:
                    return render(request,"User/ChangePassword.html",{'msg':"Old password and  Retype Password Does not match..",'userdata': userdata,'cart_count': cartcount})
            else:
                return render(request,"User/ChangePassword.html",{'msg':"Current Password Not Match..",'userdata': userdata,'cart_count': cartcount})
        else:
            return render(request,"User/ChangePassword.html",{'userdata':userdata,'cart_count': cartcount})
    


def EditPhoto(request):
    editphoto = tbl_user.objects.get(id=request.session['uid'])
    userdata=tbl_user.objects.get(id=request.session['uid'])
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()

    if request.method == "POST":
        if request.FILES.get("file_photo"):
            editphoto.user_photo = request.FILES["file_photo"]
            editphoto.save()

        return render(request, "User/EditPhoto.html", {'msg': "Photo Updated Successfully",'editphoto': editphoto,'cart_count': cartcount})
    else:
        return render(request, "User/EditPhoto.html", {'userdata': editphoto,'cart_count': cartcount})
    


def ViewCompany(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        userdata=tbl_user.objects.get(id=request.session['uid'])
        companydata=tbl_company.objects.filter(company_status=1)
        branddata=tbl_brand.objects.all().order_by('brand_name')
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        return render(request, "User/ViewCompany.html",{'companydata':companydata,'branddata':branddata,'userdata':userdata,'cart_count': cartcount})


def ajaxCompanyBrand(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        bid = request.GET.get('bid')
        companydata = tbl_company.objects.filter(company_status=1)
        userdata=tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        if bid:
            companydata = companydata.filter(brand_id=bid)
        return render(request, 'User/AjaxCompany.html', {'companydata': companydata,'cart_count': cartcount})





def CompanyRequest(request,id):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        requestdata=tbl_companyservice.objects.all()
        company = tbl_company.objects.get(id=id)
        userdata = tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        if request.method=='POST':
            content=request.POST.get('txt_content')
            date = datetime.now()
            user= tbl_user.objects.get(id=request.session['uid'])
            company=tbl_company.objects.get(id=id)
            tbl_companyservice.objects.create(companyservice_content=content,companyservice_date=date,user=user,company=company)
            return render(request, "User/Request.html", {'msg': "Request Placed Successfully",'userdata': userdata,'cart_count': cartcount})
        else:
            return render(request,"User/Request.html",{'requestdata':requestdata,'company':company,'userdata': userdata,'cart_count': cartcount})
    


def CancelCompanyServiceRequest(request, cid):
    cancelcompanyrequest = tbl_companyservice.objects.get(id=cid)
    userdata = tbl_user.objects.get(id=request.session['uid'])

    if cancelcompanyrequest.companyservice_status == 0 or cancelcompanyrequest.companyservice_status == 1:
        cancelcompanyrequest.companyservice_status = 8
        cancelcompanyrequest.save()
        return render(request, "User/MyCompanyRequest.html", {'msg': "Request Cancelled..",'userdata': userdata})
    else:
        return render(request, "User/MyCompanyRequest.html", {'msg': "Request Cannot Be Cancelled",'userdata': userdata})



def MyCompanyRequest(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        userdata=tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        mycompanyrequestdata = tbl_companyservice.objects.filter(user=request.session['uid']).order_by('-companyservice_date', '-id')
        return render(request,"User/MyCompanyRequest.html",{'mycompanyrequestdata':mycompanyrequestdata,'userdata':userdata,'cart_count': cartcount})


def ViewServiceProvider(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        serviceproviderdata = tbl_serviceprovider.objects.filter(serviceprovider_status=1)
        districtdata=tbl_district.objects.all().order_by('district_name')
        placedata=tbl_place.objects.all().order_by('place_name')
        servicetype=tbl_servicetype.objects.all().order_by('servicetype_name')
        userdata = tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        for serviceprovide in serviceproviderdata:
            names = list(tbl_serviceproviderstype.objects.filter(serviceprovider=serviceprovide))
            serviceprovide.type_names = names
            return render(request, "User/ViewServiceProvider.html", {'serviceproviderdata': serviceproviderdata,'district':districtdata,'place':placedata,'servicetype':servicetype,'userdata': userdata,'cart_count': cartcount})



def ajaxService(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    else:
        pid = request.GET.get('pid')
        sid = request.GET.get('sid')

        serviceproviders = tbl_serviceprovider.objects.filter(serviceprovider_status=1)
        userdata=tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()

        if pid and pid != "":
            serviceproviders = serviceproviders.filter(place_id=pid)

        if sid and sid != "":
            serviceproviders = serviceproviders.filter(
                tbl_serviceproviderstype__servicetype_id=sid
            )

        serviceproviders = serviceproviders.distinct()

        return render(request, 'User/AjaxService.html', {'service': serviceproviders,'cart_count': cartcount})


def ServiceProviderRequest(request, id):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        requestdata = tbl_servicerequest.objects.all()
        serviceprovider = tbl_serviceprovider.objects.get(id=id)
        servicetypedata = tbl_serviceproviderstype.objects.filter(serviceprovider_id=id)
        userdata = tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        if request.method == 'POST':
            content = request.POST.get('txt_content')
            todate = request.POST.get('txt_date')
            servicetype = tbl_servicetype.objects.get(id=request.POST.get('sel_servicetype'))
            date = datetime.now()
            user = tbl_user.objects.get(id=request.session['uid'])
            serviceprovider = tbl_serviceprovider.objects.get(id=id)
            tbl_servicerequest.objects.create(servicerequest_content=content,servicerequest_date=date,servicerequest_todate=todate,user=user,serviceprovider=serviceprovider,servicetype=servicetype)
            return render(request, "User/ServiceProviderRequest.html", {'msg': "Request Placed Successfully",'userdata': userdata,'cart_count': cartcount})
        else:
            return render(request, "User/ServiceProviderRequest.html", {'requestdata': requestdata,'servicetypedata': servicetypedata,'serviceprovider': serviceprovider,'userdata': userdata,'cart_count': cartcount})
    

def CancelServiceRequest(request, did):
    req = tbl_servicerequest.objects.get(id=did)
    userdata = tbl_user.objects.get(id=request.session['uid'])
    
    if req.servicerequest_status == 0:
        req.servicerequest_status = 6       
        req.save()
        return render(request,"User/MyServiceRequest.html",{'msg':"Request Cancelled..",'userdata': userdata})
    else:
        return render(request, "User/MyServiceRequest.html", {'req':req,'userdata': userdata})


def MyServiceRequest(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        userdata = tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        myservicerequestdata = tbl_servicerequest.objects.filter(user=request.session['uid']).order_by('-servicerequest_date', '-id')
        return render(request,"User/MyServiceRequest.html",{'myservicerequestdata':myservicerequestdata,'userdata': userdata,'cart_count': cartcount})



def Complaint(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        complaintdata = tbl_complaint.objects.filter(user=request.session['uid']).order_by('-complaint_date','-id')
        userdata = tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        if request.method == 'POST':
            title = request.POST.get('txt_title')
            content = request.POST.get('txt_content')
            date = datetime.now()
            user = tbl_user.objects.get(id=request.session['uid'])
            tbl_complaint.objects.create(complaint_title=title,complaint_content=content,complaint_date=date,user=user)
            return render(request, "User/Complaint.html", {'msg': "Complaint Submitted Successfull",'userdata': userdata,'cart_count': cartcount})
        else:
            return render(request, "User/Complaint.html",{'complaintdata':complaintdata,'userdata': userdata,'cart_count': cartcount})
    


def DeleteComplaint(request,did):
    tbl_complaint.objects.get(id=did).delete()
    userdata = tbl_user.objects.get(id=request.session['uid'])
    return render(request,"User/Complaint.html",{'msg':"Complaint Deleted Successfull",'userdata': userdata})


def EditComplaint(request,eid):
    editdata=tbl_complaint.objects.get(id=eid)
    userdata = tbl_user.objects.get(id=request.session['uid'])
    complaintdata = tbl_complaint.objects.filter(user=request.session['uid']).order_by('-complaint_date','-id')
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
    if request.method=='POST':
        title = request.POST.get('txt_title')
        content = request.POST.get('txt_content')
        editdata.complaint_title=title
        editdata.complaint_content=content
        editdata.save()
        return render(request,"User/Complaint.html",{'msg':"Complaint Updated Successfull",'userdata': userdata,'cart_count': cartcount})
    else:
        return render(request,"User/Complaint.html",{'editdata':editdata,'complaintdata':complaintdata,'userdata':userdata,'cart_count': cartcount})

    


def Feedback(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        feedbackdata = tbl_feedback.objects.filter(user=request.session['uid'])
        userdata = tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        if request.method == 'POST':
            content = request.POST.get('txt_content')
            date = datetime.now()
            user = tbl_user.objects.get(id=request.session['uid'])
            tbl_feedback.objects.create(feedback_content=content,feedback_date=date,user=user)
            return render(request, "User/Feedback.html", {'msg': "Feedback Submitted",'userdata': userdata,'cart_count': cartcount})
        else:
            return render(request, "User/Feedback.html",{'feedbackdata':feedbackdata,'userdata': userdata,'cart_count': cartcount}) 
    



def DeleteFeedback(request,did):
    tbl_feedback.objects.get(id=did).delete()
    return render(request,"User/Feedback.html",{'msg':"Data Deleted"})


def EditFeedback(request,eid):
    editdata=tbl_feedback.objects.get(id=eid)
    feedbackdata = tbl_feedback.objects.filter(user=request.session['uid'])
    userdata = tbl_user.objects.get(id=request.session['uid'])
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
    if request.method=='POST':
        content = request.POST.get('txt_content')
        editdata.feedback_content=content
        editdata.save()
        return render(request,"User/Feedback.html",{'msg':"Data Updated.."})
    else:
        return render(request,"User/Feedback.html",{'editdata':editdata,'feedbackdata':feedbackdata,'userdata':userdata,'cart_count': cartcount})
    



def ServicePaymentComplete(request,aid):
    userdata = tbl_user.objects.get(id=request.session['uid'])
    reqdata=tbl_servicerequest.objects.get(id=aid)
    reqdata.servicerequest_status = 8
    reqdata.save()
    return render(request, "User/MyServiceRequest.html",{'msg': "Payment Completed",'userdata': userdata})


def CompanyPaymentComplete(request,aid):
    userdata = tbl_user.objects.get(id=request.session['uid'])
    reqdata=tbl_companyservice.objects.get(id=aid)
    reqdata.servicerequest_status = 9
    reqdata.save()
    return render(request, "User/MyCompanyRequest.html",{'msg': "Payment Completed",'userdata': userdata})


def ServiceProviderComplaint(request, sid):
    complaintdata = tbl_complaint.objects.filter(user=request.session['uid'],servicerequest=sid)
    userdata = tbl_user.objects.get(id=request.session['uid'])
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
    
    if request.method == 'POST':
        title = request.POST.get('txt_title')
        content = request.POST.get('txt_content')
        date = datetime.now()
        user = tbl_user.objects.get(id=request.session['uid'])
        servicerequest = tbl_servicerequest.objects.get(id=sid)
        tbl_complaint.objects.create(complaint_title=title,complaint_content=content,complaint_date=date,user=user,servicerequest=servicerequest)
        return render(request, "User/Complaint.html", {'msg': "Complaint Submitted",'userdata':userdata,'cart_count': cartcount})
    else:
        return render(request, "User/Complaint.html", {'complaintdata': complaintdata,'userdata':userdata,'cart_count': cartcount})



def CompanyComplaint(request, csid):
    complaintdata = tbl_complaint.objects.filter(user=request.session['uid'],companyservice=csid)
    userdata = tbl_user.objects.get(id=request.session['uid'])
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()

    if request.method == 'POST':
        title = request.POST.get('txt_title')
        content = request.POST.get('txt_content')
        date = datetime.now()
        user = tbl_user.objects.get(id=request.session['uid'])
        companyservice = tbl_companyservice.objects.get(id=csid)

        tbl_complaint.objects.create(complaint_title=title,complaint_content=content,complaint_date=date,user=user,companyservice=companyservice)

        return render(request,"User/Complaint.html",{'msg': "Complaint Submitted Successfull"})
    else:
        return render(request,"User/Complaint.html",{'complaintdata': complaintdata,'userdata':userdata,'cart_count': cartcount})

    

def TechnicianComplaint(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        complaintdata = tbl_complaint.objects.filter(user=request.session['uid'])
        if request.method == 'POST':
            title = request.POST.get('txt_title')
            content = request.POST.get('txt_content')
            date = datetime.now()
            user = tbl_user.objects.get(id=request.session['uid'])
            tbl_complaint.objects.create(complaint_title=title,complaint_content=content,complaint_date=date,user=user)
            return render(request, "User/Complaint.html", {'msg': "Complaint Submitted Successfull"})
        else:
            return render(request, "User/Complaint.html",{'complaintdata':complaintdata})
    


def ViewShop(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        shopdata=tbl_shop.objects.filter(shop_status=1) 
        userdata = tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        if request.method == 'POST':
            shop=request.POST.get("txt_shop")
            shopdata=tbl_shop.objects.filter(shop_name__icontains=shop,shop_status=1)
            return render(request, "User/ViewShop.html",{'shopdata':shopdata,'cart_count': cartcount})
        else:
            return render(request, "User/ViewShop.html",{'shopdata':shopdata,'userdata': userdata,'cart_count': cartcount})
            



def ViewProduct(request, shopid):
    ar=[1,2,3,4,5]
    shop=tbl_shop.objects.get(id=shopid)
    categorydata=tbl_category.objects.all().order_by('category_name')
    userdata=tbl_user.objects.get(id=request.session['uid'])
    cart_count=tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()

    productdata=tbl_product.objects.filter(shop=shop)

    products=[]
    ratings=[]
    stocks=[]
    solds=[]

    for p in productdata:
        ratecount=tbl_rating.objects.filter(product=p.id).count()
        if ratecount>0:
            ratedata=tbl_rating.objects.filter(product=p.id)
            tot=0
            for r in ratedata:
                tot+=r.rating_data
            avg=tot//ratecount
        else:
            avg=0
        ratings.append(avg)
        total_sold = tbl_cart.objects.filter(product=p.id,cart_status=1,booking__booking_status__in=[1,2,3,4,5]).aggregate(total=Sum('cart_Qty'))['total']

        if total_sold is None:
            total_sold = 0

        solds.append(total_sold)

        total_stock=tbl_stock.objects.filter(product=p.id).aggregate(total=Sum('stock_Qty'))['total']
        total_cart=tbl_cart.objects.filter(product=p.id,cart_status=1,booking__booking_status__in=[1,2,3,4,5]).aggregate(total=Sum('cart_Qty'))['total']

        if total_stock is None:
            total_stock=0
        if total_cart is None:
            total_cart=0

        available_stock=total_stock-total_cart
        if available_stock<0:
            available_stock=0

        stocks.append(available_stock)
        products.append(p)

    datas=zip(products,ratings,stocks,solds)

    if request.method=="POST":
        product=request.POST.get("txt_product")
        productdata=tbl_product.objects.filter(shop=shop)

        if product:
            productdata=productdata.filter(product_name__icontains=product)

        products=[]
        ratings=[]
        stocks=[]
        solds=[]

        return render(request,"User/ViewProduct.html",{'productdata':datas,'ar':ar,'shopid':shopid,'categorydata':categorydata,'userdata':userdata,'cart_count':cart_count})

    return render(request,"User/ViewProduct.html",{'productdata':datas,'ar':ar,'shopid':shopid,'categorydata':categorydata,'userdata':userdata,'cart_count':cart_count})




def ajaxProductCategory(request, shopid):

    cid = request.GET.get('cid')
    rating_filter = request.GET.get('rating')
    search = request.GET.get('search')

    shop = tbl_shop.objects.get(id=shopid)
    productdata = tbl_product.objects.filter(shop=shop)

    if cid and cid != "":
        productdata = productdata.filter(category_id=cid)

    if search and search != "":
        productdata = productdata.filter(product_name__icontains=search)

    final_data = []

    for p in productdata:

        ratecount = tbl_rating.objects.filter(product=p.id).count()

        if ratecount > 0:
            ratedata = tbl_rating.objects.filter(product=p.id)
            tot = 0
            for r in ratedata:
                tot += r.rating_data
            avg = tot // ratecount
        else:
            avg = 0

        total_sold = tbl_cart.objects.filter(product=p.id,cart_status=1,booking__booking_status__in=[1,2,3,4,5]).aggregate(total=Sum('cart_Qty'))['total']

        if total_sold is None:
            total_sold = 0

        total_stock = tbl_stock.objects.filter(product=p.id).aggregate(total=Sum('stock_Qty'))['total']
        total_cart = tbl_cart.objects.filter(product=p.id,cart_status=1,booking__booking_status__in=[1,2,3,4,5]).aggregate(total=Sum('cart_Qty'))['total']

        if total_stock is None:
            total_stock = 0
        if total_cart is None:
            total_cart = 0

        available_stock = total_stock - total_cart
        if available_stock < 0:
            available_stock = 0

        if rating_filter:
            if avg == int(rating_filter):
                final_data.append((p, avg, available_stock, total_sold))
        else:
            final_data.append((p, avg, available_stock, total_sold))

    return render(request, 'User/AjaxProduct.html', {'datas': final_data,'shopid': shopid,'ar': [1,2,3,4,5]})




    
def companypayment(request, id):
    cpay = tbl_companyservice.objects.get(id=id)
    userdata = tbl_user.objects.get(id=request.session['uid'])
    if request.method == "POST":
        cpay.companyservice_status = 9
        cpay.save()
        return redirect("User:loader")
    return render(request,"User/Payment.html",{"Amount":cpay.companyservice_amount,'userdata': userdata})



def servicepayment(request, id):
    userdata = tbl_user.objects.get(id=request.session['uid'])
    spay = tbl_servicerequest.objects.get(id=id)
    if request.method == "POST":
        spay.servicerequest_status = 8
        spay.save()
        return redirect("User:loader")
    return render(request,"User/Payment.html",{"Amount":spay.servicerequest_amount,'userdata': userdata})


def ShopPaymentComplete(request,aid):
    userdata = tbl_user.objects.get(id=request.session['uid'])
    reqdata=tbl_booking.objects.get(id=aid)
    reqdata.booking_status = 2
    reqdata.save()
    return render(request, "User/MyBooking.html",{'msg': "Payment Completed",'userdata': userdata})


def shoppayment(request, id):
    userdata = tbl_user.objects.get(id=request.session['uid'])
    spay = tbl_booking.objects.get(id=id)
    if request.method == "POST":
        spay.booking_status = 2
        spay.save()
        return redirect("User:loader")
    return render(request,"User/Payment.html",{"Amount":spay.booking_amount,'userdata': userdata})



def loader(request):
      return render(request,"User/Loader.html")


def paymentsuc(request):
    return render(request,"User/Paymentsuc.html")



def AddtoCart(request, pid, shopid):
    product = tbl_product.objects.get(id=pid)
    booking = tbl_booking.objects.filter(user=request.session['uid'],booking_status=0).first()
    userdata = tbl_user.objects.get(id=request.session['uid'])
    
    if booking is None:
        user = tbl_user.objects.get(id=request.session['uid'])
        booking = tbl_booking.objects.create(user=user, booking_status=0)
        tbl_cart.objects.create(booking=booking,product=product,cart_Qty=1)
        return render(request, "User/ViewProduct.html", {'msg': "Added to Cart",'shopid': shopid,'userdata': userdata})
    existing_cart = tbl_cart.objects.filter(booking=booking).first()

    if existing_cart and existing_cart.product.shop.id != product.shop.id:
        return render(request, "User/ViewProduct.html", {'msg': "Please complete previous shop booking",'shopid': shopid,'userdata': userdata})

    if tbl_cart.objects.filter(booking=booking, product=product).exists():
        return render(request, "User/ViewProduct.html", {'msg': "Already Added",'shopid': shopid,'userdata': userdata})

    tbl_cart.objects.create(booking=booking,product=product,cart_Qty=1)

    return render(request, "User/ViewProduct.html", {'msg': "Added to Cart",'shopid': shopid,'userdata': userdata})
    


def MyBooking(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        userdata = tbl_user.objects.get(id=request.session['uid'])
        bookingdata=tbl_booking.objects.filter(user=request.session['uid']).distinct().order_by('-id')
        cart_count = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        return render(request, "User/MyBooking.html",{'bookingdata':bookingdata,'userdata': userdata,'cart_count': cart_count})



def OrderCancel(request, bid):
    userdata = tbl_user.objects.get(id=request.session['uid'])
    canceldata = tbl_booking.objects.get(id=bid)
    canceldata.booking_status = 6
    canceldata.save()
    return render(request, "User/MyBooking.html", {'msg': "Order cancelled successfully. Any applicable refund will be processed within 5-7 working days.",'userdata': userdata})




def Mycart(request):
    if "uid" in request.session:

        userdata = tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
        
        if request.method=="POST":

            address = request.POST.get('txt_address')
            bookingdata=tbl_booking.objects.get(id=request.session["bookingid"])
            bookingid=bookingdata.id
            bookingdata.booking_date = datetime.now()
            bookingdata.booking_amount=request.POST.get("carttotalamt")
            bookingdata.booking_status=1
            bookingdata.booking_address=address
            bookingdata.save()
            cart = tbl_cart.objects.filter(booking=bookingdata)
            for i in cart:
                i.cart_status = 1
                i.save()
            return redirect("User:shoppayment",bookingid)
        else:
            bookcount = tbl_booking.objects.filter(user=request.session["uid"],booking_status=0).count()
            if bookcount > 0:
                book = tbl_booking.objects.get(user=request.session["uid"],booking_status=0)
                request.session["bookingid"] = book.id
                cart = tbl_cart.objects.filter(booking=book)
                for i in cart:
                    total_stock = tbl_stock.objects.filter(product=i.product.id).aggregate(total=Sum('stock_Qty'))['total']
                    total_cart = tbl_cart.objects.filter(product=i.product.id,cart_status=1,booking__booking_status__in=[1,2,3,4,5]).aggregate(total=Sum('cart_Qty'))['total']

                    if total_stock is None:
                        total_stock = 0
                    if total_cart is None:
                        total_cart = 0
                    total =  total_stock - total_cart
                    i.total_stock = total
                return render(request,"User/MyCart.html",{'cartdata':cart,'userdata': userdata,'cart_count': cartcount})
            else:
                return render(request,"User/MyCart.html",{'userdata': userdata,'cart_count': cartcount})
    else:
        return redirect("Guest:Login")
    

        

def DelCart(request,did):
   tbl_cart.objects.get(id=did).delete()
   return redirect("User:Mycart")



def CartQty(request):
    if "uid" not in  request.session :
        return redirect("Guest:Login")
    else:
        qty=request.GET.get('QTY')
        cartid=request.GET.get('ALT')
        cartdata=tbl_cart.objects.get(id=cartid)
        cartdata.cart_Qty=qty
        cartdata.save()
        return redirect("User:Mycart")  



def BuyNow(request, pid):

    if "uid" not in request.session:
        return redirect("Guest:LoginForm")

    product = tbl_product.objects.get(id=pid)
    user = tbl_user.objects.get(id=request.session['uid'])
    userdata = tbl_user.objects.get(id=request.session['uid'])
    cart_count = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
    total_stock = tbl_stock.objects.filter(product=product.id).aggregate(total=Sum('stock_Qty'))['total']
    total_cart = tbl_cart.objects.filter(product=product.id,cart_status=1,booking__booking_status__in=[1,2,3,4,5]).aggregate(total=Sum('cart_Qty'))['total']

    if total_stock is None:
        total_stock = 0
    if total_cart is None:
        total_cart = 0

    available_stock = total_stock - total_cart
    
    if available_stock < 0:
        available_stock = 0

    if request.method == "POST":
        
        if available_stock == 0:
            return render(request, "User/Booking.html", {"product": product,"available_stock": available_stock,"msg": "Out of Stock"})
        qty = int(request.POST.get("final_qty"))
        address = request.POST.get("txt_address")
        total_amount = request.POST.get("total_amount")
        
        if qty > available_stock:
            qty = available_stock
        booking = tbl_booking.objects.create(user=user,booking_status=1,booking_address=address,booking_amount=total_amount,booking_date=datetime.now())
        tbl_cart.objects.create(booking=booking,product=product,cart_Qty=qty,cart_status=1)
        return redirect("User:shoppayment", booking.id)
    else:
        return render(request, "User/Booking.html", {"product": product,"available_stock": available_stock,'userdata': userdata,'cart_count': cart_count})
    



def ProductComplaint(request, pid, cid):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    else:
        user = tbl_user.objects.get(id=request.session['uid'])
        product = tbl_product.objects.get(id=pid)
        cart = tbl_cart.objects.get(id=cid)
        complaintdata = tbl_complaint.objects.filter(user=user,product=product).order_by('-complaint_date', '-id')
        cartcount = tbl_cart.objects.filter(booking__user=user,booking__booking_status=0).count()
        

        if request.method == "POST":
            title = request.POST.get("txt_title")
            content = request.POST.get("txt_content")
            date = datetime.now()
            tbl_complaint.objects.create(complaint_title=title,complaint_content=content,complaint_date=date,user=user,product=product,shop=product.shop,cart=cart)
            return render(request,"User/ProductComplaint.html",{"msg": "Complaint Submitted Successfully","product": product,"cart": cart,"complaintdata": complaintdata,'cart_count': cartcount})
        else:
            return render(request,"User/ProductComplaint.html",{"product": product,"cart": cart,"complaintdata": complaintdata,'userdata':user,'cart_count': cartcount})




def EditProductComplaint(request, cid):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    else:
        user = tbl_user.objects.get(id=request.session['uid'])
        editdata = tbl_complaint.objects.get(id=cid, user=user)
        product = editdata.product
        cart = editdata.cart

        complaintdata = tbl_complaint.objects.filter(user=user,product=product).order_by('-complaint_date', '-id')
        cartcount = tbl_cart.objects.filter(booking__user=user,booking__booking_status=0).count()

        if request.method == "POST":
            editdata.complaint_title = request.POST.get("txt_title")
            editdata.complaint_content = request.POST.get("txt_content")
            editdata.save()
            return render(request,"User/ProductComplaint.html",{"msg": "Complaint Updated Successfully","product": product,"cart": cart,"complaintdata": complaintdata,'cart_count': cartcount})
        else:
            return render(request, "User/ProductComplaint.html",{"editdata": editdata,"product": product,"cart": cart,"complaintdata": complaintdata,'cart_count': cartcount})




def DeleteProductComplaint(request, did):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    else:
        user = tbl_user.objects.get(id=request.session['uid'])
        complaint = tbl_complaint.objects.get(id=did, user=user)
        product = complaint.product
        cart = complaint.cart
        complaint.delete()
        complaintdata = tbl_complaint.objects.filter(user=user,product=product).order_by('-complaint_date', '-id')
        return render(request,"User/ProductComplaint.html",{"msg": "Complaint Deleted Successfully","product": product,"cart": cart,"complaintdata": complaintdata})



def Logout(request):
      del request.session["uid"]
      return redirect('Guest:Index')





def ReServiceRequest(request, rid):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    else:
        old = tbl_servicerequest.objects.get(id=rid)
        servicetypedata = tbl_serviceproviderstype.objects.filter(serviceprovider=old.serviceprovider)
        userdata = tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()

        if request.method == 'POST':
            servicetype = tbl_servicetype.objects.get(id=request.POST.get('sel_servicetype'))
            content = request.POST.get('txt_content')
            todate = request.POST.get('txt_todate')
            date = datetime.now()

            user = tbl_user.objects.get(id=request.session['uid'])
            serviceprovider = old.serviceprovider

            tbl_servicerequest.objects.create(servicerequest_content=content,servicerequest_date=date,servicerequest_todate=todate,user=user,serviceprovider=serviceprovider,servicetype=servicetype)

            return render(request, "User/MyServiceRequest.html",{'msg': "Service Re-Requested Successfully", 'userdata': userdata,'cart_count': cartcount})
        else:
            return render(request, "User/ReServiceRequest.html",{'old': old, 'servicetypedata': servicetypedata, 'userdata': userdata,'cart_count': cartcount})




def ReCompanyServiceRequest(request, rid):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    else:
        old = tbl_companyservice.objects.get(id=rid)
        userdata = tbl_user.objects.get(id=request.session['uid'])
        cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()

        if request.method == 'POST':
            content = request.POST.get('txt_content')
            date = datetime.now()

            user = tbl_user.objects.get(id=request.session['uid'])
            company = old.company

            tbl_companyservice.objects.create(companyservice_content=content,companyservice_date=date,user=user,company=company)

            return render(request, "User/MyCompanyRequest.html",{'msg': "Service Re-Requested Successfully", 'userdata': userdata,'cart_count': cartcount})
        else:
            return render(request, "User/ReCompanyRequest.html",{'old': old, 'userdata': userdata,'cart_count': cartcount})



def productrating(request,mid):
    user=tbl_user.objects.get(id=request.session['uid'])
    parray=[1,2,3,4,5]
    mid=mid
    
    counts=0
    counts=stardata=tbl_rating.objects.filter(product=mid,user=user).count()
    userdata = tbl_user.objects.get(id=request.session['uid'])
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(product=mid).order_by('-datetime')
        total_count = stardata.count()
        for i in stardata:
            res = res + i.rating_data
        avg = res // total_count
        return render(request,"User/ProductRating.html",{'msg': "Review Submitted",'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':total_count,'userdata': user,'cart_count': cartcount})
    else: 
         return render(request,"User/ProductRating.html",{'mid':mid,'userdata': userdata,'cart_count': cartcount})




def ajaxstar(request):
    rating_data = request.GET.get('rating_data')
    user_review = request.GET.get('user_review')
    pid = request.GET.get('pid')

    tbl_rating.objects.create(
        user = tbl_user.objects.get(id=request.session['uid']),
        user_review = user_review,
        rating_data = rating_data,
        product = tbl_product.objects.get(id=pid)
    )

    return JsonResponse({"status": "success"})





def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    rate = tbl_rating.objects.filter(product=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(product=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
       
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)



def companyrating(request,mid):
    parray=[1,2,3,4,5]
    mid=mid
    
    counts=0
    counts=stardata=tbl_rating.objects.filter(companyservice=mid).count()
    userdata = tbl_user.objects.get(id=request.session['uid'])
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(companyservice=mid).order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        return render(request,"User/CompanyRating.html",{'msg': "Review Submitted",'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts,'userdata': userdata,'cart_count': cartcount})
    else:
         return render(request,"User/CompanyRating.html",{'mid':mid,'userdata': userdata,'cart_count': cartcount})



def companyajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    
    user_review=request.GET.get('user_review')
    cid=request.GET.get('cid')

    if tbl_rating.objects.filter(user=request.session['uid'],companyservice=cid):
        return JsonResponse({"status": "rated"})
    
    tbl_rating.objects.create(user=tbl_user.objects.get(id=request.session['uid']),user_review=user_review,rating_data=rating_data,companyservice=tbl_companyservice.objects.get(id=cid))
    stardata=tbl_rating.objects.filter(companyservice=cid).order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})



def companystarrating(request):
    r_len = 0
    five = four = three = two = one = 0
    rate = tbl_rating.objects.filter(companyservice=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(companyservice=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
       
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)



def servicerating(request,mid):
    parray=[1,2,3,4,5]
    mid=mid
    
    counts=0
    counts=stardata=tbl_rating.objects.filter(servicerequest=mid).count()
    userdata = tbl_user.objects.get(id=request.session['uid'])
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(servicerequest=mid).order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        return render(request,"User/ServiceRating.html",{'msg': "Review Submitted",'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts,'userdata': userdata,'cart_count': cartcount})
    else:
         return render(request,"User/ServiceRating.html",{'mid':mid,'userdata': userdata,'cart_count': cartcount})



def serviceajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    
    
    user_review=request.GET.get('user_review')
    sid=request.GET.get('sid')

    if tbl_rating.objects.filter(user=request.session['uid'],servicerequest=sid):
        return JsonResponse({"status": "rated"})
    
    tbl_rating.objects.create(user=tbl_user.objects.get(id=request.session['uid']),user_review=user_review,rating_data=rating_data,servicerequest=tbl_servicerequest.objects.get(id=sid))
    stardata=tbl_rating.objects.filter(servicerequest=sid).order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})



def servicestarrating(request):
    r_len = 0
    five = four = three = two = one = 0
    rate = tbl_rating.objects.filter(servicerequest=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(servicerequest=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
       
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)


def UserBill(request, bid):
    booking = tbl_booking.objects.get(id=bid)
    cartdata = tbl_cart.objects.filter(booking=booking)
    userdata = tbl_user.objects.get(id=request.session['uid'])
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()

    total = 0

    for item in cartdata:
        item.subtotal = float(item.product.product_price) * item.cart_Qty
        total += item.subtotal

    return render(request, "User/ShopBill.html", {'booking': booking,'cartdata': cartdata,'userdata': userdata,'total': total,'cart_count': cartcount})


def ServiceBill(request, rid):
    requestdata = tbl_servicerequest.objects.get(id=rid)
    userdata = tbl_user.objects.get(id=request.session['uid'])
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
    providerdata = requestdata.serviceprovider

    return render(request, "User/ServiceBill.html", {'requestdata': requestdata,'userdata': userdata,'providerdata': providerdata,'cart_count': cartcount})


def CompanyServiceBill(request, cid):
    servicedata = tbl_companyservice.objects.get(id=cid)
    userdata = tbl_user.objects.get(id=request.session['uid'])
    cartcount = tbl_cart.objects.filter(booking__user=userdata,booking__booking_status=0).count()
    companydata = servicedata.company
    techniciandata = servicedata.technician

    return render(request, "User/CompanyServiceBill.html", {'servicedata': servicedata,'userdata': userdata,'companydata': companydata,'techniciandata': techniciandata,'cart_count': cartcount})