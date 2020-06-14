from django.core.mail import send_mail
from django.shortcuts import render,redirect
import requests
from .forms import VoucherCreation,SocietyCreation,mailback
from shop.models import ContactUs,Supplier,Voucher,Society,Product,Order
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from email.message import EmailMessage
import smtplib
from .models import adminmodel,addproductlist,delete_product_list
from django.conf import settings

# Create your views here.

def homepage(request):
    # currentuser = request.COOKIES['username']

    return render(request,'admin/dash.html',)


# def login(request):
#     # print(request.method)
#     print('login')
#     if request.method=='GET':
#         print('login GET')
#         forminput=loginform()
#         return render(request,'adminlogin.html',{'forminput':forminput})
#     elif request.method=='POST':
#         currentuser=""
#         print('login POST')
#         forminput=loginform(request.POST)
#         if forminput.is_valid():
#             username=forminput.cleaned_data['username']
#             password=forminput.cleaned_data['password']
#         print(username)
#         print(password)
#         try:
#
#             admindata=adminmodel.objects.get(username=username)
#             # print(admindata.username)
#             # print(admindata.password)
#             # print(admindata.password==password)
#             if admindata.password==password:
#                     # print('yes')
#                     currentuser=admindata.username
#                     # return HttpResponse('yes')
#                     name='admindash.html'
#             else:
#                 name='adminlogin.html'
#                     # return render(request,'admindash.html',{'currentuser':currentuser})
#
#         except :
#             name='adminlogin.html'
#             message='Username or Password was incorrect'
#
#         message='Username or Password was incorrect'
#         # print(name)
#         # return HttpResponse(message)
#         # return render(request,'adminlogin.html',{'forminput':forminput,'message':message})
        # response=render(request,name,{'forminput':forminput,'message':message,'currentuser':currentuser})
        # response.set_cookie('username',username)
        # return response
        # return render(request,name,{'forminput':forminput,'message':message,'currentuser':currentuser})

def societieslist(request):
    print('societieslist')
    societiesdata=Society.objects.all()
    return render(request,'admin/societieslist.html',{'societiesdata':societiesdata})
def vouchers(request):
    print('vouchers')
    return render(request,'admin/vouchers.html')



def viewsocieties(request):
    print('viewsocieties')
    socdata=Society.objects.all()
    # for i in voucherdata:
    #     print(i.voucher_code)
    return render(request,'admin/viewsocieties.html',{'socdata':socdata})

def createsocieties(request):
    print('createsocieties')
    if request.method=='GET':

        societyform=SocietyCreation()

        return render(request,'admin/createsocieties.html',{'societyform':societyform})
    else:
        societyform=SocietyCreation(request.POST)
        if societyform.is_valid():
            society_name=societyform.cleaned_data['society_name']
            society_address=societyform.cleaned_data['society_address']
            society_locality=societyform.cleaned_data['society_locality']
            socdata=Society()

            socdata.society_name=society_name
            socdata.society_address=society_address
            socdata.society_locality=society_locality

            socdata.save()

            messages.info(request,'Society created successfully!')
        else:
            messages.info(request,'Something went wrong')


        societyform=SocietyCreation()
        return render(request,'admin/createsocieties.html',{'societyform':societyform})

def deletesocieties(request):
    if request.method=='GET':
        print('deletesocieties')
        socdata=Society.objects.all()
        return render(request,'admin/deletesocieties.html',{'socdata':socdata})
    else:
        socdata=Society.objects.get(id=int(request.POST['clicked'])).delete()
        socdata=Society.objects.all()
        return render(request,'admin/deletesocieties.html',{'socdata':socdata})


