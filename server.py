from flask import Flask,request
import time
import random

app = Flask(__name__)

items = []

@app.route('/',methods=['GET'])
def _():
    time.sleep(random.randint(6,10))  #peticiones pueda atender, tiempo de espera 
    return comprobar(request.values.get('id'))

def comprobar(id): #comprobar la consulta de cliente guardada en items #existe o no existe dentro del vector
    try:
        items.index(id) # id si encuentra ejecuta no se encuentra 
        return 'False',201
    except Exception as error:
        print(error)
        items.append(id)
        return 'True',200

if __name__ == '__main__':
  app.run(host='0.0.0.0') 
