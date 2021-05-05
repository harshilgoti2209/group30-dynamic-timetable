from django.shortcuts import render,redirect
from django.contrib.auth import logout as logout_,login as login_,authenticate,update_session_auth_hash
from .forms import UserSignUpForm,profileform,ProfSignUpForm,Editnotes
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib import messages
from .models import Account,Notes,Algo
from django.contrib.auth.hashers import make_password
from .forms import loginForm
import csv,io
from .timetable_generator_V2 import *

##working 
def home(request):
    return render(request,'main/home.html')

##working
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
            fm=loginForm(request=request,data=request.POST)
            if fm.is_valid():
                email=fm.cleaned_data['username']
                password=fm.cleaned_data['password']
                user=authenticate(email=email,password=password)
                if user is not None:
                    login_(request,user)
                    return redirect('login')
        else:
            fm=loginForm()
        return render(request,'main/login.html',{'form':fm})

##working
def logout(request):
    logout_(request)
    return redirect('login')

##working
def gtimetable(request):
    if request.method=='POST':
        csv_file=request.FILES['data']  
        cube, genes =timetable( csv_file)  
        for i in range(cube.shape[1]):
            for j in range(cube.shape[2]):
                for k in range(cube.shape[0]) : 
                    if(cube[k,i,j] != -1) : 
                        obj=Algo( slot_id=genes[cube[k,i,j]].slot_id, prof_name=genes[cube[k,i,j]].prof_name,prof_id=genes[cube[k,i,j]].prof_id,subject=genes[cube[k,i,j]].subject,subject_id=genes[cube[k,i,j]].subject_id,batch=genes[cube[k,i,j]].batch,batch_id=genes[cube[k,i,j]].batch_id, day=j,time=i )
                        obj.save() 
        return redirect('login')
    else:
        return redirect('login')

##working
def shome(request):
    if request.user.is_authenticated and request.user.is_prof==False and request.user.is_superuser==False:
        account=Account.objects.get(pk=request.user.id)
        pform=profileform(instance=request.user)
        dic={}
        lis=[]
        for i in range(0,4):
            li=[]
            for j in range(0,6):
                li.append(dic)
            lis.append(li)
        timetable=Algo.objects.filter(batch_id=account.batch-1)
        for item in timetable:
            lis[item.time][item.day]={
                'prof':item.prof_name,
                'subject':item.subject,
            }
        return render(request,'main/shome.html' ,{'data':account,'pform': pform,'timetable':lis})
    else:
        return redirect('login')  

##working
def seditprofile(request):
    if not request.user.is_authenticated: 
        messages.info(request,'You can not edit someone profile')
        return redirect('login')
    else:
        account=Account.objects.get(pk=request.user.id)
        if request.method=="POST":
            fm=profileform(request.POST, instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request,'Your profile is edited successfully!!!')
                return redirect('login')
            messages.info(request,f'username or email is already exist')
            return redirect('login')  

# def sprofile(request,id):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     else:
#         account=Account.objects.get(pk=id)
#         return render(request,'main/sprofile.html',{'user':account})

def viewtimetable(request):
    if request.user.is_authenticated:
        return render(request,'main/viewtimetable.html',{'data':None})
    else:
        return redirect('login')

def changeslot(request,batch):
    if request.user.is_prof:
        dic=0
        lis=[]
        for i in range(0,4):
            li=[]
            for j in range(0,6):
                li.append(dic)
            lis.append(li)
        timetable=Algo.objects.filter(prof_id=66)
        for item in timetable:
            lis[item.time][item.day]=1
        timetable=Algo.objects.filter(batch=batch)
        for item in timetable:
            lis[item.time][item.day]=1
        available=[]
        for i in range(0,4):
            for j in range(0,6):
                if lis[i][j]==0:
                    available.append({
                        'time':i,
                        'day':j,
                    })
        if available.count==0:
            return redirect('phome')
        else:
            return render(request,'main/available.html',{'available':available})
    else:
        return redirect('login')

def phome(request):
    if request.user.is_prof:
        dic={}
        lis=[]
        for i in range(0,4):
            li=[]
            for j in range(0,6):
                li.append(dic)
            lis.append(li)
        timetable=Algo.objects.filter(prof_id=66)
        for item in timetable:
            lis[item.time][item.day]={
                'batch':item.batch,
                'subject':item.subject,
            }
        return render(request,'main/phome.html',{'timetable':lis})
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
        return redirect('login')   



# def profcsv(request):
#     if request.method == 'POST':
#         for key,value in request.FILES:
#             print(key)
#         # doc = request.FILES #returns a dict-like object
#         # doc_name = doc['filename']
#         print('hello')
#         return redirect('login')
#     else:
#         return redirect('login') 
              
def addprof(request):
    if  request.user.is_superuser==True:
        if request.method=="POST":
            fm=ProfSignUpForm(request.POST)
            if fm.is_valid():
                name=fm.cleaned_data['username']
                password=fm.cleaned_data['password1']
                email=fm.cleaned_data['email']
                password=make_password(password)
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
