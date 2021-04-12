from django.shortcuts import render,redirect
from django.contrib.auth import logout as logout_,login as login_,authenticate,update_session_auth_hash
from .forms import UserSignUpForm,profileform,ProfSignUpForm,Editnotes
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib import messages
from .models import Account,Notes
import csv,io

def home(request):
    return render(request,'main/home.html')

def login(request):
    if request.user.is_authenticated:
        if request.user.is_prof:
            return redirect('phome')  
        elif request.user.is_superuser:
            return redirect('ahome')
        else:
            return redirect('shome') 
    else:
        if request.method=='POST':
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                email=fm.cleaned_data['username']
                password=fm.cleaned_data['password']
                user=authenticate(email=email,password=password)
                if user is not None:
                    login_(request,user)
                    messages.success(request,'welcome!!!')
                    return redirect('login')
        else:
            fm=AuthenticationForm()
        return render(request,'main/login.html',{'form':fm})

def logout(request):
    logout_(request)
    return redirect('login')

def about(request):
    return render(request,'main/about.html')

def contact(request):
    return render(request,'main/contact.html')

def shome(request):
    if request.user.is_authenticated and request.user.is_prof==False and request.user.is_superuser==False:
        username=request.user.username
        return render(request,'main/shome.html' ,{'username':username})
    else:
        return redirect('login')    

def sprofile(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        account=Account.objects.get(pk=id)
        return render(request,'main/sprofile.html',{'user':account})

def seditprofile(request,id):
    if not request.user.is_authenticated or id!=str(request.user.id):
        messages.info(request,'You can not edit someone profile')
        return redirect('login')
    else:
        account=Account.objects.get(pk=request.user.id)
        if request.method=="POST":
            fm=profileform(request.POST, instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request,'Your profile is edited successfully!!!')
                return redirect('sprofile', id)
        else:
            fm=profileform( instance=request.user )
        return render(request,'main/seditprofile.html',{'form':fm})

def viewtimetable(request):
    if request.user.is_authenticated:
        return render(request,'main/viewtimetable.html',{'data':None})
    else:
        return redirect('login')

def phome(request):
    if request.user.is_prof:
        return render(request,'main/phome.html')
    else:
        return redirect('login')

def ahome(request):
    if request.user.is_superuser:
        return render(request,'main/ahome.html')
    else:
        return redirect('login')

def changepassword(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request=request,user=request.user)
                return redirect('login')
        else:
            fm=PasswordChangeForm(user=request.user)
        return render(request,'main/changepassword.html',{'form':fm})
    else:
        return redirect('login')

def signup(request):
    if request.user.is_superuser==True:
        if request.method=="POST":
            fm=UserSignUpForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,'success!!!')
        else:
            fm=UserSignUpForm()
        return render(request,'main/signup.html',{'form':fm})
    else:
        return redirect('login')   # a change karwanu che

def studentcsv(request):
    if request.method=='POST':
        csv_file=request.FILES['data']   #csv file read code
        data_set = csv_file.read().decode('UTF-8')
        io_string=io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            x=Account.objects.filter(username=column[0])
            y=Account.objects.filter(email=column[1])
            if x.count() > 0 or y.count()>0 :
                messages.info(request,f'{column[0]} username or {column[1]} email is already exist') 
            else:
                fm=Account(username=column[0], email=column[1] , password=column[2] , batch=column[3])
                fm.save() 
        messages.info(request,'success')
        return redirect('signup')
    else:
        return redirect('login')

def profcsv(request):
    if request.method=='POST':
        data=request.POST.get('file')  #csv file read code
        messages.info(request,'success')
        return redirect('addprof')
    else:
        return redirect('login') 
              
def addprof(request):
    if  request.user.is_superuser==True:
        if request.method=="POST":
            fm=ProfSignUpForm(request.POST)
            if fm.is_valid():
                name=fm.cleaned_data['username']
                password=fm.cleaned_data['password1']
                email=fm.cleaned_data['email']
                prof=Account(username=name,password=password,email=email,is_prof=True)
                prof.save()
                messages.success(request,'success!!!')
                fm=ProfSignUpForm()
        else:
            fm=ProfSignUpForm()
        return render(request,'main/profsignup.html',{'form':fm})
    else:
        return redirect('login')

def editnotes(request,id,slotid):
    if not request.user.is_authenticated or id!=str(request.user.id):
        messages.info(request,"You can not edit/view someone's notes")
        return redirect('login')
    else:
        account=Notes.objects.filter(userid=id,slotid=slotid)
        if account.count()==0:
            ob=Notes(userid=id, slotid=slotid, notes='')
            ob.save()
        account=Notes.objects.get(userid=id,slotid=slotid)
        if request.method=="POST":
            fm=Editnotes(request.POST, instance=account)
            if fm.is_valid():
                data=fm.cleaned_data['notes']
                note=Notes(id=account.id,userid=id,slotid=slotid,notes=data) 
                note.save()
                messages.success(request,'Your Notes is edited successfully!!!')
                return redirect('viewtimetable')
        else:
            fm=Editnotes( instance=account)
        return render(request,'main/editnotes.html',{'form':fm})



        