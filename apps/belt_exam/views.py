from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote


def index(request):
    return render(request, 'belt_exam/index.html')

def quotes(request):
    context={
        "users": User.objects.get(id = request.session["id"]),
        "quotes": Quote.objects.all().order_by("-created_at")
    }
    return render(request, 'belt_exam/quotes.html', context)

def user_page(request, id):
    context = {
    "users" : User.objects.get(id = id),
    "quotes" : Quote.objects.all()
    }
    return render(request, "belt_exam/user.html", context)

def login(request):
    email=request.POST["email"]
    password=request.POST["password"]
    login1={
        "email": email,
        "password": password
    }
    check=User.objects.validate_login(login1)
    if check:
        for i in range (0, len(check)):
            messages.add_message(request, messages.INFO, check[i])
        return redirect ('/')
    user1=User.objects.filter(email=email, password=password)
    request.session["id"]=user1[0].id
    return redirect('/quotes')

def register(request):
    first_name=request.POST["first_name"]
    last_name=request.POST["last_name"]
    email=request.POST["email"]
    password=request.POST["password"]
    confirm_pw=request.POST["confirm_pw"]
    dob=request.POST["dob"]
    user1 = User.objects.filter(email = email)
    if user1:
        messages.add_message(request, messages.INFO, "Email exists, please login")
        return redirect ('/')
    register1 = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "confirm_pw": confirm_pw,
        "dob": dob
    }
    check = User.objects.validate_registration(register1)
    if check:
        for x in range(0, len(check)):
            messages.add_message(request, messages.INFO, check[x])
        return redirect ('/')
    User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password, dob=dob)
    user2 = User.objects.get(email=email, password=password)
    request.session["id"]=user2.id
    return redirect ('/quotes')

def postquote(request):
    user = User.objects.get(id = request.session["id"])
    quoter= request.POST["quoter"]
    content = request.POST['content']
    if len(quoter)<4:
        messages.add_message(request, messages.INFO, "The quoted by needs to be more than 3 characters")
        return redirect ('/quotes')
    if len(content)<11:
        messages.add_message(request, messages.INFO, "The message needs to be more than 10 characters")
        return redirect ('/quotes')
    Quote.objects.create(quoter=quoter, content=content, user = user)
    return redirect('/quotes')

def favoritequote(request, id):
    quote = Quote.objects.get(id = id)
    user = User.objects.get(id = request.session["id"])
    quote.favorite.add(user)
    return redirect('/quotes')

def removequote(request, id):
    quote = Quote.objects.get(id = id)
    user = User.objects.get(id = request.session["id"])
    quote.favorite.remove(user)
    return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect ('/')
