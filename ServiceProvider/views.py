from django.shortcuts import render,redirect
from User.models import *
from Guest.models import *
from ServiceProvider.models import *
from Admin.models import *
from datetime import datetime
from django.db.models import Sum



def homepage(request):
    if "sid" not in  request.session :
        return redirect("Guest:Login")
    else:
        serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
        return render(request,"ServiceProvider/HomePage.html",{'serviceproviderdata':serviceproviderdata})


def ServiceProviderProfile(request):
    if "sid" not in  request.session :
        return redirect("Guest:Login")
    else:
        serviceproviderdata=tbl_serviceprovider.objects.get(id=request.session['sid'])
        return render(request,"Serviceprovider/ServiceProviderProfile.html",{'serviceproviderdata':serviceproviderdata})


def EditProfile(request):
    if "sid" not in  request.session :
        return redirect("Guest:Login")
    else:
        serviceproviderdata=tbl_serviceprovider.objects.get(id=request.session['sid'])
        Placedata = tbl_place.objects.get(id=serviceproviderdata.place.id)
        Pla = tbl_place.objects.filter(district=Placedata.district)
        districtdata = tbl_district.objects.all().order_by('district_name')
        experiencedata = tbl_experience.objects.all()

        if request.method == 'POST':
            name = request.POST.get('txt_name')
            email = request.POST.get('txt_email')
            contact = request.POST.get('txt_contact')
            address = request.POST.get('txt_address')
            district = tbl_district.objects.get(id=request.POST.get('sel_district'))
            place = tbl_place.objects.get(id=request.POST.get('sel_place'))
            experience = tbl_experience.objects.get(id=request.POST.get('sel_experience'))
            
            checkadmin = tbl_admin.objects.filter(admin_email=email).count()
            checkuser = tbl_user.objects.filter(user_email=email).count()
            checkcompany = tbl_company.objects.filter(company_email=email).count()
            checkserviceprovider = tbl_serviceprovider.objects.filter(serviceprovider_email=email).exclude(id=request.session['sid']).count()
            checkshop = tbl_shop.objects.filter(shop_email=email).count()
            checktechnician = tbl_technician.objects.filter(technician_email=email).count()

            if checkadmin > 0:
                return render(request,"ServiceProvider/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkuser > 0:
                return render(request,"ServiceProvider/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkcompany > 0:
                return render(request,"ServiceProvider/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkserviceprovider > 0:
                return render(request,"ServiceProvider/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkshop > 0:
                return render(request,"ServiceProvider/EditProfile.html",{'msg':"Email Already Exist"})
            elif checktechnician > 0:
                return render(request,"ServiceProvider/EditProfile.html",{'msg':"Email Already Exist"})
            else:
                serviceproviderdata.serviceprovider_name = name
                serviceproviderdata.serviceprovider_email = email
                serviceproviderdata.serviceprovider_contact = contact
                serviceproviderdata.serviceprovider_address = address
                serviceproviderdata.place = place
                serviceproviderdata.experience = experience
                serviceproviderdata.save()
                return render(request, "Serviceprovider/EditProfile.html", {'msg':"Profile updated successfully",'serviceproviderdata':serviceproviderdata,'district':districtdata,'place':Pla,'experience': experiencedata})
        else:
            return render(request, "Serviceprovider/EditProfile.html",{'serviceproviderdata': serviceproviderdata,'district': districtdata,'place': Pla,'experience': experiencedata})
    



def ChangePassword(request):
    if "sid" not in  request.session :
        return redirect("Guest:Login")
    else:
        serviceproviderdata=tbl_serviceprovider.objects.get(id=request.session['sid'])
        dbpassword = serviceproviderdata.serviceprovider_password
        if request.method=='POST':
            oldpassword=request.POST.get('txt_oldpassword')
            newpassword=request.POST.get('txt_newpassword')
            retypepassword=request.POST.get('txt_retypepassword')
            if dbpassword==oldpassword:
                if newpassword==retypepassword:
                    serviceproviderdata.serviceprovider_password=newpassword
                    serviceproviderdata.save()
                    return render(request,"ServiceProvider/ServiceProviderProfile.html",{'msg': "Password Changed..",'serviceproviderdata': serviceproviderdata})
                else:
                    return render(request,"ServiceProvider/ChangePassword.html",{'msg':"Old password and  Retype Password Does not match..",'serviceproviderdata':serviceproviderdata})
            else:
                return render(request,"ServiceProvider/ChangePassword.html",{'msg':"Current Password Not Match..",'serviceproviderdata':serviceproviderdata})
        else:
            return render(request,"ServiceProvider/ChangePassword.html",{'serviceproviderdata':serviceproviderdata})
    

    

def EditPhoto(request, sid):
    if "sid" not in  request.session :
        return redirect("Guest:Login")
    else:
        editphoto = tbl_serviceprovider.objects.get(id=sid)
        serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])

        if request.method == "POST":
            if request.FILES.get("file_photo"):
                editphoto.serviceprovider_photo = request.FILES["file_photo"]
                editphoto.save()

            return render(request, "ServiceProvider/EditPhoto.html", {'msg': "Photo Updated Succusfully",'editphoto': editphoto,'serviceproviderdata':serviceproviderdata})
        else:
            return render(request, "ServiceProvider/EditPhoto.html", {'editphoto': editphoto,'serviceproviderdata':serviceproviderdata})





def MyServices(request):
    if "sid" not in  request.session :
        return redirect("Guest:Login")
    else:
        servicedata = tbl_servicetype.objects.all()
        myservices = tbl_serviceproviderstype.objects.filter(serviceprovider=request.session['sid'])
        serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])

        if request.method == "POST":
            service_id = request.POST.get("sel_services")

            if tbl_serviceproviderstype.objects.filter(servicetype_id=service_id, serviceprovider_id=request.session['sid']):
                return render(request, "ServiceProvider/MyServices.html", {'msg': "Already Added",'serviceproviderdata':serviceproviderdata})

            servicetype = tbl_servicetype.objects.get(id=service_id)
            tbl_serviceproviderstype.objects.create(servicetype=servicetype, serviceprovider_id=request.session['sid'])

            myservices = tbl_serviceproviderstype.objects.filter(serviceprovider_id=request.session['sid'])
            return render(request, "ServiceProvider/MyServices.html", {'msg': "Service Added",'serviceproviderdata':serviceproviderdata})
        else:
            return render(request, "ServiceProvider/MyServices.html", {'servicedata': servicedata,'MyServices': myservices,'serviceproviderdata':serviceproviderdata})




