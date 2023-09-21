# -*- coding: utf-8 -*-

from datetime import datetime
import io
import json
import pickle
import tempfile
import pandas as pd
import numpy as np
from odf.opendocument import load
import sys
import os
import chardet



def comprobarTipo():
    #mismoTipo = np.full(ncol, True, dtype=bool)
    mismoTipo = []
    for i in range(ncol):
        encontradoMalo = False
        if(arrayNumNanCol[i]==nfil):   # Si toda la columna esta vacia es del mismo tipo, NaN
            mismoTipo.append([True, "NaN"])
        else: # Si no buscamos de que tipo es el primer dato de la columna
            for j in range(nfil):
                if(pd.isna(df.iloc[j, i])==False):
                    tipocol = type(df.iloc[j, i])
                    break
            for j in range(nfil): # Una vez sabemos el tipo, vemos si el tipo de todos los datos de la columna es el mismo
                dato = df.iloc[j, i]
                tipocol1 = type(dato)
                if(tipocol != tipocol1 and pd.isna(dato)!=True):    # Si un dato varia, el tipo ya no es el mismo y lo guardamos
                    mismoTipo.append(False)
                    encontradoMalo = True
                    break
            if(encontradoMalo == False):
                mismoTipo.append([True, tipocol])  # Solo si el tipo es el mismo llegará aqui y lo guardamos
    return mismoTipo

#Devuelve cuantas celdas vacías hay en cada columna y donde están
def celdasVacias():
    resultado = []
    celdasVacias = np.full(ncol, 0, dtype=int)
    dondeVacio = np.zeros((nfil,ncol))
    for i in range(ncol):
        ncelvacia = 0
        for j in range(nfil):
            dato = df.iloc[j, i]
            if(pd.isna(dato)==False):
                dondeVacio[j,i] = 1
            else:
                ncelvacia+=1
        celdasVacias[i] = ncelvacia   
    resultado.append(dondeVacio.tolist())
    resultado.append(celdasVacias.tolist())
    return resultado


def celdasVaciasFila():
    arrayNumNanFil = np.full(nfil, 0, dtype=int)
    for i in range(nfil):
        for j in range(ncol):
            if(arrayDondeNan[i][j] == 0):
                arrayNumNanFil[i] += 1
    return arrayNumNanFil.tolist()



def calcularCompletitud():
    nCeldasVacias = 0
    llamadaCeldasVacias = numceldasVacias
    for i in range(ncol):
        nCeldasVacias+=llamadaCeldasVacias[1][i]
    gradoCompletitud = 100-(nCeldasVacias*100)/nCeldasTotales
    retornado = []
    retornado.append(gradoCompletitud)
    retornado.append(nCeldasVacias)
    retornado.append(nCeldasTotales)
    return retornado
#def maxdeep(df):
    
# Funcion para determinar si hay datos alejados que se hayan colado por error, para ello vemos si en su fila y columna hay mas de tres datos, ya que
# si un dato esta puesto por error fuera del df inicial alguna de su fila o columna estará vacia, a excepcion de que haya otro dato por error mas, por
# lo que ponemos ese umbral de 3 datos.
def datosAlejados():
    #Definimos las variables necesarias
    conteoFilas = 0
    okFilas = False
    okColumnas = False
    conteoColumnas = 0
    datosFuera = []
    #Recorremos el dataframe
    for i in range(nfil):
        for j in range(ncol):
            if(pd.isna(df.iloc[i,j])==False): #Si hay una celda no vacia
                for k in range(nfil): #Recorremos su fila
                    if(pd.isna(df.iloc[k,j])==False): 
                        conteoFilas+=1
                    #Si hay mas de 3 celdas con dato en su fila 
                    if conteoFilas>=2:
                        okFilas=True
                        break
                conteoFilas=0
                for z in range(ncol): #Recorremos su columna
                    if(pd.isna(df.iloc[i,z])==False): 
                        conteoColumnas+=1
                    if conteoColumnas>=2:
                        okColumnas=True
                        break
                conteoColumnas=0
                if okFilas!=True or okColumnas!=True:
                    datosFuera.append([i,j,df.iloc[i,j]])
                okFilas = False
                okColumnas = False
    return datosFuera

def valoresRepetidos():
    conteoTotalRepetidos = []
    for columna in df.columns:
        valores = df[columna].value_counts()
        if len(valores) >= 1:
            valor_mas_repes = valores.index[0]
            repeticiones_valor = valores.loc[valor_mas_repes]
            valoresMasRepes.append([valor_mas_repes, repeticiones_valor])
            conteoTotalRepetidos.append(valores)
        else:
            valoresMasRepes.append(None)
            conteoTotalRepetidos.append(None)
    return conteoTotalRepetidos



# CONJUNTO DE FUNCIONES PARA EXAMINAR Y ANALIZAR VALORES

# FUNCION QUE HACE LA MEDIA DE LOS VALORES NUMÉRICOS DE LAS COLUMNAS
def calcularMedia(): 
    media = np.full(ncol, 0, dtype=float)
    for i in range(ncol):
        for j in range(nfil):
            if(arrNum[j][i] == True):
                try:
                    media[i]+=df.iloc[j,i]
                except:
                    media[i]+=0
    for i in range(ncol):
        if(media[i] != 0):
            media[i] = media[i]/cantNum[i]              
    return media.tolist()

# FUNCIÓN QUE DEVUELVE SI UN VALOR ES NUMÉRICO O NO
def es_numerico(valor):
    try:
        float(valor)
        return True
    except:
        return False

