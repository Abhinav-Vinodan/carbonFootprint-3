from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q
# Create your views here.

def index(request):
    return render(request, 'index.html')

def userReg(request):
    msg = ''
    if request.method == "POST":
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        cPassword = request.POST['cPassword']
        if password == cPassword:
            if User.objects.filter(username=email).exists():
                msg = "Username already exists"
            else:
                user = User.objects.create_user(
                    username=email, password=password)
                customer = Users.objects.create(
                    name=name, email=email, phone=phone, address=address, user=user)
                user.save()
                customer.save()
                msg = "Registration successful"
        else:
            msg = "Password dosen't match"
    return render(request, "userReg.html", {"msg": msg})



def expertsReg(request):
    msg = ''
    if request.method == "POST":
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        aadhar = request.POST['aadhar']
        password = request.POST['password']
        cPassword = request.POST['cPassword']
        qual = request.POST['qual']
        proof = request.FILES['proof']
        if password == cPassword:
            if User.objects.filter(username=email).exists():
                msg = "Username already exists"
            else:
                user = User.objects.create_user(
                    username=email, password=password, is_staff=1, is_active=0)
                customer = Experts.objects.create(
                    name=name, email=email, phone=phone, address=address, user=user,aadhar=aadhar,qual=qual,proof=proof)
                user.save()
                customer.save()
                msg = "Registration successful"
        else:
            msg = "Password dosen't match"
    return render(request, "expertsReg.html", {"msg": msg})


def login(request):
    msg = ""
    if (request.POST):
        email = request.POST.get("uname")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            if user.is_superuser:
                return redirect("/adminHome")
            elif user.is_staff:
                data = Experts.objects.get(email=email)
                request.session['uid'] = data.id
                return redirect('/expHome')
            else:
                data = Users.objects.get(email=email)
                request.session['uid'] = data.id
                return redirect('/userHome')
        else:
            msg = "Invalid Credentials"

    return render(request, "login.html", {"msg": msg})


def adminHome(request):
    return render(request, "adminHome.html")

def adminCategory(request):
    msg  = ''
    if request.POST:
        category = request.POST["category"]
        if Category.objects.filter(cat=category).exists():
            msg = "Category already exists"
        else:
            cat = Category.objects.create(cat=category)
            cat.save()
            msg = "Category Added"
    data = Category.objects.all()
    return render(request, "adminCategory.html", {"msg":msg, "data":data})

def adminCatStatus(request):
    id = request.GET["id"]
    status = request.GET["status"]
    cat = Category.objects.get(id=id)
    cat.status = status
    cat.save()
    return redirect("/adminCategory")

def adminExperts(request):
    data = Experts.objects.filter(user__is_active=1)
    dataIn = Experts.objects.filter(user__is_active=0)
    return render(request, "adminExperts.html", {"data": data, "dataIn": dataIn})

def adminUpdateExperts(request):
    id = request.GET["id"]
    status = request.GET["status"]
    cat = User.objects.get(id=id)
    cat.is_active = status
    cat.save()
    return redirect("/adminExperts")

def adminUsers(request):
    data = Users.objects.all()
    return render(request, "adminUsers.html", {"data": data})

def adminTips(request):
    data = Tips.objects.all().order_by("-id")
    return render(request, "adminTips.html", {"data": data})

def adminViewEmission(request):
    uid = request.GET['id']
    data = Emission.objects.filter(users=uid)
    users = Users.objects.get(id=uid)
    return render(request, "adminViewEmission.html", {"data": data, "users":users})

def expHome(request):
    uid = request.session['uid']
    user = Experts.objects.get(id=uid)
    return render(request, "expHome.html", {"user": user})

def expChats(request):
    uid = request.session['uid']
    data = Message.objects.filter(experts__id=uid)
    chats = set()
    for d in data:
        chats.add(d.users.id)
    clients = Users.objects.all()
    return render(request, "expChats.html", {"clients": clients, "chats": chats})

def expChat(request):
    uid = request.session["uid"]
    ex = Experts.objects.get(id=uid)
    cid = request.GET['id']
    url = request.GET['url']
    us = Users.objects.get(id=cid)
    if request.method == "POST":
        msg = request.POST['msg']
        db = Message.objects.create(experts=ex, users=us, msg=msg, sender='Expert')
        db.save()
    messages = Message.objects.filter(experts=ex, users=us)
    return render(request, "expChat.html", {"messages": messages,"url":url})