def deleteserviceproviderstype(request,did):
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    tbl_serviceproviderstype.objects.get(id=did).delete()
    return render(request,"ServiceProvider/MyServices.html",{'msg':"Data Deleted",'serviceproviderdata':serviceproviderdata})


def editserviceproviderstype(request, eid):
    sid = request.session.get("sid")
    editdata = tbl_serviceproviderstype.objects.get(id=eid)
    servicedata = tbl_servicetype.objects.all()
    myservices = tbl_serviceproviderstype.objects.filter(serviceprovider_id=sid)
    serviceproviderdata=tbl_serviceprovider.objects.get(id=request.session['sid'])

    if request.method == "POST":
        servicetype_id = request.POST.get("sel_services")

        if tbl_serviceproviderstype.objects.filter(servicetype_id=servicetype_id,serviceprovider_id=sid):
            return render(request, "ServiceProvider/MyServices.html", {'msg': "Already Added",'serviceproviderdata':serviceproviderdata})
        
        editdata.servicetype_id = servicetype_id
        editdata.save()

        return render(request, "ServiceProvider/MyServices.html", {'msg': "Data Updated..",'serviceproviderdata':serviceproviderdata})
    else:
        return render(request, "ServiceProvider/MyServices.html", {'editdata': editdata,'servicedata': servicedata,'services': servicedata,'MyServices': myservices,'serviceproviderdata':serviceproviderdata})
    



def MyServiceRequest(request):
    if "sid" not in  request.session :
        return redirect("Guest:Login")
    else:
        serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
        myservicerequestdata = tbl_servicerequest.objects.filter(serviceprovider=request.session['sid']).order_by('-servicerequest_date', '-id')
        return render(request,"ServiceProvider/ViewRequest.html",{'myservicerequestdata':myservicerequestdata,'serviceproviderdata':serviceproviderdata})


def UserDetails(request, id):
    userdata = tbl_servicerequest.objects.get(id=id).user
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    return render(request, "ServiceProvider/UserDetails.html", {'userdata': userdata,'serviceproviderdata':serviceproviderdata})



def ServiceAccept(request,aid):
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    reqdata=tbl_servicerequest.objects.get(id=aid)
    reqdata.servicerequest_status = 1
    reqdata.save()
    return render(request, "ServiceProvider/ViewRequest.html",{'msg': "Request Accepted",'serviceproviderdata':serviceproviderdata})


