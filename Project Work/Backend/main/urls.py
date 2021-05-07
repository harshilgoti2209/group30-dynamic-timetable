from django.urls import path
from .views import * 
urlpatterns = [
    path('',home,name='home'),
    path('login/',login,name='login'),    
    path('logout/',logout,name='logout'), 
    path('shome/',shome,name='shome'),  
    path('seditprofile/',seditprofile,name='seditprofile'),   
    path('peditprofile/',peditprofile,name='peditprofile'),   
    path('phome/',phome,name='phome'),  
    path('ahome/',ahome,name='ahome'),  
    path('pprofile/<str:prof_id>',pprofile,name='pprofile'),  
    path('changepassword/',changepassword,name='changepassword'), 
    path('signup/',signup,name='signup'),   
    path('gtimetable/',gtimetable,name='gtimetable'),   
    path('studentcsv/',studentcsv,name='studentcsv'),  
    path('editnotes/<str:slotid>',editnotes,name='editnotes'),
    path('changeslot/<str:slot>',changeslot,name='changeslot'),
    path('finalchangeslot/<str:slot>/<str:time>/<str:day>',finalchangeslot,name='finalchangeslot'),
]