def expViewEmission(request):
    uid = request.GET['id']
    data = Emission.objects.filter(users=uid)
    users = Users.objects.get(id=uid)
    return render(request, "expViewEmission.html", {"data": data, "users":users})

def expTips(request):
    uid = request.session['uid']
    user = Experts.objects.get(id=uid)
    if request.POST:
        subject = request.POST['subject']
        details = request.POST['details']
        image = request.FILES['image']
        gal = Tips.objects.create(subject=subject, details=details, image=image,experts=user)
        gal.save()
    data = Tips.objects.filter(experts__id=uid)
    return render(request, "expTips.html", {"data": data})

def expDelTip(request):
    id = request.GET["id"]
    cat = Tips.objects.get(id=id)
    cat.delete()
    return redirect("/expTips")


def userHome(request):
    uid = request.session['uid']
    user = Users.objects.get(id=uid)
    return render(request, "userHome.html", {"user": user})

def calculate_carbon_footprint(device_power, hours_per_day, lifespan_years, no_of_devices, electricity_emission_factor):
    energy_consumption_per_year = device_power * hours_per_day *no_of_devices * 30 / 1000
    total_energy_consumption = energy_consumption_per_year * lifespan_years
    total_emissions = total_energy_consumption * electricity_emission_factor
    return total_emissions

def userDevice(request):
    carbon_footprint = ''
    charge = ''
    uid = request.session['uid']
    user = Users.objects.get(id=uid)
    if request.POST:
        device_power = float(request.POST['device_power']) 
        hours_per_day = float(request.POST['hours_per_day'])   
        lifespan_years = float(request.POST['lifespan_years'])  
        no_of_devices = float(request.POST['no_of_devices'])
        cat = request.POST['cat']  
        category = Category.objects.get(id=cat)
        electricity_emission_factor_kerala = 0.5
        carbon_footprint = calculate_carbon_footprint(device_power, hours_per_day, lifespan_years, no_of_devices, electricity_emission_factor_kerala)
        carbons=(device_power/1000)*hours_per_day*30
        charge = 0
        if carbons >= 0 and carbons <= 50:
            charge = carbons * 40
        elif carbons >= 51 and carbons <= 100:
            charge = carbons * 65
        elif carbons >= 101 and carbons <= 150:
            charge = carbons * 85
        elif carbons >= 151 and carbons <= 200:
            charge = carbons * 120
        elif carbons>= 201 and carbons <= 250:
            charge = carbons * 130
        elif carbons >= 251 and carbons <= 300:
            charge = carbons * 150
        elif carbons >= 301 and carbons <= 350:
            charge = carbons * 175
        elif carbons >= 351 and carbons <= 400:
            charge = carbons * 200
        elif carbons >= 401 and carbons <= 500:
            charge = carbons * 230
        elif carbons >= 500:
            charge = carbons * 260
        
        qry = Emission.objects.create(users=user, device_power=device_power, hours_per_day=hours_per_day, lifespan_years=lifespan_years, no_of_devices=no_of_devices, result=carbon_footprint,category=category,charge=charge)
        qry.save()
    cats = Category.objects.filter(status='Active')
    return render(request, "userDevice.html", {"data":carbon_footprint, "cats":cats, "charge":charge})

def userHistory(request):
    uid = request.session['uid']
    data = Emission.objects.filter(users=uid)
    return render(request, "userHistory.html", {"data": data})

def userExperts(request):
    data = Experts.objects.filter(user__is_active=True)
    return render(request, "userExperts.html", {"data": data})

def userChats(request):
    uid = request.session['uid']
    data = Message.objects.filter(users__id=uid)
    chats = set()
    for d in data:
        chats.add(d.experts.id)
    exps = Experts.objects.all()
    return render(request, "userChats.html", {"exps": exps, "chats": chats})

def userChat(request):
    uid = request.session["uid"]
    us = Users.objects.get(id=uid)
    eid = request.GET['id']
    url = request.GET['url']
    ex = Experts.objects.get(id=eid)
    if request.method == "POST":
        msg = request.POST['msg']
        db = Message.objects.create(experts=ex, users=us, msg=msg, sender='User')
        db.save()
    messages = Message.objects.filter(experts=ex, users=us)
    return render(request, "userChat.html", {"messages": messages,"url":url})


def userTips(request):
    uid = request.session['uid']
    data = Tips.objects.filter().order_by("-id")
    return render(request, "userTips.html", {"data": data})




























