def updatesocieties(request):
    if request.method=='GET':
        print('updatesocieties')
        socdata=Society.objects.all()
        return render(request,'admin/updatesocieties.html',{'socdata':socdata})

    elif request.method=='POST' and 'clicked' in request.POST:
        orgdata=Society.objects.get(id=int(request.POST['clicked']))

        societyform=SocietyCreation(initial={'society_name': orgdata.society_name,'society_locality':orgdata.society_locality,'society_address':orgdata.society_address})
        # x=User.objects.get(username=data.username)
        # y=Supplier.objects.get(supplier_details=x)
        # addproductlist.objects.get(id=request.POST['clicked']).delete()
        # for i in orgdata.society.all():
        #     print(i.society_name)
        return render(request,'admin/updatesocieties2.html',{'orgdata':orgdata,'societyform':societyform})

    elif request.method=='POST' and 'update' in request.POST:
        societyform=SocietyCreation(request.POST)
        orgdata=Society.objects.get(id=int(request.POST['update'])).delete()
        if societyform.is_valid():

            society_name=societyform.cleaned_data['society_name']
            society_address=societyform.cleaned_data['society_address']
            society_locality=societyform.cleaned_data['society_locality']
            socdata=Society()

            socdata.society_name=society_name
            socdata.society_address=society_address
            socdata.society_locality=society_locality

            socdata.save()

        socdata=Society.objects.all()
        message='Voucher Updated Successfully'
        return render(request,'admin/updatesocieties.html',{'socdata':socdata,'message':message})

def viewvoucher(request):
    print('viewvoucher')
    voucherdata=Voucher.objects.all()
    # for i in voucherdata:
    #     print(i.voucher_code)
    return render(request,'admin/viewvoucher.html',{'voucherdata':voucherdata})

def createvoucher(request):
    print('createvoucher')
    if request.method=='GET':

        voucherform=VoucherCreation()

        return render(request,'admin/createvoucher.html',{'voucherform':voucherform})
    else:
        voucherform=VoucherCreation(request.POST)
        if voucherform.is_valid():
            voucher_code=voucherform.cleaned_data['voucher_code']
            voucher_value=voucherform.cleaned_data['voucher_value']
            chosensociety=voucherform.cleaned_data['society']
            voucherdata=Voucher()


            voucherdata.voucher_code=voucher_code
            voucherdata.voucher_value=voucher_value
            voucherdata.save()
            for i in chosensociety:
                societydata=Society.objects.get(society_name=i.society_name)
                voucherdata.society.add(societydata)
            voucherdata.save()

            messages.info(request,'Voucher created successfully!')
        else:
            messages.info(request,'Something went wrong')



        return render(request,'admin/createvoucher.html',{'voucherform':voucherform})

def deletevoucher(request):
    if request.method=='GET':
        print('deletevoucher')
        voucherdata=Voucher.objects.all()
        return render(request,'admin/deletevoucher.html',{'voucherdata':voucherdata})
    else:
        voucherdata=Voucher.objects.get(id=int(request.POST['clicked'])).delete()
        voucherdata=Voucher.objects.all()
        return render(request,'admin/deletevoucher.html',{'voucherdata':voucherdata})


def updatevoucher(request):
    if request.method=='GET':
        print('updatevoucher')
        voucherdata=Voucher.objects.all()
        return render(request,'admin/updatevoucher.html',{'voucherdata':voucherdata})

    elif request.method=='POST' and 'clicked' in request.POST:
        orgdata=Voucher.objects.get(id=int(request.POST['clicked']))

        voucherform=VoucherCreation(initial={'voucher_code': orgdata.voucher_code,'voucher_value':orgdata.voucher_value})
        # x=User.objects.get(username=data.username)
        # y=Supplier.objects.get(supplier_details=x)
        # addproductlist.objects.get(id=request.POST['clicked']).delete()
        for i in orgdata.society.all():
            print(i.society_name)
        return render(request,'admin/updatevoucher2.html',{'orgdata':orgdata,'voucherform':voucherform})

    elif request.method=='POST' and 'update' in request.POST:
        voucherform=VoucherCreation(request.POST)
        orgdata=Voucher.objects.get(id=int(request.POST['update'])).delete()
        if voucherform.is_valid():
            voucher_code=voucherform.cleaned_data['voucher_code']
            voucher_value=voucherform.cleaned_data['voucher_value']
            chosensociety=voucherform.cleaned_data['society']
            voucherdata=Voucher()

            voucherdata.voucher_code=voucher_code
            voucherdata.voucher_value=voucher_value
            voucherdata.save()
            for i in chosensociety:
                societydata=Society.objects.get(society_name=i.society_name)
                voucherdata.society.add(societydata)
            voucherdata.save()
        voucherdata=Voucher.objects.all()
        message='Voucher Updated Successfully'
        return render(request,'admin/updatevoucher.html',{'voucherdata':voucherdata,'message':message})


def supplierslist(request):
    print('supplierslist')
    # currentuser = request.COOKIES['username']
    suppdata=Supplier.objects.all()
    # print(type(suppdata))
    return render(request,'admin/supplierslist.html',{'suppdata':suppdata})

