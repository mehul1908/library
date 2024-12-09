from django.shortcuts import render,redirect,get_object_or_404
from . import form , models
from django.views import View
from django.http import HttpResponse,request
from django.contrib.auth import logout
import json
import datetime


# Create your views here.
def home(request):
    return render(request , 'home.html')


class Login(View):
    def get(self , request):

        myform=form.LoginForm()
        return render(request , 'login.html' , {'myform':myform})
    def post(self , request):
        error=False
        errormsg=""
        try:   
            obj=models.User.objects.get(user_id=request.POST['user_id'])
            if obj.pword==request.POST['pword'] and obj.status==1:
                request.session['username']=obj.uName
                request.session['userid']=obj.user_id
                request.session['type']=obj.uType
                return redirect('home')
            else:
                error=True
                errormsg="The User Id and Password is not match !! OR User is not approved , Please Contact Librarian"
                return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':error , 'errormsg':errormsg})
        except:
            error=True
            errormsg="The User id is not available !!"
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':error , 'errormsg':errormsg})

class SignUp(View):
    def get(self,request):
        myform=form.SignUpForm()
        return render(request,'signup.html' , {'myform':myform})    
    def post(self,request):
        myform=form.SignUpForm(request.POST)
        error=False
        errormsg=''
        if myform.is_valid():
            myform.save()
            return redirect('home')
        else:
            error=True
            errormsg=myform.errors
            return render(request,'signup.html',{'myform':form.SignUpForm,'error':error , 'errormsg':errormsg})   

def approvePage(request):
    if (request.session.has_key("type")) and (request.session['type']==1 or request.session['type']==2) :
            data=models.User.objects.filter(status=2)
            return render(request,'approvepage.html',{'mydata':data})
    else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})

def approveUser(request , id):
    if (request.session.has_key("type")) and (request.session['type']==1 or request.session['type']==2):

        try:
            data=get_object_or_404(models.User , user_id=id)
            data.status=1
            data.save()
        finally:
            return redirect('approvepage')
    else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})


def rejectUser(request , id):
    if (request.session.has_key("type")) and (request.session['type']==1 or request.session['type']==2):

        try:
            data=get_object_or_404(models.User , user_id=id)
            data.delete()
        finally:
            return redirect('approvepage')
    else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})

def logouts(request):
    logout(request)
    return redirect('home')

class AddBook(View):
    def get(self,request):
        if (request.session.has_key("type")) and (request.session['type']==1 or request.session['type']==2):
            myform=form.BookForm()
            return render(request,'addbook.html',{'myform':myform})
        else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})

    def post(self,request):
        if (request.session.has_key("type")) and (request.session['type']==1 or request.session['type']==2):

            myform=form.BookForm(request.POST)
            errormsg=''

            try:
                bid=models.Book.objects.all().order_by("-book_id")[0].book_id
            except:
                bid=0
            try:
                obj=models.Book(book_id=bid+1 , bName=request.POST['bName'] , author=request.POST['author'] , publisher=request.POST['publisher'] , category=request.POST['category'] , edition=request.POST['edition'] , count=request.POST['count'])
                if models.Book.objects.filter(bName=request.POST['bName']).filter(author=request.POST['author']).filter(edition=request.POST['edition']).count()!=0:
                        errormsg="The Book is already added with the Same name and Edition"
                        return render(request,'addbook.html',{'myform':form.BookForm(),'error':True , 'errormsg':errormsg})
                else:
                        obj.save()
                        return render(request,'addbook.html',{'myform':form.BookForm(),'result':bid+1})
            except:
                return render(request,'addbook.html',{'myform':form.BookForm(),'error':True , 'errormsg':"Please Enter the Quantity of Books Greater than or Equal to 0"})
        else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})


class ListBook(View):
    def get(self,request):
        data=models.Book.objects.all()
        return render(request,'listbook.html',{'mydata':data})
    def post(self,request):
        temp=request.POST['query']
        data1=models.Book.objects.filter(bName__icontains=temp)
        data2=models.Book.objects.filter(author__icontains=temp)
        data3=models.Book.objects.filter(publisher__icontains=temp)
        data4=models.Book.objects.filter(category__icontains=temp)
        data=(((data1 | data2)|data3)|data4).distinct()
        return render(request , 'listbook.html',{'mydata':data , 'temp':temp} )

