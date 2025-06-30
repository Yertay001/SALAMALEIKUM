from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Customer

def register(request):
    if request.method == 'POST': 
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Проверка на заполнение всех полей
        if not all([first_name, last_name, email, password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')
        
        # Проверка длины пароля
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'register.html')
        
        # Проверка существования пользователя с таким email
        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'register.html')
        
        # Генерация username на основе email
        username = email.split('@')[0]

        # Создание пользователя через create_user()
        user = Customer.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Account created successfully! You are noe logged in.')
            return redirect('home')
        else:
            messages.error (request, 'There was a problem logging you in automatically. Please login manually.')
            return redirect('login')
        
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Both email and password are required.')
            return render(request, 'login.html')
        
        # Ищем пользователя по email
        try:
            user_obj = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')
        
        # Аутентифицируем по username (так как authenticate требует username)
        user = authenticate(request, username=user_obj.username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')  # замени на маршрут своей главной страницы
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


       

