from django.shortcuts import render,redirect
from User.models import *
from Company.models import *
from Guest.models import *
from Shop.models import *
from datetime import datetime
from django.db.models import Sum
from django.db.models import Sum, F, ExpressionWrapper, FloatField



def homepage(request):
    if "shopid" not in  request.session :
        return redirect("Guest:Login")
    else:
        shopdata = tbl_shop.objects.get(id=request.session['shopid'])
        return render(request,"Shop/HomePage.html",{'shopdata':shopdata})
    

def ShopProfile(request):
    if "shopid" not in  request.session :
        return redirect("Guest:Login")
    else:
        shopdata=tbl_shop.objects.get(id=request.session['shopid'])
        return render(request,"Shop/MyProfile.html",{'shopdata':shopdata})



def EditProfile(request):
    if "shopid" not in  request.session :
        return redirect("Guest:Login")
    else:
        shopdata=tbl_shop.objects.get(id=request.session['shopid'])
        Placedata=tbl_place.objects.get(id=shopdata.place.id)
        Pla=tbl_place.objects.filter(district=Placedata.district)
        districtdata=tbl_district.objects.all().order_by('district_name')

        if request.method=='POST':
            name=request.POST.get('txt_name')
            email=request.POST.get('txt_email')
            contact=request.POST.get('txt_contact')
            address=request.POST.get('txt_address')
            district = tbl_district.objects.get(id=request.POST.get('sel_district'))
            place = tbl_place.objects.get(id=request.POST.get('sel_place'))

            checkadmin = tbl_admin.objects.filter(admin_email=email).count()
            checkuser = tbl_user.objects.filter(user_email=email).count()
            checkcompany = tbl_company.objects.filter(company_email=email).count()
            checkserviceprovider = tbl_serviceprovider.objects.filter(serviceprovider_email=email).count()
            checkshop = tbl_shop.objects.filter(shop_email=email).exclude(id=request.session['shopid']).count()
            checktechnician = tbl_technician.objects.filter(technician_email=email).count()

            if checkadmin > 0:
                return render(request,"Shop/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkuser > 0:
                return render(request,"Shop/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkcompany > 0:
                return render(request,"Shop/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkserviceprovider > 0:
                return render(request,"Shop/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkshop > 0:
                return render(request,"Shop/EditProfile.html",{'msg':"Email Already Exist"})
            elif checktechnician > 0:
                return render(request,"Shop/EditProfile.html",{'msg':"Email Already Exist"})
            else:
                shopdata.shop_name=name
                shopdata.shop_email=email
                shopdata.shop_contact=contact
                shopdata.shop_address=address
                shopdata.district=district
                shopdata.place=place
                shopdata.save()
                return render(request,"Shop/EditProfile.html",{'msg':"Profile updated successfully",'shopdata':shopdata,'district':districtdata,'place':Pla})
        else:
            return render(request,"Shop/EditProfile.html",{'shopdata':shopdata,'district':districtdata,'place':Pla})
        


def ChangePassword(request):
    if "shopid" not in  request.session :
        return redirect("Guest:Login")
    else:
        shopdata=tbl_shop.objects.get(id=request.session['shopid'])
        dbpassword = shopdata.shop_password
        if request.method=='POST':
            oldpassword=request.POST.get('txt_oldpassword')
            newpassword=request.POST.get('txt_newpassword')
            retypepassword=request.POST.get('txt_retypepassword')
            if dbpassword==oldpassword:
                if newpassword==retypepassword:
                    shopdata.shop_password=newpassword
                    shopdata.save()
                    return render(request,"Shop/ChangePassword.html",{'msg':"Password Changed..",'shopdata':shopdata})
                else:
                    return render(request,"Shop/ChangePassword.html",{'msg':"New password and  Retype Password Does not match..",'shopdata':shopdata})
            else:
                return render(request,"Shop/ChangePassword.html",{'msg':"Current Password Not Match..",'shopdata':shopdata})
        else:
            return render(request,"Shop/ChangePassword.html",{'shopdata':shopdata})
    




def EditPhoto(request):

    shopdata = tbl_shop.objects.get(id=request.session['shopid'])

    if request.method == "POST":
        if request.FILES.get("file_logo"):
            shopdata.shop_photo = request.FILES["file_logo"]
            shopdata.save()

        return render(request, "Shop/EditPhoto.html", {'msg': "Photo Updated Successfully",'shopdata': shopdata})
    else:
        return render(request, "Shop/EditPhoto.html", {'shopdata': shopdata})    
    



def AddProduct(request):
    if "shopid" not in  request.session :
        return redirect("Guest:Login")
    else:
        shop = tbl_shop.objects.get(id=request.session['shopid'])
        productdata = tbl_product.objects.filter(shop=shop)
        shopdata = tbl_shop.objects.get(id=request.session['shopid'])
        categorydata = tbl_category.objects.all()
        if request.method=='POST':
            name=request.POST.get('txt_name')
            details=request.POST.get('txt_details')
            photo=request.FILES.get('file_photo')
            price=request.POST.get('txt_price')
            category=tbl_category.objects.get(id=request.POST.get('sel_category'))
            shop=tbl_shop.objects.get(id=request.session['shopid'])
            if tbl_product.objects.filter(product_name=name):
                return render(request,"Shop/Product.html",{'productdata':productdata,'shopdata':shopdata,'msg':"Product Already Exists"})
            else:
                tbl_product.objects.create(product_name=name,product_details=details,product_photo=photo,product_price=price,category=category,shop=shop)
                return render(request,"Shop/Product.html",{'productdata':productdata,'shopdata':shopdata,'msg':"Product Added Successfully"})
        else:
            return render(request,'Shop/Product.html',{'shopdata':shopdata,'productdata':productdata,'category':categorydata})
        


def deleteProduct(request,did):
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    tbl_product.objects.get(id=did).delete()
    return render(request,"Shop/Product.html",{'msg':"Product Deleted.",'shopdata':shopdata})



def AddStock(request,aid):
    productdata=tbl_product.objects.all()
    stockdata=tbl_stock.objects.filter(product=aid)
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    for i in stockdata:
        total_stock = tbl_stock.objects.filter(product=i.product.id).aggregate(total=Sum('stock_Qty'))['total']
        total_cart = tbl_cart.objects.filter(product=i.product.id,cart_status=1,booking__booking_status__in=[1,2,3,4,5]).aggregate(total=Sum('cart_Qty'))['total']
        if total_stock is None:
            total_stock = 0
        if total_cart is None:
            total_cart = 0
        total = total_stock - total_cart
        i.total_stock = total
    if request.method=='POST':
        Qty=request.POST.get('txt_qty')
        date = datetime.now()
        product=tbl_product.objects.get(id=aid)
        tbl_stock.objects.create(stock_Qty=Qty,stock_date=date,product=product)
        return render(request,"Shop/Stock.html",{'msg':"Stock Added",'aid':aid,'shopdata':shopdata})
    else:
        return render(request,'Shop/Stock.html',{'productdata':productdata,'stockdata':stockdata,'aid':aid,'shopdata':shopdata})
    


def deleteStock(request,did,aid):
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    tbl_stock.objects.get(id=did).delete()
    return render(request,"Shop/Stock.html",{'msg':"Product Deleted",'aid':aid,'shopdata':shopdata})



def Complaint(request):
    if "shopid" not in  request.session :
        return redirect("Guest:Login")
    else:
        shop = tbl_shop.objects.get(id=request.session['shopid'])
        complaintdata = tbl_complaint.objects.filter(shop=shop,user__isnull=True,product__isnull=True)
        shopdata = tbl_shop.objects.get(id=request.session['shopid'])

        if request.method == 'POST':
            title = request.POST.get('txt_title')
            content = request.POST.get('txt_content')
            date = datetime.now()
            tbl_complaint.objects.create(complaint_title=title,complaint_content=content,complaint_date=date,shop=shop)
            return render(request,"Shop/Complaint.html",{'msg': "Complaint Submitted",'complaintdata': complaintdata,'shopdata':shopdata})
        else:
            return render(request,"Shop/Complaint.html",{'complaintdata': complaintdata,'shopdata':shopdata})
        


def DeleteComplaint(request,did):
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    tbl_complaint.objects.get(id=did).delete()
    return render(request,"Shop/Complaint.html",{'msg':"Data Deleted",'shopdata':shopdata})



def EditComplaint(request,eid):
    editdata=tbl_complaint.objects.get(id=eid)
    complaintdata=tbl_complaint.objects.filter(shop=request.session['shopid'])
    userdata=tbl_user.objects.get(id=request.session['uid'])
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    if request.method=='POST':
        title = request.POST.get('txt_title')
        content = request.POST.get('txt_content')
        editdata.complaint_title=title
        editdata.complaint_content=content
        editdata.save()
        return render(request,"Shop/Complaint.html",{'msg':"Complaint Updated Successfully.",'shopdata':shopdata})
    else:
        return render(request,"Shop/Complaint.html",{'editdata':editdata,'complaintdata':complaintdata,'shopdata':shopdata,'userdata':userdata})



def ViewBooking(request):
    if "shopid" not in  request.session :
        return redirect("Guest:Login")
    else:
        shopdata = tbl_shop.objects.get(id=request.session['shopid'])
        bookingdata = tbl_booking.objects.filter(tbl_cart__product__shop=tbl_shop.objects.get(id=request.session['shopid'])).distinct().order_by( '-id')
        return render(request, "Shop/ViewBooking.html", {'bookingdata': bookingdata,'shopdata':shopdata})


def OrderPacked(request, bid):
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    packdata = tbl_booking.objects.get(id=bid)
    packdata.booking_status = 3
    packdata.save()
    bookingdata = tbl_booking.objects.exclude(booking_amount=None)
    return render(request, "Shop/ViewBooking.html", {'bookingdata': bookingdata,'msg': "Order Packed",'shopdata':shopdata})


def OrderShipped(request, bid):
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    shipdata = tbl_booking.objects.get(id=bid)
    shipdata.booking_status = 4
    shipdata.save()
    bookingdata = tbl_booking.objects.exclude(booking_amount=None)
    return render(request, "Shop/ViewBooking.html", {'bookingdata': bookingdata,'shopdata':shopdata,'msg': "Order Shipped"})



def OrderDelivered(request, bid):
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    deldata = tbl_booking.objects.get(id=bid)
    deldata.booking_status = 5
    deldata.save()
    bookingdata = tbl_booking.objects.exclude(booking_amount=None)
    return render(request, "Shop/ViewBooking.html", {'bookingdata': bookingdata,'shopdata':shopdata,'msg': "Order Delivered"})



def ViewProductComplaint(request, pid):
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    complaintproductdata = tbl_complaint.objects.filter(product_id=pid,product__shop=request.session['shopid']).order_by('-id')
    return render(request,"Shop/ViewProductComplaint.html",{'complaintproductdata': complaintproductdata,'shopdata':shopdata})



def ComplaintReply(request, id):
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    replydata = tbl_complaint.objects.get(id=id)
    pid = replydata.product.id
    if request.method == 'POST':
        replydata.complaint_reply = request.POST.get('txt_reply')
        replydata.complaint_status = 1
        replydata.save()
        return render(request,"Shop/ViewProductComplaint.html",{'msg': "Reply submitted successfully",'pid': pid,'shopdata':shopdata})
    else:
        return render(request, 'Shop/Reply.html', {'replydata': replydata,'shopdata':shopdata})
    


def Logout(request):
      del request.session["shopid"]
      return redirect('Guest:Index')
    


def ViewProductRating(request,pid):
    ratingdata=tbl_rating.objects.filter(product=pid).order_by('-datetime','id')
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])
    count=ratingdata.count()
    avg=0
    if count>0:
        total=0
        for i in ratingdata:
            total+=i.rating_data
        avg=total//count
    return render(request,"Shop/ViewProductRating.html",{'ratingdata':ratingdata,'avg':avg,'count':count,'pid':pid,'shopdata':shopdata})






def shop_revenue_report(request):

    if "shopid" not in request.session:
        return redirect("Guest:Login")

    shop_id = request.session["shopid"]

    user_name = request.GET.get("user_name","")
    from_date = request.GET.get("from_date","")
    to_date = request.GET.get("to_date","")
    product_id = request.GET.get("product","")



    products = tbl_product.objects.filter(shop_id=shop_id).order_by("product_name")
    bookings = tbl_booking.objects.filter(tbl_cart__product__shop_id=shop_id,booking_status__range=(2,5)).distinct().order_by("-booking_date","-id")
    shopdata = tbl_shop.objects.get(id=request.session['shopid'])


    if user_name:
        bookings = bookings.filter(user__user_name__icontains=user_name)


    if from_date and to_date:
        bookings = bookings.filter(booking_date__range=[from_date,to_date])


    if product_id:
        bookings = bookings.filter(tbl_cart__product_id=product_id)


    report = []
    total_revenue = 0

    for booking in bookings:

        carts = tbl_cart.objects.filter(booking=booking,product__shop_id=shop_id).select_related("product")


        if product_id:
            carts = carts.filter(product_id=product_id)


        product_list = []
        booking_total = 0


        for cart in carts:

            price = float(cart.product.product_price)
            qty = int(cart.cart_Qty)

            total = price * qty

            booking_total += total

            product_list.append({"name": cart.product.product_name,"image": cart.product.product_photo.url,"price": price,"qty": qty,"total": total,})


        if product_list:

            total_revenue += booking_total

            report.append({"booking_id": booking.id,"user": booking.user,"booking_date": booking.booking_date,"products": product_list,"booking_total": booking_total})



    context = {"report": report,"total_requests": len(report),"total_revenue": total_revenue,"products": products,"user_name": user_name,"from_date": from_date,"to_date": to_date,"selected_product": product_id,'shopdata':shopdata}

    return render(request,"Shop/Report.html",context)