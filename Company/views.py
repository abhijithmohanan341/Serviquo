from django.shortcuts import render,redirect
from User.models import *
from Company.models import *
from Guest.models import *
from Technician.models import *
from datetime import datetime
from datetime import date
from django.db.models import Sum
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def homepage(request):
    if "cid" not in request.session:
        return redirect("Guest:Login")
    else:
        companydata = tbl_company.objects.get(id=request.session['cid'])
        return render(request,"Company/HomePage.html",{'companydata': companydata})



def CompanyProfile(request):
    if "cid" not in  request.session :
        return redirect("Guest:Login")
    else:
        companydata=tbl_company.objects.get(id=request.session['cid'])
        return render(request,"Company/CompanyProfile.html",{'companydata':companydata})



def EditProfile(request):
    if "cid" not in request.session:
        return redirect("Guest:Login")
    else:
        companydata = tbl_company.objects.get(id=request.session['cid'])
        Placedata = tbl_place.objects.get(id=companydata.place.id)
        Pla = tbl_place.objects.filter(district=Placedata.district)
        districtdata = tbl_district.objects.all().order_by('district_name')

        if request.method == 'POST':
            name = request.POST.get('txt_name')
            email = request.POST.get('txt_email')
            contact = request.POST.get('txt_contact')
            address = request.POST.get('txt_address')
            district = tbl_district.objects.get(id=request.POST.get('sel_district'))
            place = tbl_place.objects.get(id=request.POST.get('sel_place'))

            checkadmin = tbl_admin.objects.filter(admin_email=email).count()
            checkuser = tbl_user.objects.filter(user_email=email).count()
            checkcompany = tbl_company.objects.filter(company_email=email).exclude(id=request.session['cid']).count()
            checkserviceprovider = tbl_serviceprovider.objects.filter(serviceprovider_email=email).count()
            checkshop = tbl_shop.objects.filter(shop_email=email).count()
            checktechnician = tbl_technician.objects.filter(technician_email=email).count()

            if checkadmin > 0:
                return render(request,"Company/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkuser > 0:
                return render(request,"Company/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkcompany > 0:
                return render(request,"Company/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkserviceprovider > 0:
                return render(request,"Company/EditProfile.html",{'msg':"Email Already Exist"})
            elif checkshop > 0:
                return render(request,"Company/EditProfile.html",{'msg':"Email Already Exist"})
            elif checktechnician > 0:
                return render(request,"Company/EditProfile.html",{'msg':"Email Already Exist"})
            else:
                companydata.company_name = name
                companydata.company_email = email
                companydata.company_contact = contact
                companydata.company_address = address
                companydata.district = district
                companydata.place = place
                companydata.save()
                return render(request,"Company/EditProfile.html",{'msg':"Profile updated successfully",'companydata':companydata,'district':districtdata,'place':Pla})
        else:
            return render(request,"Company/EditProfile.html",{'companydata':companydata,'district':districtdata,'place':Pla})

        

def ChangePassword(request):
    if "cid" not in  request.session :
        return redirect("Guest:Login")
    else:
        companydata=tbl_company.objects.get(id=request.session['cid'])
        dbpassword = companydata.company_password
        if request.method=='POST':
            oldpassword=request.POST.get('txt_oldpassword')
            newpassword=request.POST.get('txt_newpassword')
            retypepassword=request.POST.get('txt_retypepassword')
            if dbpassword==oldpassword:
                if newpassword==retypepassword:
                    companydata.company_password=newpassword
                    companydata.save()
                    return render(request,"Company/CompanyProfile.html",{'msg':"Password Changed..",'companydata': companydata})
                else:
                    return render(request,"Company/ChangePassword.html",{'msg':"Old password and  Retype Password Does not match..",'companydata': companydata})
            else:
                return render(request,"Company/ChangePassword.html",{'msg':"Current Password Not Match..",'companydata': companydata})
        else:
            return render(request,"Company/ChangePassword.html",{'companydata':companydata})
    


def EditPhoto(request, cid):

    companydata=tbl_company.objects.get(id=request.session['cid'])
    editphoto = tbl_company.objects.get(id=request.session['cid'])

    if request.method == "POST":
        if request.FILES.get("file_logo"):
            editphoto.company_logo = request.FILES["file_logo"]
            editphoto.save()

        return render(request, "Company/CompanyProfile.html", {'msg': "Photo Changed Successfully",'editphoto': editphoto,'companydata':companydata})
    else:
        return render(request, "Company/EditPhoto.html", {'editphoto': editphoto,'companydata':companydata})    



def TechnicianRegistration(request):
    if "cid" not in  request.session :
        return redirect("Guest:Login")
    else:
        techniciandata=tbl_technician.objects.filter(company=request.session['cid'])
        districtdata=tbl_district.objects.all().order_by('district_name')
        placedata=tbl_place.objects.all()
        company=tbl_company.objects.all()
        companydata=tbl_company.objects.get(id=request.session['cid'])
        if request.method=='POST':
            name=request.POST.get('txt_name')
            email=request.POST.get('txt_email')
            contact=request.POST.get('txt_contact')
            address=request.POST.get('txt_address')
            district=tbl_district.objects.get(id=request.POST.get('sel_district'))
            place=tbl_place.objects.get(id=request.POST.get('sel_place'))
            company=tbl_company.objects.get(id=request.session['cid'])
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
                    return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
                elif checkuseremail > 0 :
                    return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
                elif checkcompanyemail > 0 :
                    return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
                elif checkserviceprovideremail > 0 :
                    return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
                elif checkshopemail > 0 :
                    return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
                elif checktechnicianemail > 0 :
                    return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
                else:
                    tbl_technician.objects.create(technician_name=name,technician_email=email,technician_contact=contact,technician_address=address,place=place,company=company,technician_photo=photo,technician_proof=proof,technician_password=password)
                    subject = "Serviquo | Technician Registration Successful"

                    message = (
                        f"Dear {name},\n\n"
                        
                        f"Your technician account has been successfully created on Serviquo.\n\n"

                        f"Company: {company.company_name}\n\n"
                        
                        f"Your login details are as follows:\n\n"
                        f"Email: {email}\n"
                        f"Password: {password}\n\n"
                        
                        f"You can now log in and start using the system.\n\n"
                        
                        f"For security purposes, we recommend that you change your password after logging in.\n\n"
                        
                        f"If you need any assistance, please contact our support team.\n\n"
                        
                        f"Best regards,\n\n"
                        f"Serviquo Team"
                    )

                    send_mail(subject,message,settings.EMAIL_HOST_USER,[email],fail_silently=False,)

                    return render(request,"Company/TechnicianRegistration.html",{'msg':"Registration completed successfully and send Mail to technician",'technicianregistration':techniciandata,'district':districtdata,'place':placedata,'companydata': companydata})
            else:
                return render(request,"Company/TechnicianRegistration.html",{'msg':"Confirm Password Mismatch",'technicianregistration':techniciandata,'district':districtdata,'place':placedata,'companydata': companydata})
        else:
            return render(request,'Company/TechnicianRegistration.html', {'technicianregistration':techniciandata,'district':districtdata,'place':placedata,'companydata':companydata,'company':company})
        



def deleteTechnician(request,did):
    tbl_technician.objects.get(id=did).delete()
    companydata = tbl_company.objects.get(id=request.session['cid'])
    return render(request,"Company/TechnicianRegistration.html",{'msg':"Technician Deleted Successfully",'companydata': companydata})



def editTechnician(request, eid):
    editdata = tbl_technician.objects.get(id=eid)
    techniciandata = tbl_technician.objects.filter(company=request.session['cid'])
    placedata = tbl_place.objects.get(id=editdata.place.id)
    place = tbl_place.objects.filter(district=placedata.district)
    district = tbl_district.objects.all().order_by('district_name')
    companydata=tbl_company.objects.get(id=request.session['cid'])

    if request.method == 'POST':
        name = request.POST.get('txt_name')
        email = request.POST.get('txt_email')
        contact = request.POST.get('txt_contact')
        address = request.POST.get('txt_address')
        sel_place = tbl_place.objects.get(id=request.POST.get('sel_place'))

        checkemail = tbl_admin.objects.filter(admin_email=email).count()
        checkuseremail = tbl_user.objects.filter(user_email=email).count()
        checkcompanyemail = tbl_company.objects.filter(company_email=email).count()
        checkserviceprovideremail = tbl_serviceprovider.objects.filter(serviceprovider_email=email).count()
        checkshopemail = tbl_shop.objects.filter(shop_email=email).count()
        checktechnicianemail = tbl_technician.objects.filter(technician_email=email).exclude(id=eid).count()

        if checkemail > 0:
            return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
        elif checkuseremail > 0:
            return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
        elif checkcompanyemail > 0:
            return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
        elif checkserviceprovideremail > 0:
            return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
        elif checkshopemail > 0:
            return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
        elif checktechnicianemail > 0:
            return render(request,"Company/TechnicianRegistration.html",{'msg':"Email Already Exist"})
        else:
            editdata.technician_name = name
            editdata.technician_email = email
            editdata.technician_contact = contact
            editdata.technician_address = address
            editdata.place = sel_place

            if request.POST.get('txt_password'):
                editdata.technician_password = request.POST.get('txt_password')

            if request.FILES.get("file_photo"):
                editdata.technician_photo = request.FILES["file_photo"]

            if request.FILES.get("file_proof"):
                editdata.technician_proof = request.FILES["file_proof"]

            editdata.save()
            
            subject = "Serviquo | Technician Profile Updated"

            message = (
                f"Dear {name},\n\n"
                
                f"Your technician profile has been successfully updated on Serviquo.\n\n"
                
                f"Company: {companydata.company_name}\n\n"
                
                f"Updated details:\n\n"
                f"Email: {email}\n"
                f"Contact: {contact}\n"
                f"Address: {address}\n"

            )

            if request.POST.get('txt_password'):
                message += (
                    f"Password: {request.POST.get('txt_password')}\n\n"
                    f"For security purposes, please change your password after logging in.\n\n"
                )

            message += (
                f"If you did not make these changes, please contact our support team immediately.\n\n"
                
                f"Best regards,\n\n"
                f"Serviquo Team"
            )

            send_mail(subject,message,settings.EMAIL_HOST_USER,[email],fail_silently=False,)

            return render(request,"Company/TechnicianRegistration.html",{'msg':"Profile updated successfully and send Mail to technician",'technicianregistration':techniciandata,'district':district,'place':place,'companydata': companydata})
    else:
        return render(request,"Company/TechnicianRegistration.html",{'editdata':editdata,'technicianregistration':techniciandata,'district':district,'place':place,'companydata':companydata})




def ViewRequest(request):
    if "cid" not in  request.session :
        return redirect("Guest:Login")
    else:
        viewrequestdata = tbl_companyservice.objects.filter(company=request.session['cid']).order_by('-companyservice_date', '-id')
        companydata=tbl_company.objects.get(id=request.session['cid'])
        return render(request,"Company/ViewRequest.html",{'viewrequestdata':viewrequestdata,'companydata':companydata})



def CompanyServiceAccept(request,aid):
    reqdata=tbl_companyservice.objects.get(id=aid)
    companydata = tbl_company.objects.get(id=request.session['cid'])
    reqdata.companyservice_status = 1
    reqdata.save()
    return render(request, "Company/ViewRequest.html",{'msg': "Request Accepted",'companydata': companydata})


def CompanyServiceReject(request,aid):
    reqdata=tbl_companyservice.objects.get(id=aid)
    companydata = tbl_company.objects.get(id=request.session['cid'])
    reqdata.companyservice_status = 2
    reqdata.save()
    return render(request, "Company/ViewRequest.html",{'msg': "Request Rejected",'companydata': companydata})


def TechnicianAssign(request):
    if "cid" not in  request.session :
        return redirect("Guest:Login")
    else:
        viewrequestdata = tbl_companyservice.objects.filter(company=request.session['cid'],companyservice_status=1)
        companydata = tbl_company.objects.get(id=request.session['cid'])
        return render(request, "Company/TechnicianAssign.html", {'viewrequestdata': viewrequestdata,'companydata': companydata})



def Assign(request, rid):
    requestdata = tbl_companyservice.objects.get(id=rid)
    techniciandata = tbl_technician.objects.filter(company=request.session['cid']).order_by('technician_name')
    today = date.today()
    leave = tbl_technicianleave.objects.filter(leave_status=1,leave_fromdate__lte=today,leave_todate__gte=today).values_list('technician_id', flat=True)
    companydata = tbl_company.objects.get(id=request.session['cid'])

    if request.method == 'POST':
        tech_id = request.POST.get('sel_technician')

        if int(tech_id) in leave:
            return render(request,'Company/Assign.html',{'techniciandata': techniciandata,'leave_tech_ids': leave,'requestdata': requestdata,'companydata': companydata,'msg': "Selected technician is on leave"})
        else:
            technicianname = tbl_technician.objects.get(id=tech_id)
            requestdata.technician = technicianname
            requestdata.companyservice_status = 3
            requestdata.save()
            return redirect("Company:ViewRequest")
    else:
        return render(request,'Company/Assign.html',{'techniciandata': techniciandata,'leave_tech_ids': leave,'requestdata': requestdata,'companydata':companydata})
    


def CancelCompanyServiceRequest(request, id):
    req = tbl_companyservice.objects.get(id=id)
    companydata = tbl_company.objects.get(id=request.session['cid'])

    if req.companyservice_status == 0:
        req.companyservice_status = 7
        req.save()
        return render(request, "Company/ViewRequest.html", {'msg': "Request Canceled..",'companydata': companydata})
    else:
        return render(request, "Company/ViewRequest.html", {'req': req,'companydata': companydata})
    


def CompanyPaymentComplete(request,aid):
    reqdata=tbl_servicerequest.objects.get(id=aid)
    companydata = tbl_company.objects.get(id=request.session['cid'])
    reqdata.servicerequest_status = 9
    reqdata.save()
    return render(request, "Company/ViewRequest.html",{'msg': "Payment Completed",'companydata': companydata})
    



def Complaint(request):
    if "cid" not in  request.session :
        return redirect("Guest:Login")
    else:
        complaintdata = tbl_complaint.objects.filter(company=request.session['cid']).order_by('-id')
        companydata=tbl_company.objects.get(id=request.session['cid'])
        if request.method == 'POST':
            title = request.POST.get('txt_title')
            content = request.POST.get('txt_content')
            date = datetime.now()
            company = tbl_company.objects.get(id=request.session['cid'])
            tbl_complaint.objects.create(complaint_title=title,complaint_content=content,complaint_date=date,company=company)
            return render(request, "Company/Complaint.html", {'msg': "Complaint Submitted",'companydata': companydata})
        else:
            return render(request, "Company/Complaint.html",{'complaintdata':complaintdata,'companydata':companydata})
    


def ViewComplaint(request):
    if "cid" not in  request.session :
        return redirect("Guest:Login")
    else:
        complainttechniciandata = tbl_complaint.objects.filter(technician__company=request.session['cid']).order_by('-id')
        companydata=tbl_company.objects.get(id=request.session['cid'])
        return render(request, "Company/ViewComplaints.html",{'complainttechniciandata':complainttechniciandata,'companydata':companydata})



def ComplaintReply(request,id):
    replydata = tbl_complaint.objects.get(id=id)
    companydata=tbl_company.objects.get(id=request.session['cid'])
    if request.method == 'POST':
        reply = request.POST.get('txt_reply')
        replydata.complaint_reply=reply
        replydata.complaint_status=1
        replydata.save()
        return render(request, "Company/ViewComplaints.html", {'msg': "Replied",'companydata': companydata})
    else:
        return render(request, 'Company/ComplaintReply.html', {'replydata': replydata,'companydata':companydata})
    
    

def DeleteComplaint(request,did):
    tbl_complaint.objects.get(id=did).delete()
    companydata = tbl_company.objects.get(id=request.session['cid'])
    return render(request,"Company/Complaint.html",{'msg':"Data Deleted",'companydata': companydata})


def EditComplaint(request,eid):
    editdata=tbl_complaint.objects.get(id=eid)
    complaintdata=tbl_complaint.objects.filter(company=request.session['cid'])
    companydata=tbl_company.objects.get(id=request.session['cid'])
    if request.method=='POST':
        title = request.POST.get('txt_title')
        content = request.POST.get('txt_content')
        editdata.complaint_title=title
        editdata.complaint_content=content
        editdata.save()
        return render(request,"Company/Complaint.html",{'msg':"Data Updated..",'companydata': companydata})
    else:
        return render(request,"Company/Complaint.html",{'editdata':editdata,'complaintdata':complaintdata,'companydata':companydata})


    
def ViewUserComplaint(request, cid):
    if "cid" not in request.session:
        return redirect("Guest:Login")
    else:
        companycomplaintdata = tbl_complaint.objects.filter(companyservice=cid,companyservice__company=request.session['cid']).order_by('-id')
        companydata=tbl_company.objects.get(id=request.session['cid'])
        return render(request,"Company/ViewUserComplaint.html",{'companycomplaintdata': companycomplaintdata,'companydata':companydata})



def UserComplaintReply(request, id):
    replydata = tbl_complaint.objects.get(id=id)
    companydata=tbl_company.objects.get(id=request.session['cid'])
    cid = replydata.companyservice.id

    if request.method == 'POST':
        replydata.complaint_reply = request.POST.get('txt_reply')
        replydata.complaint_status = 1
        replydata.save()

        return render(request,"Company/ViewUserComplaint.html",{'msg': "Reply submitted successfully",'cid': cid,'companydata': companydata})
    else:
        return render(request,'Company/UserComplaintReply.html',{'replydata': replydata,'cid': cid,'companydata':companydata})

    

def ViewLeaveRequest(request):
    if "cid" not in  request.session :
        return redirect("Guest:Login")
    else:
        company= request.session['cid']
        leavedata = tbl_technicianleave.objects.filter(technician__company=company).order_by('-applied_date', '-id')
        companydata=tbl_company.objects.get(id=request.session['cid'])
        return render(request, "Company/ViewLeaveRequest.html", {"leavedata": leavedata,'companydata':companydata})


def AcceptLeave(request, id):
    leavedata = tbl_technicianleave.objects.get(id=id)
    companydata = tbl_company.objects.get(id=request.session['cid'])
    leavedata.leave_status = 1
    leavedata.save()
    return render(request,"Company/ViewLeaveRequest.html",{'msg': "Leave Approved",'companydata': companydata})


def RejectLeave(request, id):
    companydata = tbl_company.objects.get(id=request.session['cid'])
    leavedata = tbl_technicianleave.objects.get(id=id)
    leavedata.leave_status = 2
    leavedata.save()
    return render(request,"Company/ViewLeaveRequest.html",{'msg': "Leave Rejected",'companydata': companydata})


def Logout(request):
      del request.session["cid"]
      return redirect('Guest:Index')


def ViewCompanyServiceRating(request,cid):
    ratingdata=tbl_rating.objects.filter(companyservice=cid).order_by('-datetime','id')
    companydata=tbl_company.objects.get(id=request.session['cid'])
    count=ratingdata.count()
    avg=0
    if count>0:
        total=0
        for i in ratingdata:
            total+=i.rating_data
        avg=total//count
    return render(request,"Company/ViewCompanyServiceRating.html",{'ratingdata':ratingdata,'avg':avg,'count':count,'cid':cid,'companydata':companydata})



def company_revenue_report(request):

    if "cid" not in request.session:
        return redirect("Guest:Login")

    company_id = request.session["cid"]

    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")
    user_name = request.GET.get("user_name", "")

    report = tbl_companyservice.objects.filter(company_id=company_id,companyservice_status=9).select_related("user", "technician").order_by("-companyservice_date", "-id")
    companydata=tbl_company.objects.get(id=request.session['cid'])

    if from_date and to_date:
        report = report.filter(companyservice_date__date__range=[from_date, to_date])

    if user_name:
        report = report.filter(user__user_name__icontains=user_name)

    total_revenue = report.aggregate(total=Sum("companyservice_amount"))["total"] or 0

    total_requests = report.count()
    context = {"report": report,"total_revenue": total_revenue,"total_requests": total_requests,"user_name": user_name,"from_date": from_date,"to_date": to_date,'companydata':companydata}
    
    return render(request, "Company/Report.html", context)