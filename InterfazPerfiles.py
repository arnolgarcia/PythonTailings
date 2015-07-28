# Metodos para la interfaz grafica para subir archivos de perfiles
#__author__ = 'Arnol'

import os
from osgeo import ogr,osr
from Tkinter import *

def UploadPerfil(path,proyecto,connStr):
    files = []
    #Lista con todos los archivos del directorio:
    ficheros = os.listdir(path)

    #Crea una lista de los ficheros jpg que existen en el directorio y los incluye a la lista.
    for fichero in ficheros:
        (nombreFichero, extension) = os.path.splitext(fichero)
        if(extension == ".txt"):
            perfil=nombreFichero.split(" ")
            print perfil
            dataPerfil=creaDatosPerfil(path+fichero,perfil[1],proyecto)
            tablename=nombreFichero+" " + proyecto
            CargaArchivoPerfil(connStr,tablename,dataPerfil,len(dataPerfil))
            files.append(nombreFichero+extension)
#   Fin de la funcion


def CargaArchivoPerfil(connStr,table,datos,N):
    # Abrir la coneccion
    conn = ogr.Open(connStr)
    # create the spatial reference, WGS84
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    # Crear la tabla con los campos
    layer = conn.CreateLayer(table, srs, ogr.wkbPoint, ['OVERWRITE=YES'] )
    #field_name = ogr.FieldDefn("PointID", ogr.OFTString)
    #field_name.SetWidth(24)
    #layer.CreateField(field_name)
    layer.CreateField(ogr.FieldDefn("distancia", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("profundidad", ogr.OFTReal))
    #layer.CreateField(ogr.FieldDefn("Fecha", ogr.OFTDateTime))
    #layer.CreateField(ogr.FieldDefn("Perfil", ogr.OFTReal))
    #layer.CreateField(ogr.FieldDefn("Pendiente", ogr.OFTReal))

    # Leer archivo y cargarlo en BD
    for i in range(N):
        # create the feature
        feature = ogr.Feature(layer.GetLayerDefn())
        # Set the attributes using the values from the data
        feature.SetField("distancia", datos[i][0])
        feature.SetField("profundidad", datos[i][1])
        #feature.SetField("Fecha", datos[i][2])
        #feature.SetField("Perfil", datos[i][3])
        #feature.SetField("Pendiente", datos[i][4])
        # Crear layer en la BD
        layer.CreateFeature(feature)
        # Destroy the feature to free resources
        feature.Destroy()
    # eliminar el TimeZone del campo 'fecha'
    #sql = 'ALTER TABLE %s ALTER COLUMN %s TYPE timestamp(6);' %(table,"Fecha")
    #sql = 'ALTER TABLE %s DROP COLUMN "wkb_geometry","ogc_fid";' %(table)
    #conn.ExecuteSQL(sql)
    # Destroy the data source to free resources
    conn.Destroy()
#   Fin de la funcion


def creaDatosPerfil(filename,perfil,fecha):
    datos = []
    file=open(filename)
    line=file.readline()
    # Encabezado
    line=file.readline()
    #lastX=float(line.split("\t")[0])
    #lastY=float(line.split("\t")[1])
    #print lastY,lastX
    while (line != "" and line!="\n"): # Termina si llega al final del archivo o si hay una linea en blanco
        Line=line.split("\t")
        x=float(Line[0])
        y=float(Line[1])
        #f=fecha
        #p=perfil
        #m=0
        #if x!=lastX:
        #    m=(y-lastY)/(x-lastX)
        #datos.append([x,y,f,p,m])
        datos.append([x,y])
        #lastX=x
        #lastY=y
        line=file.readline()
    file.close()
    return datos
#   Fin de la funcion




# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------

dbServer = "152.231.85.226"
dbName = "Testing_ETL"
dbUser = "postgres"
dbPW = "admin"
connString = "PG: host=%s dbname=%s user=%s password=%s" %(dbServer,dbName,dbUser,dbPW)


#dir = "C:/Users/Arnol/Desktop/TestPerfiles/07.07.2015/"
#proyect = '07_07_2015'
#UploadPerfil(dir,proyect,connString)


# Interfaz grafica
def IGcargaArchivos():
    try:
        newRuta = formatoRuta(rutaP.get())
        UploadPerfil(newRuta,fechaP.get(),connString)
    except IndexError:
        print "Ingresar ruta"
# Fin funcion

def formatoRuta(rutaAux):
    aux=rutaAux.replace("\\","/")
    if aux[-1]!="/":
        aux=aux+"/"
    return aux
#Fin funcion


# Inicializar Interfaz Gráfica
w = Tk()

# Titulo de la ventana
l = Label(w, text='Cargador archivos de perfiles')
l.grid(row=1,column=2)
# Espacio en blanco
aux = Label(w, text='').grid(row=2,column=2)

# Extrae ruta donde estan los archivos
l3 = Label(w, text='Ruta:')
l3.grid(row=3,column=1)
rutaP = StringVar()
e3 = Entry(w, textvariable=rutaP)
e3.grid(row=3,column=2)

# Extrae nombre (fecha) del proyecto
l4 = Label(w, text='Fecha del proyecto (dd_mm_aaaa):')
l4.grid(row=4,column=1)
fechaP = StringVar()
e4 = Entry(w, textvariable=fechaP)
e4.grid(row=4,column=2)
b4 = Button(w, text='Cargar archivos',command=IGcargaArchivos)
b4.grid(row=4,column=3)

exitB = Button(w, text='Salir', command=exit)
exitB.grid(row=5,column=2)

w.mainloop()