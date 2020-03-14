from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

#Cargamos vistas de los modelos
from .models import Servicio, Usuario
from .forms import ServicioForm, registroUsuario, Login

# Create your views here.

def index(request):
    servicios = Servicio.objects.all().order_by('id')
    seccion = 'Inicio'
    return render(request, 'webapp/index.html', {'servicios': servicios, 'seccion': seccion})

def verServicios(request):
    servicios = Servicio.objects.all().order_by('id')
    seccion = 'Ver Servicios'
    return render(request, 'webapp/ver_servicios.html', {'servicios': servicios, 'seccion': seccion})

def crearServicio(request):
    seccion = 'Crear Servicio'

    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form= ServicioForm()
    return render(request, 'webapp/crear_servicio.html', {'form': form, 'seccion': seccion})

def altaUsuario(request):
    seccion = 'Alta de nuevo Usuario'
    if request.method == 'POST':
        form = registroUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = registroUsuario()
    return render(request, 'webapp/registro.html', {'form': form, 'seccion':seccion})

def login(request):
    seccion= 'Ingreso de usuario'
    if request.method == 'POST':
        form = Login(data = request.POST)
        if form.is_valid():
            documento = request.POST['documento']
            password = request.POST['password']
            user = authenticate(documento=documento, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request,user)
                    return redirect('/registro') #user is redirected to dashboard
    else:
        form = Login()

    return render(request,'webapp/login.html',{'form':form, 'seccion': seccion})

def logout(request):
    django_logout(request)
    return redirect('/')