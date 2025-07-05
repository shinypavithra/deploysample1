from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score


def home_view(request):
    return render(request, 'home.html')



def register_view(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if not all([username, password, confirmpassword]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != confirmpassword:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        user = User.objects.create_user(username=username,password=password)
        
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'register.html')



def predict(request):
    if request.method == 'POST':
        
        df = pd.read_csv('data.csv')
        x = df[['temp', 'hum', 'ph']]
        y = df['rain']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        model = LogisticRegression()
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        result = r2_score(y_test, y_pred)

        
        a = int(request.POST.get('temp'))
        b = int(request.POST.get('hum'))
        c = int(request.POST.get('ph'))

        prediction = model.predict([[a, b, c]])[0]

        return render(request, 'result.html', {'prediction': prediction, 'score': result})
    return render(request, 'predict.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('login')
