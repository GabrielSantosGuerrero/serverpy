import threading
import csv
import requests
from queue import Queue
import time
import random as rd
from conectaBD import db

NUM_WORKERS = 5 #cantidad de hilos a ejecutar 
hilos = [] #vector de hilos
conn = db()

name = "Historial.csv"
url = "http://779482d99530.ngrok.io"
nombre = "AlexisPC"+str(rd.randint(0,10))
inicio = 0 
fin = rd.randint(5,10)

#consumidor
def comprobar(i,queue,nombre):
    print("Comprobar.............")
    while True:
        time.sleep(1)
        item = queue.get() #toda la linea csv
        resp =requests.get(url+"?id="+str(item[0])) # peticion al servidor, insertar el csv, consulta al servidor 
        
        if( resp.status_code == 200): # si regresa un 200 el server ingresa a la base el dato
            conn.ingresadatos("insert into \"proyectoA\" values({},'{}','{}','{}','{}','{}','{}','{}','{}')".format(str(item[0]),str(item[1]),str(item[2]),str(item[3]),str(item[4]),str(item[5]),str(item[6]),str(item[7]),str(nombre)))
            print("Inserta PC {} hilo {} valor: {} ...".format(str(nombre),i,str(item[0])))
        else:
            print("No inserto PC {} hilo {} valor: {}".format(str(nombre),i,str(item[0])))
        
        queue.task_done()



#productor
def lecturacsv(queue): #lee el csv interactua 
    with open(name, 'r', encoding = "utf-8") as csvfile:
      leer = csv.reader(csvfile, delimiter=',')
      for x,linea in enumerate(leer):
          if x >= inicio and x < fin:
            queue.put(linea) # inserta ese dato a la cola, toda la linea 
            time.sleep(1) #ordenar 
          if x == fin:
              break
            

        
    

if __name__ == "__main__":
    queue = Queue() # vector primero que entra primero que sale 
    hilos.append(threading.Thread(target=lecturacsv,args=(queue,))) #vector de hilos ,entra un hilo, lecturacsv=productor 

    for i in range(NUM_WORKERS): #hilos simultaneos 
        hilos.append(threading.Thread(target=comprobar,args=(i,queue,nombre))) #comprobar es el consumidor 
        #sirve la para la sincronizacion entre el hilo productor e hilo consumidor, hilo consumdir consulta si puedo o no insertar a la base 
    for i in hilos:
        i.start()
    
    for i in hilos:
        i.join()
        