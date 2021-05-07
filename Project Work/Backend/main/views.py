from django.shortcuts import render,redirect
from django.contrib.auth import logout as logout_,login as login_,authenticate,update_session_auth_hash
from .forms import UserSignUpForm,profileform,ProfSignUpForm,Editnotes
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib import messages
from .models import Account,Notes,Algo
from django.contrib.auth.hashers import make_password
from .forms import loginForm,profform,changePasswordForm
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
                'Prof':item.prof_id,
                'subject':item.subject,
                'slot':item.slot_id,
            }
        return render(request,'main/shome.html', {'data':account,'pform': pform,'timetable':lis})
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

def phome(request):
    if request.user.is_prof:
        account=Account.objects.get(pk=request.user.id)
        pform=profform (instance=request.user)
        dic={}
        lis=[]
        for i in range(0,4):
            li=[]
            for j in range(0,6):
                li.append(dic)
            lis.append(li)
        sub=[]
        timetable=Algo.objects.filter(prof_id=request.user.batch)
        for item in timetable:
            lis[item.time][item.day]={
                'batch':item.batch,
                'subject':item.subject,
                'slot':item.slot_id,
            }
            if item.subject not in sub:
                sub.append(item.subject)
        return render(request,'main/phome.html',{'data':account,'pform': pform,'timetable':lis,'subject':sub})
    else:
        return redirect('login')

def peditprofile(request):
    if not request.user.is_prof: 
        messages.info(request,'You can not edit someone profile')
        return redirect('login')
    else:
        if request.method=="POST":
            fm=profform(request.POST, instance=request.user)
            if fm.is_valid():
                Algo.objects.filter(prof_id=request.user.batch).update(prof_name=request.POST['username'],email=request.POST['email'])
                fm.save()
                messages.success(request,'Your profile is edited successfully!!!')
                return redirect('login')
            messages.info(request,f'username or email is already exist')
            return redirect('login')  
        else:
            return redirect('login')

def changeslot(request,slot):
    if request.user.is_prof:
        dic=0
        lis=[]
        for i in range(0,4):
            li=[]
            for j in range(0,6):
                li.append(dic)
            lis.append(li)
        timetable=Algo.objects.filter(prof_id=request.user.batch)
        for item in timetable:
            lis[item.time][item.day]=1
        batch=Algo.objects.get(slot_id=int(slot)).batch
        timetable=Algo.objects.filter(batch=batch)
        for item in timetable:
            lis[item.time][item.day]=1
        available=[]
        def fun(i):
            if i==0:
                return 'Slot-1'
            elif i==1:
                return 'Slot-2'
            elif i==2:
                return 'Slot-3'
            else:
                return 'Slot-4'
        def fun2(i):
            if i==0:
                return 'Monday'
            elif i==1:
                return 'Tuesday'
            elif i==2:
                return 'Wednesday'
            elif i==3:
                return 'Thursday'
            elif i==4:
                return 'Friday'
            else:
                return 'Saturday'

        for i in range(0,4):
            for j in range(0,6):
                if lis[i][j]==0:
                    available.append({
                        'time':i,
                        'day':j,
                        'Time':fun(i),
                        'Day':fun2(j),
                    })
        if available.count==0:
            return redirect('phome')
        else:
            return render(request,'main/available.html',{'available':available,'slot':slot})
    else:
        return redirect('login')

def finalchangeslot(request,slot,time,day):
    if request.user.is_prof:
        obj=Algo.objects.get(slot_id=int(slot))
        obj.time=int(time)
        obj.day=int(day)
        obj.save()
        return redirect('login')
    else:
        return redirect('login')   


def ahome(request):
    if request.user.is_superuser:
        final=[]
        for k in range(0,24):
            dic={}
            lis=[]
            for i in range(0,4):
                li=[]
                for j in range(0,6):
                    li.append(dic)
                lis.append(li)
            final.append(lis)
        timetable=Algo.objects.filter()
        for item in timetable:
            final[item.batch_id][item.time][item.day]={
                'subject':item.subject,
                'prof':item.prof_name,
            }
        form2=UserSignUpForm()
        return render(request,'main/ahome.html',{'timetable':final,'fm2':form2})
    else:
        return redirect('login')