class EditBook(View):
    def get(self,request,id):
        if (request.session.has_key("type")) and (request.session['type']==1 or request.session['type']==2):

            data=models.Book.objects.get(book_id=id)
            myform=form.BookForm(instance=data)
            return render(request,'editbook.html',{'myform':myform})
        else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})

    def post(self,request,id):
        if (request.session.has_key("type")) and (request.session['type']==1 or request.session['type']==2):
            data=models.Book.objects.get(book_id=id)
            try:
                obj=models.Book(book_id=data.book_id , bName=request.POST['bName'] , author=request.POST['author'] , publisher=request.POST['publisher'] , category=request.POST['category'] , edition=request.POST['edition'] , count=request.POST['count'])
                obj.save()
                return redirect('listbook')
            except:
                return render(request,'editbook.html',{'myform':form.BookForm(),'error':True , 'errormsg':"Please Enter the Quantity of Books Greater than or Equal to 0"})
        else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})

def delBook(request,id):
    if (request.session.has_key("type")) and (request.session['type']==1 or request.session['type']==2):

        data=models.Book.objects.get(book_id=id)
        data.delete()
        return redirect('listbook')
    else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})


def issueBook(request , id):
    if (request.session.has_key("type")) and (request.session['type']==3 or request.session['type']==4):

        error=False
        errormsg=''
        bk=get_object_or_404(models.Book , book_id=id)
        user=get_object_or_404(models.User , user_id=request.session['userid'])
        data=models.Book.objects.all()
        if bk.count == 0:
            error=True
            errormsg="Book is not available. Please Check Later"
            return render(request,'listbook.html',{'mydata':data,'error':error , 'errormsg':errormsg}) 
        isData=models.IssuedBook.objects.filter(user_id=user)
        if isData.count() == request.session['type']:
            error=True
            errormsg="You reached upto your allowed limits"
            return render(request,'listbook.html',{'mydata':data,'error':error , 'errormsg':errormsg}) 
        try:
            tid=models.Transaction.objects.all().order_by("-trans_id")[0].trans_id
        except:
            tid=0
        trans= models.Transaction(trans_id=tid+1 , user_id=user,book_id=bk , issueDtTm=datetime.datetime.now())
        trans.save()
        ib=models.IssuedBook(trans_id=trans, user_id=user)
        ib.save()
        bk.count = bk.count-1
        bk.save()
        return redirect('listbook')
    else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})


def returnBookPage(request ):
    if (request.session.has_key("type")) :
        if (request.session['type']==3 or request.session['type']==4):
            user=get_object_or_404(models.User , user_id=request.session['userid'])
            data=models.IssuedBook.objects.filter(user_id=user)
            return render(request,'returnbook.html' , {'mydata':data})
        else:
            data=models.IssuedBook.objects.all()
            return render(request,'returnbook.html' , {'mydata':data})
    else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})

    

def returnBook(request , id):
    if (request.session.has_key("type")) and (request.session['type']==3 or request.session['type']==4):

        trans=get_object_or_404(models.Transaction , trans_id=id)
        trans.book_id.count+=1
        trans.book_id.save()
        print(trans)
        bk=get_object_or_404(models.IssuedBook , trans_id=trans)
        bk.delete()
        trans.returnDtTm=datetime.datetime.now()
        trans.save()
        
        return redirect('returnbookpage')
    else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})


def userlist(request):
    if (request.session.has_key("type")) and (request.session['type']==1 or request.session['type']==2):
        data=models.User.objects.exclude(user_id='headlib')
        return render(request , 'userlist.html' , {'mydata':data})
    else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})


class EditUser(View):
    def get(self,request,id):
        if (request.session.has_key("type")) and (request.session['type'] in (1,2,3,4)):

            data=models.User.objects.get(user_id=id)
            myform=form.SignUpForm(instance=data)
            return render(request,'edituser.html',{'myform':myform})
        else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})

    def post(self,request,id):
        if  (request.session.has_key("type")) and (request.session['type'] in (1,2,3,4)):

            data=models.User.objects.get(user_id=id)
            obj=models.User(user_id=data.user_id , uName=request.POST['uName'] , pword=request.POST['pword'] , uType=request.POST['uType'] , status=data.status)
            obj.save()
            return redirect('userlist')
        else:
            return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})

        

def delUser(request , id):
    if (request.session.has_key("type")) and (request.session['type'] in (1,2,3,4)):
        data=models.User.objects.get(user_id=id)
        data.delete()
        if request.session['type'] in (1,2):
            return redirect('userlist')
        else:
            return redirect('logouts')
    else:
        return render(request , 'login.html' , {'myform':form.LoginForm() , 'error':True , 'errormsg':"Please Login with correct crendentials"})

from django.conf import settings
from django.core.mail import send_mail


def sendMail(request):
    username="mehul"
    subject = 'welcome to GFG world'
    message = f'Hi {username}, thank you for registering in geeksforgeeks.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["vijayvargiyamehul@mail.com", ]
    send_mail( subject, message, email_from, recipient_list )
    return HttpResponse("Email sent Successfully")
