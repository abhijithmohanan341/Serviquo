from django.shortcuts import render,redirect
from User.models import *
from Company.models import *
from Guest.models import *
from Technician.models import *
from datetime import datetime
from django.db.models import Sum



def homepage(request):
    if "tid" not in  request.session :
        return redirect("Guest:Login")
    else:
        techniciandata = tbl_technician.objects.get(id=request.session['tid'])
        return render(request,"Technician/HomePage.html",{'techniciandata':techniciandata})


def TechnicianProfile(request):
    if "tid" not in  request.session :
        return redirect("Guest:Login")
    else:
        techniciandata=tbl_technician.objects.get(id=request.session['tid'])
        return render(request,"Technician/TechnicianProfile.html",{'techniciandata':techniciandata})



def EditProfile(request):
    if "tid" not in  request.session :
        return redirect("Guest:Login")
    else:
        techniciandata=tbl_technician.objects.get(id=request.session['tid'])
        Placedata=tbl_place.objects.get(id=techniciandata.place.id)
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
            checkshop = tbl_shop.objects.filter(shop_email=email).count()
            checktechnician = tbl_technician.objects.filter(technician_email=email).exclude(id=request.session['tid']).count()

            if checkadmin > 0:
                return render(request,"Technician/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkuser > 0:
                return render(request,"Technician/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkcompany > 0:
                return render(request,"Technician/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkserviceprovider > 0:
                return render(request,"Technician/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkshop > 0:
                return render(request,"Technician/EditProfile.html",{'msg':"Email Already Exist"})
            elif checktechnician > 0:
                return render(request,"Technician/EditProfile.html",{'msg':"Email Already Exist"})
            else:
                techniciandata.technician_name=name
                techniciandata.technician_email=email
                techniciandata.technician_contact=contact
                techniciandata.technician_address=address
                techniciandata.district=district
                techniciandata.place=place
                techniciandata.save()
                return render(request,"Technician/EditProfile.html",{'msg':"Profile updated successfully",'techniciandata':techniciandata,'district':districtdata,'place':Pla})
        else:
            return render(request,"Technician/EditProfile.html",{'techniciandata':techniciandata,'district':districtdata,'place':Pla})
        



def ChangePassword(request):
    if "tid" not in  request.session :
        return redirect("Guest:Login")
    else:
        techniciandata=tbl_technician.objects.get(id=request.session['tid'])
        dbpassword = techniciandata.technician_password
        if request.method=='POST':
            oldpassword=request.POST.get('txt_oldpassword')
            newpassword=request.POST.get('txt_newpassword')
            retypepassword=request.POST.get('txt_retypepassword')
            if dbpassword==oldpassword:
                if newpassword==retypepassword:
                    techniciandata.technician_password=newpassword
                    techniciandata.save()
                    return render(request,"Technician/TechnicianProfile.html",{'msg':"Password Changed..",'techniciandata': techniciandata})
                else:
                    return render(request,"Technician/ChangePassword.html",{'msg':"Old password and  Retype Password Does not match..",'techniciandata':techniciandata})
            else:
                return render(request,"Technician/ChangePassword.html",{'msg':"Current Password Not Match.."})
        else:
            return render(request,"Technician/ChangePassword.html",{'techniciandata':techniciandata})
        



def EditPhoto(request, tid):
    if "tid" not in  request.session :
        return redirect("Guest:Login")
    else:
        editphoto = tbl_technician.objects.get(id=tid)
        techniciandata = tbl_technician.objects.get(id=request.session['tid'])
        if request.method == "POST":
            if request.FILES.get("file_photo"):
                editphoto.technician_photo = request.FILES["file_photo"]
                editphoto.save()

            return render(request, "Technician/EditPhoto.html", {'msg': "Photo Updated Successfully",'editphoto': editphoto,'techniciandata':techniciandata})
        else:
            return render(request, "Technician/EditPhoto.html", {'editphoto': editphoto,'techniciandata': techniciandata})
    



def MyRequest(request):
    if "tid" not in  request.session :
        return redirect("Guest:Login")
    else:
        myrequestdata=tbl_companyservice.objects.filter(technician=request.session['tid'],companyservice_status__gt=2).order_by('-companyservice_date', '-id')
        techniciandata = tbl_technician.objects.get(id=request.session['tid'])
        return render(request,"Technician/MyRequest.html",{'myrequestdata':myrequestdata,'techniciandata': techniciandata})
  

def UserDetails(request, id):
    userdata = tbl_companyservice.objects.get(id=id).user
    techniciandata = tbl_technician.objects.get(id=request.session['tid'])
    return render(request, "Technician/UserDetails.html", {'userdata': userdata,'techniciandata': techniciandata})



def Complaint(request):
    if "tid" not in  request.session :
        return redirect("Guest:Login")
    else:
        complaintdata = tbl_complaint.objects.filter(technician=request.session['tid'])
        techniciandata = tbl_technician.objects.get(id=request.session['tid'])
        if request.method == 'POST':
            title = request.POST.get('txt_title')
            content = request.POST.get('txt_content')
            date = datetime.now()
            technician = tbl_technician.objects.get(id=request.session['tid'])
            tbl_complaint.objects.create(complaint_title=title,complaint_content=content,complaint_date=date,technician=technician)
            return render(request, "Technician/Complaint.html", {'msg': "Complaint Submitted",'techniciandata': techniciandata})
        else:
            return render(request, "Technician/Complaint.html",{'complaintdata':complaintdata,'techniciandata': techniciandata})
    

def DeleteComplaint(request,did):
    tbl_complaint.objects.get(id=did).delete()
    techniciandata = tbl_technician.objects.get(id=request.session['tid'])
    return render(request,"Technician/Complaint.html",{'msg':"Data Deleted",'techniciandata': techniciandata})


def EditComplaint(request,eid):
    if "tid" not in  request.session :
        return redirect("Guest:Login")
    else:
        editdata=tbl_complaint.objects.get(id=eid)
        complaintdata=tbl_complaint.objects.filter(technician=request.session['tid'])
        techniciandata = tbl_technician.objects.get(id=request.session['tid'])
        if request.method=='POST':
            title = request.POST.get('txt_title')
            content = request.POST.get('txt_content')
            editdata.complaint_title=title
            editdata.complaint_content=content
            editdata.save()
            return render(request,"Technician/Complaint.html",{'msg':"Data Updated..",'techniciandata': techniciandata})
        else:
            return render(request,"Technician/Complaint.html",{'editdata':editdata,'complaintdata':complaintdata,'techniciandata': techniciandata})
    

    

def ServiceStart(request,aid):
    techniciandata=tbl_technician.objects.get(id=request.session['tid'])
    reqdata=tbl_companyservice.objects.get(id=aid)
    reqdata.companyservice_status = 4
    reqdata.save()
    return render(request, "Technician/MyRequest.html",{'msg': "Work Started",'techniciandata': techniciandata})


def ServiceProgress(request,aid):
    techniciandata=tbl_technician.objects.get(id=request.session['tid'])
    reqdata=tbl_companyservice.objects.get(id=aid)
    reqdata.companyservice_status = 5
    reqdata.save()
    return render(request, "Technician/MyRequest.html",{'msg': "Work in Progress",'techniciandata': techniciandata})


def ServiceEnd(request,aid):
    techniciandata=tbl_technician.objects.get(id=request.session['tid'])
    reqdata=tbl_companyservice.objects.get(id=aid)
    reqdata.companyservice_status = 6
    reqdata.save()
    return render(request, "Technician/MyRequest.html",{'msg': "Work Ended",'techniciandata': techniciandata})



def Amount(request,aid):
    companyequest=tbl_companyservice.objects.get(id=aid)
    techniciandata = tbl_technician.objects.get(id=request.session['tid'])

    if request.method == 'POST':
        amount=request.POST.get('txt_amount')
        companyequest.companyservice_amount = amount
        companyequest.companyservice_status=7
        companyequest.save()
        return render(request,"Technician/MyRequest.html",{'msg':"Amount Added...",'techniciandata': techniciandata})
    else: 
        return render(request,"Technician/Amount.html",{'techniciandata': techniciandata})
    



def CompanyPaymentComplete(request,aid):
    techniciandata=tbl_technician.objects.get(id=request.session['tid'])
    reqdata=tbl_servicerequest.objects.get(id=aid)
    reqdata.servicerequest_status = 9
    reqdata.save()
    return render(request, "Technician/MyRequest.html",{'msg': "Payment Completed",'techniciandata': techniciandata})




def LeaveRequest(request):
    if "tid" not in  request.session :
        return redirect("Guest:Login")
    else:
        tech = tbl_technician.objects.get(id=request.session['tid'])
        leavedata = tbl_technicianleave.objects.filter(technician=tech).order_by('-applied_date', '-id')
        techniciandata = tbl_technician.objects.get(id=request.session['tid'])
        if request.method == "POST":
            fromdate = request.POST["date_fromdate"]
            todate = request.POST["date_todate"]
            reason = request.POST["txt_reason"]
            date = datetime.now()
            tbl_technicianleave.objects.create(leave_fromdate=fromdate,leave_todate=todate,leave_reason=reason,applied_date=date,technician=tech)
            return render(request, "Technician/LeaveRequest.html", {'msg': "Leave Request Submitted",'techniciandata': techniciandata})
        else:
            return render(request, "Technician/LeaveRequest.html", {"leavedata": leavedata,'techniciandata': techniciandata})




def DeleteLeave(request,did):
    tbl_technicianleave.objects.get(id=did).delete()
    techniciandata = tbl_technician.objects.get(id=request.session['tid'])
    return render(request,"Technician/LeaveRequest.html",{'msg':"Request Deleted",'techniciandata': techniciandata})



def Logout(request):
      del request.session["tid"]
      return redirect('Guest:Index')



def ServiceRemark(request, id):
        remarkdata = tbl_companyservice.objects.get(id=id)
        techniciandata = tbl_technician.objects.get(id=request.session['tid'])
        if request.method == 'POST':
            remarkdata.companyservice_remark = request.POST.get('txt_remark')
            remarkdata.companyservice_status = 6
            remarkdata.save()
            return render(request,"Technician/MyRequest.html",{'msg': "Remark submitted successfully",'techniciandata': techniciandata})
        else:
            return render(request,'Technician/Remark.html',{'remarkdata': remarkdata,'techniciandata': techniciandata})
        



def technician_revenue_report(request):

    if "tid" not in request.session:
        return redirect("Guest:Login")

    technician_id = request.session["tid"]

    user_name = request.GET.get("user_name", "")
    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")

    report = tbl_companyservice.objects.filter(technician_id=technician_id,companyservice_status=9).select_related("user", "company").order_by("-companyservice_date", "-id")
    techniciandata = tbl_technician.objects.get(id=request.session['tid'])


    if user_name:
        report = report.filter(user__user_name__icontains=user_name)


    if from_date and to_date:
        report = report.filter(companyservice_date__date__range=[from_date, to_date])


    total_revenue = report.aggregate(total=Sum("companyservice_amount"))["total"] or 0

    total_requests = report.count()


    context = {"report": report,"total_requests": total_requests,"total_revenue": total_revenue,"user_name": user_name,"from_date": from_date,"to_date": to_date,'techniciandata': techniciandata}

    return render(request, "Technician/Report.html", context)