##working
def signup(request):
    if request.user.is_superuser==True:
        if request.method=="POST":
            fm=UserSignUpForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,'success!!!')
        else:
            fm=UserSignUpForm()
        return redirect('login')
    else:
        return redirect('login')   

##working
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
                password=make_password(column[2])
                fm=Account(username=column[0], email=column[1] , password=password , batch=column[3])
                fm.save() 
        # messages.info(request,'success')
        return redirect('login')
    else:
        return redirect('login')

##working
def gtimetable(request):
    if request.method=='POST':
        obj=Algo.objects.all()
        lis=[]
        obj.delete()
        obj=Account.objects.filter(is_prof=True)
        obj.delete()
        csv_file=request.FILES['data']  
        cube, genes =timetable( csv_file)  
        for i in range(cube.shape[1]):
            for j in range(cube.shape[2]):
                for k in range(cube.shape[0]) : 
                    if(cube[k,i,j] != -1) : 
                        obj=Algo( slot_id=genes[cube[k,i,j]].slot_id,email=genes[cube[k,i,j]].email, prof_name=genes[cube[k,i,j]].prof_name,prof_id=genes[cube[k,i,j]].prof_id,subject=genes[cube[k,i,j]].subject,subject_id=genes[cube[k,i,j]].subject_id,batch=genes[cube[k,i,j]].batch,batch_id=genes[cube[k,i,j]].batch_id, day=j,time=i )
                        obj.save()
                        if Account.objects.filter(email=genes[cube[k,i,j]].email).count()==0:
                            ob=Account(username= genes[cube[k,i,j]].prof_name,email=genes[cube[k,i,j]].email,password=make_password('qwer@123'),is_prof=True, batch=genes[cube[k,i,j]].prof_id)
                            ob.save()
        return redirect('login')
    else:
        return redirect('login')

def editnotes(request,slotid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        account=Notes.objects.filter(userid=request.user.id,slotid=slotid)
        if account.count()==0:
            ob=Notes(userid=request.user.id, slotid=slotid, notes='')
            ob.save()
        account=Notes.objects.get(userid=request.user.id,slotid=slotid)
        if request.method=="POST":
            fm=Editnotes(request.POST, instance=account)
            if fm.is_valid():
                data=fm.cleaned_data['notes']
                note=Notes(id=account.id,userid=request.user.id,slotid=slotid,notes=data) 
                note.save()
                messages.success(request,'Your Notes is edited successfully!!!')
                return redirect('login')
        else:
            fm=Editnotes( instance=account)
        return render(request,'main/editnotes.html',{'form':fm})

def changepassword(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=changePasswordForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request=request,user=request.user)
                return redirect('login')
        else:
            fm=changePasswordForm(user=request.user)
        return render(request,'main/changepassword.html',{'form':fm})
    else:
        return redirect('login')

def pprofile(request,prof_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        account=Account.objects.get(batch=int(prof_id))
        dic={}
        lis=[]
        for i in range(0,4):
            li=[]
            for j in range(0,6):
                li.append(dic)
            lis.append(li)
        sub=[]
        timetable=Algo.objects.filter(prof_id=account.batch)
        for item in timetable:
            lis[item.time][item.day]={
                'batch':item.batch,
                'subject':item.subject,
                'slot':item.slot_id,
            }
            if item.subject not in sub:
                sub.append(item.subject)
        return render(request,'main/pprofile.html',{'data':account,'subject':sub})
 


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
    pass
    # if  request.user.is_superuser==True:
    #     if request.method=="POST":
    #         fm=ProfSignUpForm(request.POST)
    #         if fm.is_valid():
    #             name=fm.cleaned_data['username']
    #             password=fm.cleaned_data['password1']
    #             email=fm.cleaned_data['email']
    #             password=make_password(password)
    #             prof=Account(username=name,password=password,email=email,is_prof=True)
    #             prof.save()
    #             messages.success(request,'success!!!')
    #             fm=ProfSignUpForm()
    #     else:
    #         fm=ProfSignUpForm()
    #     return render(request,'main/profsignup.html',{'form':fm})
    # else:
    #     return redirect('login')


