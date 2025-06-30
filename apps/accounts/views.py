from django.shortcuts import render, redirect
from django.contrib import messages
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
        
        # Создание пользователя через create_user() (правильно для кастомной модели)
        Customer.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')  # убедись, что в urls.py есть path с name='login'
    
    return render(request, 'register.html')
