from flask import Flask,render_template,redirect,request,url_for
import requests
from flask_pymongo import PyMongo

app=Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/weather_data'
mongo=PyMongo(app)

@app.route("/",methods=["POST","GET"])
def home():
    data=[]
    item=mongo.db.datas
    for i in item.find():
        data.append(i)
    city=None
    if request.method=="POST":
       mongo.db.datas.delete_many({})

       city=request.form.get("city")
       url=f"http://api.weatherstack.com/current?access_key=644a5a6c34d6bd077949c9dd1c7857bb&query={city}"
       response=requests.get(url)
       data=response.json()
       country=data["location"]["country"]
       region=data["location"]["region"]
       lat=data["location"]["lat"]
       lon=data["location"]["lon"]
       lot=data["location"]["localtime"]
       temp=data["current"]["temperature"]
       wed=data["current"]["wind_speed"]
       pressure=data["current"]["pressure"]
       feelslike=data["current"]["feelslike"]
       humidity=data["current"]["humidity"]
       uv_index=data["current"]["uv_index"]
       visibility=data["current"]["visibility"]
       des=data["current"]["weather_descriptions"][0]
       
       coll = mongo.db.datas
       coll.insert_one({"city":city,"country":country,"region":region,"lat":lat,"lon":lon,"lot":lot,"temp":temp,"wed":wed,"pressure":pressure,"feelslike":feelslike,"humidity":humidity,"uv_index":uv_index,"visibility":visibility,"des":des})
       return redirect(url_for('home'))
    

    return render_template("index.html",data=data)


if __name__=="__main__":
    app.run(debug=True)