# FUNCIÓN QUE GUARDA EN UN ARRAY BOOLEANO LOS VALORES QUE SON NUMÉRICOS
def es_numerico_array():
    isNumeric = np.full((nfil,ncol), False, dtype=bool)
    for i in range(nfil):
        for j in range(ncol):
            dato = df.iloc[i, j]
            if(pd.isna(dato)==True):
                isNumeric[i][j] = False
            elif es_numerico(dato):
                isNumeric[i][j] = True
            else:
                isNumeric[i][j] = False
    return isNumeric.tolist()



def calcular_desviacion_tipica():
    desvTipica = np.full(ncol, 0, dtype=float)  # Usamos np.nan para indicar valores no calculados

    for i in range(ncol):
        try:
            if cantNum[i] != 0:  # Verificamos si hay algún numero en la columna
                num_values = df.iloc[:, i][np.array(arrNum)[:, i]]  # Filtramos los valores numéricos de la columna
                desvTipica[i] = num_values.std()  # Calculamos la desviación estándar
        except:
            desvTipica[i] = 0
    return desvTipica.tolist()
    


def convertir_valores_no_serializables_en_serializables(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')  # Convertir datetime a formato ISO 8601
    elif isinstance(value, np.datetime64):
        return value.astype(datetime).strftime('%Y-%m-%d') 
    elif isinstance(value, pd.Timestamp):
        return value.strftime('%Y-%m-%d')
    elif isinstance(value, np.int64):
        return int(value)
    elif isinstance(value, np.ndarray):
        return value.tolist()  # Convertir arrays de NumPy a listas de Python
    elif isinstance(value, set):
        return list(value)  # Convertir conjuntos a listas
    elif isinstance(value, complex):
        return str(value)  # Convertir números complejos a strings
    else:
        return value


def mediaGeneral():
    if (len(medias) == 0):
        return 0; #Devuelve 0 si el array está vacío para evitar la división por cero.
    suma = sum(medias)
    media = suma / len(medias)
    return media

def obtener_tipos_de_datos():
    tipos_de_datos = []

    for fila in df.values:
        fila_tipos = []

        for valor in fila:
            tipo = type(valor)
            if tipo == int:
                fila_tipos.append("Integer")
            elif tipo == float:
                fila_tipos.append("Float")
            elif tipo == str:
                fila_tipos.append("String")
            elif tipo == bool:
                fila_tipos.append("Booleano")
            elif tipo == pd.Timestamp:
                fila_tipos.append("Fecha")
            elif tipo == np.datetime64:
                fila_tipos.append("Fecha")
            elif tipo == datetime:
                fila_tipos.append("Fecha")
            else:
                fila_tipos.append(str(tipo))  # Otros tipos de datos

        tipos_de_datos.append(fila_tipos)

    return tipos_de_datos


#---------------------------------------------------------------------------------------------MAIN-------------------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Debe proporcionar la ruta del archivo como argumento.")
    else:
        df_file = sys.argv[1]
        #codificacion = 'utf-8'  # Reemplaza con la codificación correcta si la conoces
        #contenido_archivo = leer_archivo_con_codificacion(ruta_archivo, codificacion)
        df = pd.read_excel(df_file)

        nfil = df.shape[0]
        ncol = df.shape[1]
        nCeldasTotales = nfil*ncol
        valoresMasRepes = []
        valoresMasRepesInt = []
        tiposColumnas = []

        #NO BORRAR
        numceldasVacias = celdasVacias()
        arrayDondeNan = numceldasVacias[0]              # ARRAY BOOLEANO DEL TAMAÑO DE DF PARA SABER SI ES VALOR NAN O NO, SI ES 1 TIENE DATO, SI ES 0 NAN
        arrayNumNanCol = numceldasVacias[1]             # ARRAY DEL NÚMERO DE VALORES NAN DE CADA COLUMNA
        arrayNumNanFil = celdasVaciasFila()             # ARRAY DEL NÚMERO DE VALORES NAN DE CADA FILA
        arrNum = es_numerico_array()                    # ARRAY DE BOOLEANOS DE SI ES NUMERO O NO
        cantNum = np.sum(arrNum, axis=0)                # CANTIDAD DE NÚMEROS EN EL DF
        desvTipica = calcular_desviacion_tipica()       # ARRAY CON DEVIACIÓN TÍPICA DE CADA COLUMNA CON ALGÚN NÚMERO
        gradoCompletitud = calcularCompletitud()        # GRADO DE COMMPLETITUD COMPARANDO CELDAS VACÍAS CON EL TOTAL DE CELDAS
        datosRepetidos = valoresRepetidos()             # CUANTAS VECES SE REPITE CADA VALOR EN CADA COLUMNA
        medias = calcularMedia()                        # MEDIA DE LAS COLUMNAS NUMÉRICAS
        mediadeMedias = mediaGeneral()                  # MEDIA DE MEDIAS
        tipoDatos = obtener_tipos_de_datos()
        #NO BORRAR

        # Cambiar los valores de int64 a int en la variable valoresMasRepes
        for item in valoresMasRepes:
            if item is not None:
                converted_item = [convertir_valores_no_serializables_en_serializables(item[0]), convertir_valores_no_serializables_en_serializables(item[1])]
                valoresMasRepesInt.append(converted_item)
            else:
                valoresMasRepesInt.append(None)


        processed_array = []
        processed_array.append(ncol)
        processed_array.append(nfil)
        processed_array.append(cantNum.tolist())
        processed_array.append(medias)
        processed_array.append(valoresMasRepesInt)
        processed_array.append(numceldasVacias)
        processed_array.append(gradoCompletitud)
        processed_array.append(desvTipica)
        processed_array.append(mediadeMedias)
        processed_array.append(tipoDatos)
        processed_array.append(df.columns.tolist())
        
            
        
        
        
        #processed_array.append(df_json)
        
        print(json.dumps(processed_array))
        
        # resultado = analizar_calidad_de_datos(ruta_archivo)
        #print(resultado)