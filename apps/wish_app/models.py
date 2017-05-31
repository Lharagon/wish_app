from __future__ import unicode_literals
from django.db import models
import re
from django.contrib import messages
import bcrypt
from datetime import datetime
from django.utils import timezone

# Create your models here.
name_re = re.compile(r'^[A-Za-z\s]{1,}$')
password_re = re.compile(r'^[a-zA-Z0-9.+_-]{8,}.\*?$')

class UserManager(models.Manager):
	def Reg_validator(self, post_data, request):
		errors = []
		empty = False

		if len(post_data['name']) == 0:
			empty = True
		elif not name_re.match(post_data['name']):
			errors.append("First name can't be fewer than 3 characters")

		if len(post_data['username']) < 3:
			empty = True
			errors.append("Username can't be fewer than 3 characters")
			user = User.objects.filter(username = post_data['username'])
			if len(user) > 0:
				errors.append('Username already taken')

		if len(post_data['password']) == 0:
			empty = True
		elif not password_re.match(post_data['password']):
			errors.append("Password must be more than 8 characters.")

		if post_data['password'] != post_data['passconf']:
			errors.append("Passwords don't match")

		try:
			datetime.strptime(post_data['hired_date'], "%Y-%m-%d")
			
		except:
			errors.append("Not valid Date")

		if empty:
			errors.append("All fields are required")


		if len(errors) > 0:
			for error in errors:
				messages.error(request, error)

			return False
		
		return True
		
	def Log_validator(self, post_data, request):
		try:
			user = User.objects.get(username = post_data['username'])
			hashed_pass = bcrypt.hashpw(request.POST['password'].encode(), user.password.encode())
			
			if  hashed_pass == user.password:
				# request.session['user'] = user.first_name
				return True
			messages.error(request, "Not valid username or password")
			return False
		except:
			messages.error(request, "Not valid username or password")
			return False

class User(models.Model):
	name = models.CharField(max_length=100)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=150)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	date_hired = models.DateTimeField(default=timezone.now)
	objects = UserManager()

class Item(models.Model):
	item_name = models.CharField(max_length=100)
	creator = models.ForeignKey(User, related_name="my_products")
	wished_by = models.ManyToManyField(User, related_name = "my_wishes")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

