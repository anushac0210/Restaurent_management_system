from django import forms

class c_add(forms.Form):
    cust_fname = forms.CharField(label="cust_fname")
    cust_lname = forms.CharField(label="cust_lname")
    email = forms.CharField(label="email")
    phone = forms.CharField(label="phone")
    members = forms.CharField(label="members")

class eo(forms.Form):
    o_id = forms.IntegerField(label="o_id")
    food_name = forms.CharField(label="food_name")
    quant = forms.IntegerField(label="qaunt")
    
class bill(forms.Form):
    o_id = forms.IntegerField(label="o_id")
    method = forms.CharField(label="method")


class login_details(forms.Form):
    username = forms.IntegerField(label="username")
    password = forms.CharField(label="password")