def ServiceReject(request,aid):
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    reqdata=tbl_servicerequest.objects.get(id=aid)
    reqdata.servicerequest_status = 2
    reqdata.save()
    return render(request, "ServiceProvider/ViewRequest.html",{'msg': "Request Rejected",'serviceproviderdata':serviceproviderdata})


def ServiceStart(request,aid):
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    reqdata=tbl_servicerequest.objects.get(id=aid)
    reqdata.servicerequest_status = 3
    reqdata.save()
    return render(request, "ServiceProvider/ViewRequest.html",{'msg': "Work Started",'serviceproviderdata':serviceproviderdata})


def ServiceProgress(request,aid):
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    reqdata=tbl_servicerequest.objects.get(id=aid)
    reqdata.servicerequest_status = 4
    reqdata.save()
    return render(request, "ServiceProvider/ViewRequest.html",{'msg': "Work in Progress",'serviceproviderdata':serviceproviderdata})


def ServiceEnd(request,aid):
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    reqdata=tbl_servicerequest.objects.get(id=aid)
    reqdata.servicerequest_status = 5
    reqdata.save()
    return render(request, "ServiceProvider/ViewRequest.html",{'msg': "Work Ended",'serviceproviderdata':serviceproviderdata})



def CancelServiceRequest(request, id):
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    req = tbl_companyservice.objects.get(id=id)

    if req.companyservice_status == 0:
        req.companyservice_status = 6
        req.save()
        return render(request, "User/MyCompanyRequest.html", {'msg': "Request Canceled..",'serviceproviderdata':serviceproviderdata})
    else:
        return render(request, "User/MyCompanyRequest.html", {'req': req,'serviceproviderdata':serviceproviderdata})



def Complaint(request):
    if "sid" not in  request.session :
        return redirect("Guest:Login")
    else:
        complaintdata = tbl_complaint.objects.filter(serviceprovider=request.session['sid']).order_by('-id')
        serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
        if request.method == 'POST':
            title = request.POST.get('txt_title') 
            content = request.POST.get('txt_content')
            date = datetime.now()
            serviceprovider = tbl_serviceprovider.objects.get(id=request.session['sid'])
            tbl_complaint.objects.create(complaint_title=title,complaint_content=content,complaint_date=date,serviceprovider=serviceprovider)
            return render(request, "ServiceProvider/Complaint.html", {'msg': "Complaint Submitted",'serviceproviderdata':serviceproviderdata})
        else:
            return render(request, "ServiceProvider/Complaint.html",{'complaintdata':complaintdata,'serviceproviderdata':serviceproviderdata})
    


def DeleteComplaint(request,did):
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    tbl_complaint.objects.get(id=did).delete()
    return render(request,"ServiceProvider/Complaint.html",{'msg':"Data Deleted",'serviceproviderdata':serviceproviderdata})



def EditComplaint(request,eid):
    editdata=tbl_complaint.objects.get(id=eid)
    complaintdata=tbl_complaint.objects.filter(serviceprovider=request.session['sid']).order_by('-id')
    serviceproviderdata=tbl_serviceprovider.objects.get(id=request.session['sid'])
    if request.method=='POST':
        title = request.POST.get('txt_title')
        content = request.POST.get('txt_content')
        editdata.complaint_title=title
        editdata.complaint_content=content
        editdata.save()
        return render(request,"ServiceProvider/Complaint.html",{'msg':"Data Updated..",'serviceproviderdata':serviceproviderdata})
    else:
        return render(request,"ServiceProvider/Complaint.html",{'editdata':editdata,'complaintdata':complaintdata,'serviceproviderdata':serviceproviderdata})
    

def ViewUserComplaint(request, sid):
    if "sid" not in request.session:
        return redirect("Guest:Login")
    else:
        complaintservicedata = tbl_complaint.objects.filter(servicerequest=sid,servicerequest__serviceprovider=request.session['sid']).order_by('-id')
        serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
        return render(request,"ServiceProvider/ViewUserComplaint.html",{'complaintservicedata': complaintservicedata,'serviceproviderdata':serviceproviderdata})



