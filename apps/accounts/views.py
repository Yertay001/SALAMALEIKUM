import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer, Profile
from .utils import send_msg, send_auth_code
from .tasks import send_auth_code_async, send_welcome_message_async

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

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'register.html')

        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'register.html')

        # Создание пользователя через кастомного менеджера
        user = Customer.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        #Генерация и отправка кода авторизации 
        user.auth_code = random.randint(100000, 999999)
        user.save()   

        # Отправка привественного сообщения
        # send_msg(user.email)
        send_welcome_message_async.delay(user.email)

        # Отправка кода авторизации на email
        # send_auth_code(user)
        send_auth_code_async.delay(email=user.email, auth_code=user.auth_code)

        # Вход пользователя в систему
        login(request, user)
        messages.success(request, 'Account created successfully! You are now logged in.')
        return redirect('check_auth_code')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Both email and password are required.')
            return render(request, 'login.html')

        # authenticate напрямую по email
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('/')  # или другой URL
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')

@login_required
def check_auth_code(request):
    if request.method == 'POST':
        auth_code = request.POST.get('auth_code', '').strip()
        user = request.user

        if not auth_code:
            messages.error(request, 'Authenticaation code is required.')
            return render(request, 'check_auth_code.html')
        
        if user.auth_code == auth_code:
            messages.success(request, 'Authentication successful!')
            return redirect('/')  # или другой URL
        else:
            messages.error(request, 'Invalid authentication code.')
            return render(request, 'verify-code.html')
        
    return render(request, 'verify-code.html')

@login_required       
def logout_view(request):
    logout(request)
    messages.success(request, 'You have succesfully logged out.')
    return redirect('/')


@login_required
def profile(request):
    user = request.user
    profile = Profile.objects.get_or_create(customer=user)

    if request.method == 'POST':
        # Здесь можно добавить логику для обновления профиля
        pass
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'profile.html', context=context)


