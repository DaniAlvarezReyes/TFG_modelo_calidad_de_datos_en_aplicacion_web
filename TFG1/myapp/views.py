import json
import os
import pickle
from django.http import FileResponse
from django.shortcuts import render, redirect
#from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import pandas as pd
import subprocess

# Create your views here.
def index(request):
    title = 'Bienvenido al TFG de Dani'
    return render(request, 'index.html', {
        'title': title
    })


def welcome(request):
    return render(request, 'welcome.html')


def iniciarsesion(request):
    if request.method == 'GET':
        return render(request, 'iniciarsesion.html', {
            'form': iniciarSesion()
        })
    else:
        user = authenticate(username=request.POST['user'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            mensaje = "Usuario o contraseña incorrectos, pruebe otra vez."
            return render(request, 'iniciarsesion.html', {
                'form': iniciarSesion(),
                'error_message': mensaje
            })
        
    

def registro(request):
    if request.method == 'GET':
        
        return render(request, 'registro.html', {
            'form': NewRegistro()
        })
    else:
        try:
            user = User.objects.create_user(username = request.POST['user'], email=request.POST['email'], password=request.POST['password'], 
                                        first_name = request.POST['username'], last_name= request.POST['lastname'])
            login(request, user)
        except:
            return render(request, 'registro.html', {
                'form': NewRegistro(),
                'error_message': 'Ya se ha registrado ese nombre de usuario.'})
        return redirect('welcome')


def logout_view(request):
    logout(request)
    return redirect('index')


def upload_files(request):
    if request.method == 'GET':
        
        return render(request, 'upload_files.html')
    else:

        #Almacenamos el nombre de la hoja en caso de ser introducida
        hoja = request.POST['hoja']
        
        #Vemos cual es el separador introducido en caso de que haya
        try:
            separador = request.POST['separacion']
            print("El separador es: ", separador)
        except:
            separador = 0

        try:
            file = request.FILES['uploaded_files']
        except:
            return render(request, 'upload_files.html', {'error_message': 'Introduce un archivo'})


        if len(hoja)>0:
            try:
                data = pd.read_csv(file, sheet_name=hoja)
            except:
                try:
                    data = pd.read_excel(file, sheet_name=hoja)
                except:
                    print("No existe la hoja introducida")
                    return render(request, 'upload_files.html',{'error_message': '¡No existe la hoja introducida!'})
        elif (separador!=0):
            try:
                data = pd.read_csv(file, sep=separador,low_memory=False, na_values=['NA'])     
            except:
                return render(request, 'upload_files.html',{'error_message': '¡Introduzca bien la separación!'})
        else:
            try:
                data = pd.read_csv(file)
            except:
                try:
                    print("file: ", file)
                    data = pd.read_excel(file)
                except:
                    return render(request, 'upload_files.html',{'error_message': '¡Intentalo otra vez!'})
        data1 = data.head()
        df_html = data1.to_html()
        #print("df_html: ", df_html)

        guardar_excel = 'myapp/archivo_a_analizar.xlsx'
        data.to_excel(guardar_excel)
        #request.session['df'] = data.to_json()
        request.session['df_html'] = df_html
        return redirect('vista_previa')


def vista_previa(request):
    if request.method == 'GET':
        df_html = request.session.get('df_html')
        return render(request, 'vista_previa.html', {
            'df_html': df_html
        })
    else:
        primaryKey = request.POST.get('primarykey', False)
        columnasCalc = request.POST.get('columnasCalc', False)
        df_json = request.session.get('df')
        file = request.session.get('file')
        

        #Comprobamos ruta de programa externo
        ruta_views_py = os.path.abspath(__file__)
        #print("RUTA DE VIEWS.PY: ", ruta_views_py)
        ruta_excel = os.path.join(os.path.dirname(ruta_views_py), 'archivo_a_analizar.xlsx')
        ruta_programa_externo = os.path.join(os.path.dirname(ruta_views_py), 'programaControlCalidadDatos.py')

        
        #Ejecutamos el programa en python
        resultado = subprocess.run(['python3', ruta_programa_externo, ruta_excel], stdout=subprocess.PIPE, text=True)
        external_output = resultado.stdout
        #print("External output: ",external_output)
        processed_array = json.loads(external_output)
        #print("Resultado[0]: ",processed_array[0])
        #print("PROCESSED_ARRAY: ",processed_array)
        #processed_array2 = json.dumps(processed_array)

        # Declarar variables que serán utilizadas después en el html

        context = {
            'resultado': json.dumps(processed_array),
        }

        request.session['resultado'] = json.dumps(processed_array)

        print("Primary key: ", primaryKey)
        print("columnasCalc: ", columnasCalc)
        return render(request, 'resultados.html', {
            'resultado': context
        })
    
def resultados(request):
    if request.method == 'GET':
        context = request.session.get('resultado')
        return render(request, 'resultados.html', {
            'resultado': context
        })
    else:
        return render(request, 'resultados.html', {
            #'resultado': resultado
        })