def ComplaintReply(request, id):
    replydata = tbl_complaint.objects.get(id=id)
    sid = replydata.servicerequest.id
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])

    if request.method == 'POST':
        replydata.complaint_reply = request.POST.get('txt_reply')
        replydata.complaint_status = 1
        replydata.save()

        return render(request,"ServiceProvider/ViewUserComplaint.html",{'msg': "Reply submitted successfully", 'sid': sid,'serviceproviderdata':serviceproviderdata})
    else:
        return render(request,'ServiceProvider/Reply.html',{'replydata': replydata, 'sid': sid,'serviceproviderdata':serviceproviderdata})

    


def Amount(request,aid):
    servicerequest=tbl_servicerequest.objects.get(id=aid)
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    if request.method == 'POST':
        amount=request.POST.get('txt_amount')
        servicerequest.servicerequest_amount = amount
        servicerequest.servicerequest_status=7
        servicerequest.save()
        return render(request,"ServiceProvider/ViewRequest.html",{'msg':"Amount Added...",'serviceproviderdata':serviceproviderdata})
    else: 
        return render(request,"ServiceProvider/Amount.html",{'serviceproviderdata':serviceproviderdata})
    


def ServicePaymentComplete(request,aid):
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    reqdata=tbl_servicerequest.objects.get(id=aid)
    reqdata.servicerequest_status = 8
    reqdata.save()
    return render(request, "ServiceProvider/ViewRequest.html",{'msg': "Payment Completed",'serviceproviderdata':serviceproviderdata})


def Logout(request):
      del request.session["sid"]
      return redirect('Guest:Index')

    

def ViewServiceRating(request,sid):
    ratingdata=tbl_rating.objects.filter(servicerequest=sid).order_by('-datetime','id')
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
    count=ratingdata.count()
    avg=0
    if count>0:
        total=0
        for i in ratingdata:
            total+=i.rating_data
        avg=total//count
    return render(request,"ServiceProvider/ViewServiceRating.html",{'ratingdata':ratingdata,'avg':avg,'count':count,'sid':sid,'serviceproviderdata':serviceproviderdata})


def ServiceRemark(request, id):
        remarkdata = tbl_servicerequest.objects.get(id=id)
        serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
        if request.method == 'POST':
            remarkdata.servicerequest_remark = request.POST.get('txt_remark')
            remarkdata.servicerequest_status = 5
            remarkdata.save()
            return render(request,"ServiceProvider/ViewRequest.html",{'msg': "Remark submitted successfully",'serviceproviderdata':serviceproviderdata})
        else:
            return render(request,'ServiceProvider/Remark.html',{'remarkdata': remarkdata,'serviceproviderdata':serviceproviderdata})
        



def serviceprovider_revenue_report(request):

    if "sid" not in request.session:
        return redirect("Guest:Login")

    spid = request.session["sid"]

    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")
    user_name = request.GET.get("user_name", "")
    service_type = request.GET.get("service_type", "")


    service_types = tbl_serviceproviderstype.objects.filter(serviceprovider_id=spid).select_related("servicetype")
    report = tbl_servicerequest.objects.filter(serviceprovider_id=spid,servicerequest_status=8).select_related("user","servicetype").order_by("-servicerequest_date","-id")
    serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])

    if from_date and to_date:

        report = report.filter(servicerequest_date__date__range=[from_date, to_date])

    if user_name:

        report = report.filter(user__user_name__icontains=user_name)

    if service_type:

        report = report.filter(servicetype_id=service_type)


    total_requests = report.count()


    total_revenue = report.aggregate(total=Sum("servicerequest_amount"))["total"] or 0

    context = {"report": report,"total_requests": total_requests,"total_revenue": total_revenue,"service_types": service_types,"user_name": user_name,"from_date": from_date,"to_date": to_date,"service_type": service_type,'serviceproviderdata':serviceproviderdata}

    return render(request,"ServiceProvider/Report.html",context)


def ServiceRejectReply(request,id):
        rejectreplay = tbl_servicerequest.objects.get(id=id)
        serviceproviderdata = tbl_serviceprovider.objects.get(id=request.session['sid'])
        if request.method == 'POST':
            rejectreplay.servicerequest_reject = request.POST.get('txt_reject')
            rejectreplay.servicerequest_status = 2
            rejectreplay.save()
            return render(request,"ServiceProvider/ViewRequest.html",{'msg': "Reason submitted successfully",'serviceproviderdata':serviceproviderdata})
        else:
            return render(request,'ServiceProvider/RejectReply.html',{'rejectreplay': rejectreplay,'serviceproviderdata':serviceproviderdata})



