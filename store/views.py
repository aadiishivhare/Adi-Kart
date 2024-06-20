from django.shortcuts import render
from django.http import JsonResponse
from .models import * 
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)
	# if request.user.is_authenticated:   # will check wheter the user is authenticated or not
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer = customer, complete = False) # get or create method have checking function within it to check user first name and email and if not then it will create it
	# 	items = order.orderitem_set.all()
	# 	cartItems = order.get_cart_items
	# else:
	# 	# items = [] # if user is not authenticated then for page visitor 
	# 	# order = {'get_cart_total':0, "get_cart_items":0, 'shipping': False}
	# 	# cartItems = order['get_cart_items']
	# 	cookieData = cookieCart(request)
	# 	cartItems= cookieData['cartItems']

	# products = Product.objects.all()
	# context = {'products':products, 'cartItems': cartItems}
	# return render(request, 'store/store.html', context)

def cart(request):
	# if request.user.is_authenticated:   # will check wheter the user is authenticated or not
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer = customer, complete = False) # get or create method have checking function within it to check user first name and email and if not then it will create it
	# 	items = order.orderitem_set.all()
	# 	cartItems = order.get_cart_items
	# else:
	# 	cookieData = cookieCart(request)
	# 	cartItems= cookieData['cartItems']
	# 	order= cookieData['order']
	# 	items= cookieData['items']

	# context = {'items': items, 'order' : order, 'cartItems':cartItems}
	# return render(request, 'store/cart.html', context)
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	# products = Product.objects.all()
	context = {'items': items, 'order' : order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	# if request.user.is_authenticated:   # will check wheter the user is authenticated or not
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer = customer, complete = False) # get or create method have checking function within it to check user first name and email and if not then it will create it
	# 	items = order.orderitem_set.all()
	# 	cartItems = order.get_cart_items
	# else:
	# 	# items = [] # if user is not authenticated then for page visitor 
	# 	# order = {'get_cart_total':0, "get_cart_items":0, 'shipping': False} # a replica for orders and it items so that no error comes through cart.html
	# 	# cartItems = order['get_cart_items']
	# 	cookieData = cookieCart(request)
	# 	cartItems= cookieData['cartItems']
	# 	order= cookieData['order']
	# 	items= cookieData['items']
	# context = {'items': items, 'order' : order, 'cartItems':cartItems}
	# return render(request, 'store/checkout.html', context)
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added',safe= False)

def processOrder(request):
	# transaction_id = datetime.datetime.now().timestamp()
	# data = json.loads(request.body)

	# if request.user.is_authenticated:
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# 	total = float(data['form']['total'])
	# 	order.transaction_id = transaction_id
	# 	if total == order.get_cart_total:
	# 		order.complete = True
	# 	order.save()

	# 	if order.shipping == True:
	# 		ShippingAddress.objects.create(
	# 			customer=customer,
	# 			order=order,
	# 			address=data['shipping']['address'],
	# 			city=data['shipping']['city'],
	# 			state=data['shipping']['state'],
	# 			zipcode=data['shipping']['zipcode'],
	# 		)
	# else:
	# 	print('not logged')
	# 	# customer, order = guestOrder(request, data)



	# print('Data:', request.body)
	# return JsonResponse('Payment submitted..', safe=False)
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)