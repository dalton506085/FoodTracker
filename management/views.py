from tkinter.font import names

from django.shortcuts import render
from . import views

from django.template import loader
from django.http import HttpResponse
from management.models import Users
from management.models import FoodItem
from management.models import Recipe

import datetime
from datetime import date

def index(request):
    return render(request, 'index.html')

def logout(request):
    if 'totalItems' in request.session:
        del request.session['totalItems']
    if 'user_name' in request.session:
        del request.session['user_name']
    if 'type' in request.session:
        del request.session["type"]
    if 'user_id' in request.session:
        del request.session["user_id"]
    if 'equip_id' in request.session:
        del request.session['equip_id']
    if 'equip_name' in request.session:
        del request.session['equip_name']
    if 'equip_max_qty' in request.session:
        del request.session['equip_max_qty']
    return render(request, 'index.html')

def register(request):
    user_name = request.POST['user_name']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email_id = request.POST['email_id']
    password = request.POST['password']
    cpassword = request.POST['cpassword']
    message = ""
    user = Users.objects.filter(user_name=user_name)
    if password !=cpassword:
        message = "Password and confirm password does not match"
    elif user.count() !=0:
        message = 'User name already exists!'
    else:
        user = Users(first_name=first_name, last_name=last_name, email_id=email_id, password=password,user_name=user_name)
        user.save()
        message = 'successfully registered!'
    context = {
        'message': message,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def login(request):
    if request.POST['user_name'] == 'admin':
        user = Users.objects.get(user_name='admin')
        print(user)
        if request.POST['password'] == user.password:
            request.session["type"] = "admin"
            request.session["user_id"] = user.id
            request.session["user_name"] = user.user_name
            return dashboard(request)
        else:
            message = 'Invalid Admin Password'
            context = {
                'message': message,
            }
            template = loader.get_template('index.html')
            return HttpResponse(template.render(context, request))
    else:
        user = Users.objects.filter(user_name=request.POST['user_name']).values()
        print(user[0])
        if user.count()!=0 and request.POST['password'] == user[0]['password']:
            request.session["type"] = "student"
            request.session["user_id"] = user[0]['id']
            request.session["user_name"] = user[0]['user_name']
            return dashboard(request)
        else:
            message = 'Invalid Username/Password'
            context = {
                'message': message,
            }
            template = loader.get_template('index.html')
            return HttpResponse(template.render(context, request))

def dashboard(request):
    vegetables = FoodItem.objects.filter(type='vegetables')
    fruits = FoodItem.objects.filter(type='fruits')
    grains = FoodItem.objects.filter(type='grains')
    dairy = FoodItem.objects.filter(type='dairy')

    context = {
        'num_vegetables': vegetables.count(),
        'num_fruits': fruits.count(),
        'num_grains': grains.count(),
        'num_dairy': dairy.count(),
    }
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render(context, request))

def addFoodItem(request):
    return render(request, 'addFoodItem.html')

def saveItem(request):
    template = loader.get_template('addFoodItem.html')
    item_id  = request.POST.get('item_id')
    item_name = request.POST.get('item_name')
    food_type = request.POST.get('food_type')
    item_qty = request.POST.get('item_qty')
    expiry_date = request.POST.get('expiry_date')
    recipe_name = request.POST.get('recipe_name')

    print (expiry_date)
    if item_id != '':
        foodItem = FoodItem.objects.get(item_id=item_id)
        foodItem.name = item_name
        foodItem.type = food_type
        foodItem.quantity = item_qty
        foodItem.expiryDate = expiry_date
        foodItem.recipe_id = 1
        foodItem.recipe_name = recipe_name
        foodItem.save()
        context = {
            'message': 'Item updated successfully!',
        }
        return HttpResponse(template.render(context, request))
    else:
        foodItem = FoodItem(name= item_name,type=food_type, quantity=item_qty, expiryDate=expiry_date, recipe_id=1, recipe_name=recipe_name)
        foodItem.save()
        context = {
            'message': 'Item added successfully!',
        }
        return HttpResponse(template.render(context, request))

def updateItem(request):
    template = loader.get_template('addFoodItem.html')
    item_id = request.GET.get('item_id')
    print("Clicked Item ID " + str(item_id))
    foodItem = FoodItem.objects.get(item_id=item_id)
    context = {
        'foodItem': foodItem,
    }
    return HttpResponse(template.render(context, request))

def viewItems(request):
    template = loader.get_template('viewFoodItems.html')
    foodItems = FoodItem.objects.all()
    context = {
        'foodItems': foodItems,
    }
    return HttpResponse(template.render(context, request))

def deleteItem(request):
    item_id = request.GET.get('item_id')
    foodItem = FoodItem.objects.get(item_id=item_id)
    foodItem.delete()
    return viewItems(request)


def expiryChart(request):
    template = loader.get_template('expiryChart.html')
    foodItems = FoodItem.objects.all()

    labels = []
    counts = []
    today = date.today()
    for foodItem in foodItems:
        exp_day = datetime.date(foodItem.expiryDate.year, foodItem.expiryDate.month, foodItem.expiryDate.day)
        if today > exp_day:
            labels.append(foodItem.name)
            counts.append(foodItem.quantity)
    print(labels)
    print(counts)
    request.session['labels'] = labels
    context = {
        "status_lables": ["Apple", "Orange"],
        "status_count": counts
    }
    return HttpResponse(template.render(context, request))