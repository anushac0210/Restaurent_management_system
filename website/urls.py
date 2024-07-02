from django.urls import path
from . import views
from .views import customer_add

urlpatterns = [
    # path('wbsite/', views.homepage, name='homepage'),
    path('', views.homepage, name='homepage'),
    path('website/', views.website, name='index'),
    
    path('website/menu/',views.menu,name='menu'),
    path('website/chef/',views.chef,name='chef'),
    path('website/chef_login/chef/<int:id>/', views.chef, name='chef'),
    path('website/chef_login/chef/<int:id>/chef_serve/<int:sno>/', views.chef_serve, name='chef_serve'),
    path('website/customer/',views.customer,name='customer'),
    path('website/dining_supervisor/',views.dining_supervisor,name='dining_supervisor'),
    path('website/dining_supervisor/bill_calculation/',views.bill_calculation,name='bill_calculation'),
    path('website/dining_supervisor/bill_calculation/display_bill/',views.display_bill,name='display_bill'),
    path('website/dining_supervisor/enter_customer/customer_add/',views.customer_add,name='customer_add'),
    path('website/dining_supervisor/enter_customer/',views.enter_customer,name='enter_customer'),
    # hk
    path('website/manager_login/',views.manager_login,name='loginpage'),
    path('website/chef_login/',views.chef_login,name='loginpage'),
    path('website/server/',views.server,name='server'),
    path('website/server/chef_food',views.chef_food,name='chef_food'),
    path('website/server/enter_order/',views.enter_order,name='enter_order'),
    path('website/server/enter_order/insert_oi/',views.insert_oi,name='insert_oi'),
    path('website/dining_supervisor_login/',views.dining_supervisor_login,name='loginpage'),

    # path("/", views.insertcust, name="insertcust"),
    # path("<int:members><int:cust_id>/", views.allocatingtable, name="allocatingtable"),
    # path("<int:oid><int:foodid><int:quan>/", views.insertingintoorderitems, name="insertingintoorderitems"),
    # path("<int:sno>/", views.chefdone, name="chefdone"),
    # path("<int:cust_id><string:pm>/", views.billing, name="billing"),
    # path("<int:billno>/", views.displaybill, name="displaybill"),
    path('website/manager_login/view_all_employees/', views.view_all_employees, name='view_all_employees'),
    path('website/manager/menu/', views.menu, name='menu'),
    path('website/customer_add/', customer_add, name='customer_add'),
    path('website/customer/menu/', views.menu, name='menu'),
    path('website/manager_login/menu/', views.menu, name='menu'),
    path('website/manager_login/top_food/', views.top_food, name='top_food'),
    path('website/manager_login/total_revenue/', views.total_revenue, name='total_revenue'),
    path('website/manager_login/adjust_price/<str:food_name>/<int:quant>/', views.adjust_price, name='adjust_price'),
    path('website/manager_login/adjust_price/', views.adjust_price_1, name='adjust_price_1'),
    path('website/manager_login/total_orders_by_mode/', views.total_orders_by_mode, name='total_orders'),
]


