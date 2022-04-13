from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth  import authenticate,login,logout
import json
# Create your views here.
def index(Request):
	products = Product.objects.all()
	allProds = []		
	catprods = Product.objects.values('category','id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prod = Product.objects.filter(category = cat)
		n = len(prod)
		nSlides= n//4 + ceil((n/4) + (n//4))
		allProds.append([prod,range(1,nSlides),nSlides])

	params = {"allProds":allProds}
	return render(Request,'shop/index.html',params)

def searchMatch(query,item):
	if query in item.product_name.lower() or query in item.desc.lower() or query in item.category.lower():
		return True
	else:
		return False

def search(Request):
	query = Request.GET.get('search')
	products = Product.objects.all()
	allProds = []		
	catprods = Product.objects.values('category','id')
	cats = {item['category'] for item in catprods}
	for cat in cats:
		prodtemp = Product.objects.filter(category = cat)
		prod = [item for item in prodtemp if searchMatch(query,item)]
		n = len(prod)
		nSlides= n//4 + ceil((n/4) + (n//4))
		if(len(prod)!=0):
			allProds.append([prod,range(1,nSlides),nSlides])
			msg = ""
		if(len(allProds)==0):
			msg = "Please enter relevant query.."

	params = {"allProds":allProds,"msg":msg}
	return render(Request,'shop/search.html',params)

def about(Request):
	return render(Request,'shop/about.html')

def contact(Request):
	print(Request)
	if Request.method == "POST":
		print(Request)
		name = Request.POST.get('name','')
		email = Request.POST.get('email','')
		phone = Request.POST.get('phone','')
		query = Request.POST.get('query','')
		print(name)
		contact = Contact(name=name,email=email,phone=phone,query=query)
		contact.save()
	return render(Request,'shop/contact.html')


def productView(Request,myid):
	#fetch product using Id
	prod = Product.objects.filter(id = myid)
	return render(Request,'shop/prodview.html',{"product":prod[0]})

def checkout(Request):
	if Request.method == "POST":
		items_json = Request.POST.get('itemsJson','')
		name = Request.POST.get('name','')
		email = Request.POST.get('email','')
		address = Request.POST.get('address1','')+" "+Request.POST.get('address2','')
		state = Request.POST.get('state','')
		city = Request.POST.get('city','')
		zipcode = Request.POST.get('zipcode','')
		phone = Request.POST.get('phone','')
		amount = Request.POST.get('amount','')
		print(name)
		order = Orders(items_json=items_json,name=name,email=email,phone =phone,address=address,city=city,
			state=state,zipcode=zipcode,amount=amount)
		order.save()
		update = OrderUpdate(order_id = order.order_id,update_desc = "Your order is placed")
		update.save()
		thank = True
		id = order.order_id
		return render(Request, 'shop/checkout.html', {'thank':thank, 'id': id})
	return render(Request,'shop/checkout.html')

def tracker(Request):
	if Request.method == "POST":
		order_id = Request.POST.get('order_id','')
		email = Request.POST.get('emailUser','')
		print("order:"+order_id+"email:"+email)
		try:
			order = Orders.objects.filter(order_id = order_id,email=email)
			print(order)
			if len(order)>0:
				update = OrderUpdate.objects.filter(order_id=order_id)
				updates = []
				for item in update:
					updates.append({'text': item.update_desc, 'time': item.timestamp})
					response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json},default=str)
				return HttpResponse(response)
			else:
				return HttpResponse('{"status":"noitem"}')
		except Exception as e:
			print(e)
			return HttpResponse('{"status":"error"}')
	return render(Request,'shop/tracker.html')


def handleSignup(Request):
	if Request.method=="POST":
		# Get the post parameters
		username=Request.POST['username']
		print("username"+username)
		email=Request.POST['email']
		fname=Request.POST['fname']
		lname=Request.POST['lname']
		pass1=Request.POST['pass1']
		pass2=Request.POST['pass2']

		# check for errorneous input
		if len(username)<5:
			messages.error(Request,"Your username must be more than 5 Characters")
			return redirect("ShopHome")
		if not username.isalnum():
			messages.error(Request, "User name should only contain letters and numbers")
			return redirect('ShopHome')				
		if pass1 != pass2:
			messages.error(Request,"Password doesn't match")
			return redirect("ShopHome")
	
		# Create the user
		myuser = User.objects.create_user(username, email, pass1)
		myuser.first_name= fname
		myuser.last_name= lname
		myuser.save()
		messages.success(Request, "Your Account has been successfully created")
		return redirect('ShopHome')
	else:
		return HttpResponse('404-not found')


def handleLogin(Request):
	if Request.method == "POST":		
		loginusername = Request.POST['loginusername']
		loginpassword = Request.POST['loginpassword']

		user = authenticate(username = loginusername, password = loginpassword)
		if user is not None:
			login(Request,user)
			messages.success(Request,"You are logged in..!")
			return redirect('ShopHome')
		else:
			messages.error(Request,"Invalid Credentials ! Please try again")
			return redirect('ShopHome')
	return HttpResponse("404-Not Found")

def handleLogout(Request):
    logout(Request)
    messages.success(Request, "Successfully logged out")
    return redirect('ShopHome')