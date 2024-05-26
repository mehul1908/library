from django.contrib import admin
from django.urls import path 
from . import views
urlpatterns = [
    path('' , views.home , name='home' ),
    path('login' , views.Login.as_view() , name='login'),
    path('signup' , views.SignUp.as_view() , name='signup'),
    path('approvepage',views.approvePage,name='approvepage'),
    path('approveuser/<str:id>',views.approveUser,name='approveuser'),
    path('rejectuser/<str:id>',views.rejectUser,name='rejectuser'),
    path('logouts',views.logouts , name='logouts'),
    path('addbook',views.AddBook.as_view(),name='addbook'),
    path('listbook',views.ListBook.as_view(),name='listbook'),
    path('editbook/<int:id>',views.EditBook.as_view(),name='editbook'),
    path('delbook/<int:id>',views.delBook,name='delbook'),
    path('issuebook/<int:id>' , views.issueBook , name='issuebook'),
    path('returnbookpage' , views.returnBookPage , name='returnbookpage'),
    path('returnbook/<int:id>' , views.returnBook , name='returnbook'),
    path('userlist' , views.userlist , name='userlist'),
    path('edituser/<str:id>' , views.EditUser.as_view() , name='edituser'),
    path('deluser/<str:id>' , views.delUser , name='deluser')

]