from world.forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from . import models

# Create your views here.
def index(request):
    user = LoginForm()
    if user.is_valid():
        user.save()
        render(request, "login.html", {'form': user})
        return redirect('home')
    else:
        return render(request,"login.html",{'form':user})

def register(request):
    if request.method == 'POST':  # if the form has been submitted
        form = UserRegistrationForm(request.POST)  # form bound with post data
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required()
def update_location(request):
    try:
        print("Updating user location")
        user_profile = models.Profile.objects.get(user=request.user)
        if not user_profile:
            raise ValueError("Can't get User Details")

        point = request.POST["point"].split(",")
        point = [float(part) for part in point]
        point = Point(point, srid=4326)

        user_profile.last_location = point
        user_profile.save()

        return JsonResponse({"message": f"Set location to {point.wkt}."},status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)},status=400)