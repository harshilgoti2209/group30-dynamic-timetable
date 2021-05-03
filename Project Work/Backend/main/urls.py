from django.urls import path
from .views import home,login,about,signup,contact,logout,shome,sprofile,seditprofile,viewtimetable,phome,addprof,ahome,changepassword, studentcsv, profcsv ,editnotes
urlpatterns = [
    path('',home,name='home'),   #done
    
    path('login/',login,name='login'),    #done
    path('logout/',logout,name='logout'),  #done
    
    path('about/',about,name='about'),  #done
    path('contact/',contact,name='contact'),  #done
   
    path('shome/',shome,name='shome'),  #done
    path('sprofile/<str:id>',sprofile,name='sprofile'),   #done
    path('seditprofile/<str:id>',seditprofile,name='seditprofile'),   #done
    
    path('viewtimetable/',viewtimetable,name='viewtimetable'),   #done

    path('phome/',phome,name='phome'),  #done

    path('ahome/',ahome,name='ahome'),   #done
    
    path('changepassword/',changepassword,name='changepassword'),   #done
    
    path('signup/',signup,name='signup'),   #done
    path('studentcsv/',studentcsv,name='studentcsv'),  #done 
    path('profcsv/',profcsv,name='profcsv'), #baki
      
    path('addprof/',addprof,name='addprof'),  # baki
    
    path('editnotes/<str:id>/<str:slotid>',editnotes,name='editnotes'),

]
