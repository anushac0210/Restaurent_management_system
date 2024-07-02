
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from datetime import date
from .forms import c_add
from .forms import eo
from .forms import bill
from .forms import login_details
from django.contrib import messages
from django.shortcuts import redirect


# def login():
#     template = loader.get_template('welcome.html')
#     return HttpResponse(template.render())

def homepage(request):
    return render(request,'homepage.html')



def enter_customer(req):
    return render(req,'customers.html')

def customer_add(req):
    if req.method == 'POST':
        form = c_add(req.POST)
        if form.is_valid():
            cust_fname = form.cleaned_data["cust_fname"]
            cust_lname = form.cleaned_data["cust_lname"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            mem = form.cleaned_data["members"]
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO customer (cust_fname, cust_lname, contact_no, email_id) VALUES (%s, %s, %s, %s)", [cust_fname, cust_lname, phone, email])
                cursor.execute("select * from GetLastcustomer()")
                c_id = cursor.fetchone()
                cursor.execute("call Table_allocation(%s,%s)",[c_id[0],mem])
                cursor.execute("select * from GetLasttableid()")
                t_id=cursor.fetchone()
                cursor.execute("select * from GetLastorderid()")
                o_id=cursor.fetchone()
                messages.success(req, 'Customer added successfully and his table is %s and order id is : %s' % (t_id[0], o_id[0]))

    else:
        form = c_add()  
    return render(req, 'customers.html', {'form': form})

def enter_order(req):
    return render(req,'enter_order.html')
    


def insert_oi(req):
    if req.method == 'POST':
        form = eo(req.POST)
        if form.is_valid():
            f1 = form.cleaned_data["o_id"]
            f2 = form.cleaned_data["food_name"]
            f3 = form.cleaned_data["quant"]
            with connection.cursor() as cursor:
                cursor.execute("SELECT food_id FROM food WHERE food_name = %s", [f2])
                f_id = cursor.fetchone()
                if f_id:
                    cursor.execute("call insert_oi(%s,%s,%s)",[f1,f_id[0],f3])
                    return redirect(f'/website/server/')  # Redirect to the same view
                else:
                    # Handle if food not found
                    return HttpResponse("Food not found")
    else:
        form = eo()  # Assuming enter_order1 is your form class
    return render(req, 'enter_order.html', {'form': form})


def allocating_table(request):
    with connection.cursor() as cursor:
        cursor.execute("call Table_allocation(7,2)")
    return HttpResponse('Done table allocation')

def bill_calculation(req):
    return render(req,'bill_calculation.html')

def display_bill(req):
    if req.method == 'POST':
        form = bill(req.POST)
        if form.is_valid():
            f1 = form.cleaned_data["o_id"]
            f2 = form.cleaned_data["method"]
            with connection.cursor() as cursor:
                cursor.execute("call bill(%s,%s)",[f1,f2])
                cursor.execute("SELECT * FROM bill WHERE order_id = %s order by bill_no desc limit 1", [f1])
                display = cursor.fetchall()
                context = {
                    'display_bill' : display,
                }
                template = loader.get_template('display_bill.html')
                return HttpResponse(template.render(context,req))
    else:
        form = eo()  # Assuming enter_order1 is your form class
    return render(req, 'bill_calculation.html', {'form': form})

    



def menu(request):
    with connection.cursor() as cursor:
        cursor.execute("set role manager")
        display_query = "SELECT food_id,food_name , price FROM food order by food_id"
        cursor.execute(display_query)
        rows = cursor.fetchall()
        
        # Constructing a list of dictionaries for each row
        items = [{'id':row[0],'name': row[1], 'price': row[2]} for row in rows]

    return render(request, 'menu1.html', {'items': items})

def chef_food(r):
    with connection.cursor() as cursor:
        cursor.execute("select distinct * from chef_food")
        display = cursor.fetchall()
        contex={
            'chef_food':display,
        }
        template = loader.get_template('chef_and_food.html')
    return HttpResponse(template.render(contex,r))

def manager_login(req):
    if req.method == 'POST':
        form = login_details(req.POST)
        if form.is_valid():
            f1 = form.cleaned_data["username"]
            f2 = form.cleaned_data["password"]
            with connection.cursor() as cursor:
                cursor.execute("select password from login where user_name = 0")
                display = cursor.fetchone()
                if (f2==display[0] and f1 ==0):
                    cursor.execute("set role manager")
                    return render(req,'manager_view.html')
    return render(req,'manager_login.html')

def chef_login(req):
    return render(req,'chef_login.html')

def server_login(req):
    return render(req,'server_login.html')

def dining_supervisor_login(req):
    return render(req,'dining_supervisor_login.html')

def manager(req):
    with connection.cursor() as cursor:
        cursor.execute("set role manager")
    return render(req,'manager_view.html')

def server(req):
    return render(req,'server_view.html')

def dining_supervisor(req):
    return render(req,'dining_supervisor_view.html')


def customer(req):
    return render(req,'customer_view.html')


def chef(req,id):
    with connection.cursor() as cursor:
        cursor.execute("select * from notserved_food where chef_id = %s",[id])
        display = cursor.fetchall()
        template = loader.get_template('chef_pending_orders.html')
        context={
            'chef_done':display,
        }
        return HttpResponse(template.render(context,req))

def website(req):
    return render(req,'index.html')

    
def view_all_employees(request):
    with connection.cursor() as cursor:
        cursor.execute("set role manager")
        display_query = "SELECT emp_fname || ' ' || emp_lname, designation, emp_salary FROM employee"
        cursor.execute(display_query)
        rows = cursor.fetchall()
        
        # Constructing a list of dictionaries for each row
        employees = [{'name': row[0], 'designation': row[1], 'salary': row[2]} for row in rows]

    return render(request, 'employees.html', {'employees': employees})



def chef_serve(request, id, sno):
    with connection.cursor() as cursor:
        cursor.execute("call chef_serve(%s)", [sno])
    return redirect(f'/website/chef_login/chef/{id}/')



def food_chef(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from chef_food")
        display = cursor.fetchall()
        template = loader.get_template('food_chef.html')
        context = {
            'food_chef':display,
        }
        return HttpResponse(template.render(context,request))
def top_food(request):
    with connection.cursor() as cursor:
        cursor.execute("select food_name,total_orders,food_id from top_selling_food_items")
        display=cursor.fetchall()
        template=loader.get_template('top_selling.html')
        context={
            'top_food':display
        }
        return HttpResponse(template.render(context,request))

def total_revenue(request):
    with connection.cursor() as cursor:
        cursor.execute("select order_date,total_orders,total_revenue from orders_revenue_by_date")
        display=cursor.fetchall()
        template=loader.get_template('total_revenue.html')
        context={
            'total_revenue':display
        }
        return HttpResponse(template.render(context,request))
    
def total_orders_by_mode(request):
    with connection.cursor() as cursor:
        cursor.execute("select payment_mode,sum(net_amount) from payment inner join bill on payment.bill_no = bill.bill_no group by payment_mode ")
        display = cursor.fetchall()
        template = loader.get_template('total_orders_by_mode.html')
        context={
            'total_orders_by_mode':display
        }
        return HttpResponse(template.render(context,request))


def adjust_price(req, food_name, quant):
    with connection.cursor() as cursor:
        cursor.execute("SELECT food_id FROM food WHERE food_name = %s", [food_name])
        id_ = cursor.fetchone()
        if id_:
            food_id = int(id_[0])  # Extracting the first element of the tuple and converting it to an integer
            cursor.execute("select adjust_price(%s, %s)", [food_id, quant])
    return redirect('/website/manager_login/menu/')


def adjust_price_1(req):
    return render(req,'adjust_price.html')

