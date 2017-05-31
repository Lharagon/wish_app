from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Item
import bcrypt
# Create your views here.

def main(request):
	return render(request, 'wish_app/main.html')

def dashboard(request):
	me = User.objects.get(id = request.session['user_id'])
	my_wishes = Item.objects.filter(wished_by = me)
	others_wishes = Item.objects.exclude(wished_by = me)

	context = {
		"my_wish_list": my_wishes,
		"others_wishes": others_wishes
		}
	return render(request, 'wish_app/dashboard.html', context)

def register(request):
	if request.method == 'POST':
		validated = User.objects.Reg_validator(request.POST, request)
		if validated:
			hashed_pass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			print "This is the hashed_ass at register", hashed_pass
			user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashed_pass, date_hired=request.POST['hired_date'])
			request.session['user'] = user.name
			request.session['user_id'] = user.id
			return redirect('/dashboard')

		return redirect('/')

def login(request):
	if request.method == 'POST':
		validated = User.objects.Log_validator(request.POST, request)
	
		if validated:
			user = User.objects.get(username=request.POST['username'])
			request.session['user'] = user.name
			request.session['user_id'] = user.id
			return redirect('/dashboard')
	
		return redirect('/')

	return redirect('/')

def log_out(request):
	# if request.method == 'POST':
	request.session.clear();
	messages.success(request, "Hurry Back!!!!")
	return redirect('/')

def add_page(request):
	return render(request, 'wish_app/create.html')

def add_product(request, id):
	product = request.POST['item']
	if len(product) > 2:
		creator = User.objects.get(id = id)
		new_product = Item.objects.create(item_name = product, creator = creator)

		new_product.wished_by.add(creator)

		return redirect('/dashboard')

	messages.error(request, "Product field must have at least 3 characters")
	return redirect('/add_page')

def item_profile(request, id):
	product = Item.objects.get(id = id)
	people = User.objects.filter(my_wishes = product)

	context = {
		"product": product,
		'people': people
	}
	return render(request, 'wish_app/item.html', context)

def delete(request, id):
	Item.objects.get(id = id).delete()

	return redirect('/dashboard')

def add_wish(request, id):
	new_wish = Item.objects.get(id = id)
	me = User.objects.get(id = request.session['user_id'])
	new_wish.wished_by.add(me)

	return redirect('/dashboard')

def remove_wish(request, id):
	wish = Item.objects.get(id=id)
	me = User.objects.get(id = request.session['user_id'])
	wish.wished_by.remove(me)

	return redirect('/dashboard')






