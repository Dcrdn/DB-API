from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from flask_cors import CORS
from tweets import *
import random
reload(sys)  
sys.setdefaultencoding('utf8')

app = Flask(__name__)
CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Usuarios
#hashtags, --> pie    hashtags(user)
#sentimiento, -->pie  analisis(user)
#fechas , --> grafica de lineas.. getDates(user)
#most common words getCommonWords(user)
#posted by day of the week getDias(user)

#user="Diego_crdn"

colores=['rgba(255, 99, 132, 0.6)','rgba(54, 162, 235, 0.6)','rgba(255, 206, 86, 0.6)','rgba(75, 192, 192, 0.6)','rgba(153, 102, 255, 0.6)','rgba(255, 159, 64, 0.6)','rgba(255, 99, 132, 0.6)']

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/sentimientos")#works -->  pie
def sentimientos(): #works yasta
    user = request.args.get('username')
    info=analisis(user)
    info=json.loads(info)
    data=[info["positive"], info["negative"], info["neutral"]]
    backgroundColor=["rgba(255, 99, 132, 0.6)", "rgba(54, 162, 235, 0.6)", "rgba(255, 206, 86, 0.6)"]
    labels=["positive", "negative", "neutral"]
    result=convertToJson(backgroundColor, data, labels)
    return result

@app.route("/hashtags") #works
def hashtags():
    user = request.args.get('username')
    info= batmanHashtags(user)
    return info

@app.route("/dates") #works #pie
def dates():
    user = request.args.get('username')
    info=getDates(user) 
    info2=json.loads(info)
    data=[]
    backgroundColor=[]
    labels=[]
    for key,value in info2.items():
      labels.append(key)
      data.append(value)
      backgroundColor.append(random.choice(colores))
    result=convertToJson(backgroundColor, data, labels)
    return result

@app.route("/commonWords")
def commonWords2():
    user = request.args.get('username')
    info=getCommonWords(user)
    info=json.loads(info)
    data=[]
    backgroundColor=[]
    labels=[]
    for key,value in info.items():
      labels.append(key)
      data.append(value)
      backgroundColor.append(random.choice(colores))
    result=convertToJson(backgroundColor, data, labels)
    return result

@app.route("/dias")
def dias():
    user = request.args.get('username')
    info2=getDias(user)
    info=json.loads(info2)
    data=[]
    backgroundColor=[]
    labels=[]
    temp={"1":"Lunes", "2":"Martes","3":"Miercoles","4":"Jueves","5":"Viernes","6":"Sabado","7":"Domingo"}
    print("llega")
    for key,value in info.items():
      print("entra1")
      labels.append(temp[key])
      data.append(value)
      backgroundColor.append(random.choice(colores))
    fun=convertToJson(backgroundColor,data,labels)
    return fun

if __name__ == '__main__':
    app.run()


"""
      chartData:{
        labels: ['Boston', 'Worcester', 'Springfield', 'Lowell', 'Cambridge', 'New Bedford'],
        datasets:[
          {
            label:'Population',
            data:[
              617594,
              181045,
              153060,
              106519,
              105162,
              95072
            ],
            backgroundColor:[
              'rgba(255, 99, 132, 0.6)',
              'rgba(54, 162, 235, 0.6)',
              'rgba(255, 206, 86, 0.6)',
              'rgba(75, 192, 192, 0.6)',
              'rgba(153, 102, 255, 0.6)',
              'rgba(255, 159, 64, 0.6)',
              'rgba(255, 99, 132, 0.6)'
            ]
          }
        ]
      }
"""