def requestslist(request):

    print('requestslist')
    return render(request,'admin/requestslist.html',{})


def complaintslist(request):
    # currentuser = request.COOKIES['username']
    if request.method=='GET':
        complaintdata=ContactUs.objects.filter(is_addressed=False)

        print('complaintslist')
        return render(request,'admin/complaintslist.html',{'complaintdata':complaintdata})
    elif request.method=='POST' and 'clicked' in request.POST:
        orgdata=ContactUs.objects.get(id=int(request.POST['clicked']))
        mailform=mailback()
        return render(request,'admin/sendmail.html',{'mailform':mailform,'orgdata':orgdata})

    elif request.method=='POST' and 'send' in request.POST:
        orgdata=ContactUs.objects.get(id=int(request.POST['send']))
        mailform=mailback(request.POST)
        msg=""
        if mailform.is_valid():
            msg=mailform.cleaned_data['message']

            DEFAULT_FROM_EMAIL='raoashish1008@gmail.com'
            password='vegefoods1234'

            subject='Re: '+str(orgdata.subject)
            body=orgdata.message
            msg= f'Subject: {subject}\n\n{body}'
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(DEFAULT_FROM_EMAIL,password)
            server.sendmail(DEFAULT_FROM_EMAIL,orgdata.email,msg)
            server.quit()

        complaintdata=ContactUs.objects.filter(is_addressed=False)
        orgdata.is_addressed=True
        orgdata.save()
        return render(request,'admin/complaintslist.html',{'complaintdata':complaintdata})

def refundslist(request):
    # currentuser = request.COOKIES['username']

    print('refundslist')
    return render(request,'admin/refundslist.html',)

def orderslist(request):
    print('orderslist')
    # currentuser = request.COOKIES['username']

    orderdata=Order.objects.filter(is_completed=False)
    print(type(orderdata))
    return render(request,'admin/orderslist.html',{'orderdata':orderdata})

def approvallist(request):
    if request.method=='GET':
        print('approvallist')
        # currentuser = request.COOKIES['username']

        approvaldata=Supplier.objects.filter(is_approved=False)
        print(approvaldata)
        return render(request,'admin/approvallist.html',{'approvaldata':approvaldata})
    else:
        orgdata=Supplier.objects.get(id=int(request.POST['clicked']))
        orgdata.is_approved=True
        orgdata.save()
        approvaldata=Supplier.objects.filter(is_approved=False)
        message='Supplier Approved Successfully'
        return render(request,'admin/approvallist.html',{'approvaldata':approvaldata,'message':message})

def deleteproduct(request):
    if request.method=='GET':
        print('deleteproduct')
        # currentuser = request.COOKIES['username']
        deleteproddata=delete_product_list.objects.filter(is_approved=False)
        return render(request,'admin/deleteproduct.html',{'deleteproddata':deleteproddata})
    else:
        orgdata=delete_product_list.objects.get(id=int(request.POST['clicked']))
        orgdata.is_approved=True
        orgdata.save()
        approvaldata=Supplier.objects.filter(is_approved=False)
        message='Delete Product request Approved Successfully'
        return render(request,'admin/deleteproduct.html',{'approvaldata':approvaldata,'message':message})

def newproduct(request):
    if request.method=='GET':
        print('newproduct')
        # currentuser = request.COOKIES['username']
        addproddata=addproductlist.objects.filter(is_approved=False)
        return render(request,'admin/newproduct.html',{'addproddata':addproddata})
    elif request.method=='POST':

        data=addproductlist.objects.get(id=int(request.POST['clicked']))
        # x=User.objects.get(username=data.username)
        # y=Supplier.objects.get(supplier_details=x)
        # addproductlist.objects.get(id=request.POST['clicked']).delete()
        # addproductdata=Product.objects.create(product_name=data.product_name,product_description=data.product_description,product_sku=data.product_sku,product_price=data.product_price,
        #                                         category="Not Added!",supplier=x)
        data.is_approved=True
        data.save()
        addproddata=addproductlist.objects.filter(is_approved=False)
        return render(request,'admin/newproduct.html',{'addproddata':addproddata})
def logout(request):

    response= redirect('/office',{'message':'You have successfully logged out'})
    response.delete_cookie('username')
    return response
