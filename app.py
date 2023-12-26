from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import pickle
import sklearn
from sklearn.preprocessing import StandardScaler    # standardizing mean = 0, SD =1
import mysql.connector

app = Flask(__name__, template_folder='template')
model = pickle.load(open('random_forest_model_upd.pkl', 'rb'))   # reads binay

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'majorproject'

mysql = MySQL(app)

@app.route('/',methods=['GET'])     #end point
def Home():
    return render_template('index.html')



@app.route('/client', methods=['GET','POST'])  # HTTPS methods

def client_form():

    if request.method=='POST':

        name= request.form['name']
        email= request.form['email']
        carName= request.form['carName']
        carPrice= request.form['carPrice']
        address = request.form['address']
        phno = request.form['phno']

        cur= mysql.connection.cursor()      #cursor object allow to run sql query

        cur.execute("insert into client1(name,email,car,price,address,phno)values(%s,%s,%s,%s,%s,%s)",(name,email,carName,carPrice,address,phno))
        mysql.connection.commit()   #if error occured during insertion, commit will not reach.
        cur.close()
        return render_template('success.html')

    elif request.method=='GET':
        return render_template('client.html')

standard_to = StandardScaler()  # feature scaling for contributing all features equally.

@app.route("/predict", methods=['POST'])

def predict():
    Fuel_Type_Diesel=0

    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']

        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1          #encoding/ compatibility
            Fuel_Type_Diesel=0

        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1

        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0

        Year= 2023-Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']

        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1

        else:
            Seller_Type_Individual=0	

        Transmission_Mannual=request.form['Transmission_Mannual']

        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {} Lakh".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=False)
    
# Encoding: = Categorical variables need to be converted into numerical form for the model to understand and use them effectively