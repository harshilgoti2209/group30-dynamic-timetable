"""dynamictimetable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import home,login,about,signup,contact,logout,shome,sprofile,seditprofile,viewtimetable,phome,addprof,ahome,changepassword, studentcsv, profcsv
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
    
    path('signup/',signup,name='signup'),   
    path('studentcsv/',studentcsv,name='studentcsv'), 
    path('profcsv/',profcsv,name='profcsv'), 
      
    path('addprof/',addprof,name='addprof'),  # baki
]
