import os
import pickle
from flask import Flask,redirect,url_for,render_template,request,session
from flask import Flask,render_template,url_for,request
import sqlite3
UPLOAD_FOLDER = os.path.join('static', 'images')
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'This is your secret key to utilize session in Flask'

# Load models
with open('models/chilli.pkl', 'rb') as f:
    chili_type_model = pickle.load(f)

with open('models/chilli2.pkl', 'rb') as f:
    yield_model = pickle.load(f)

with open('models/greenchilli.pkl', 'rb') as f:
    gchili_type_model = pickle.load(f)

with open('models/greenchilli2.pkl', 'rb') as f:
    gyield_model = pickle.load(f)
import pandas as pd

# Load the dataset (replace 'your_data.csv' with your actual file)
df = pd.read_csv('newred.csv')
df1 = pd.read_csv('new1.csv')

def get_nutrients(chili_name, acres):
    # Filter the DataFrame based on chili type and acres
    row = df[(df['Chili Type'] == chili_name) & (df['Acres'] == acres)]
    
    if not row.empty:
        # Extract values for Nitrogen, Phosphorus, and Potassium
        ph=row['Ph'].values[0]
        nitrogen = row['Nitrogen'].values[0]
        phosphorus = row['Phosphorus'].values[0]
        potassium = row['Potassium'].values[0]
        water = row['WaterRequirement'].values[0]
        space= row['SpacingBetweenPlants'].values[0]
        
        return ph,nitrogen, phosphorus, potassium,water,space
    else:
        return "No data found for the given chili type and acres."
def get_nutrients1(chili_name, acres):
    # Filter the DataFrame based on chili type and acres
    row = df1[(df1['Chili Type'] == chili_name) & (df1['Acres'] == acres)]
    
    if not row.empty:
        # Extract values for Nitrogen, Phosphorus, and Potassium
        ph=row['Ph'].values[0]
        nitrogen = row['Nitrogen'].values[0]
        phosphorus = row['Phosphorus'].values[0]
        potassium = row['Potassium'].values[0]
        water = row['WaterRequirement'].values[0]
        space= row['SpacingBetweenPlants'].values[0]
        
        return ph,nitrogen, phosphorus, potassium,water,space
    else:
        return "No data found for the given chili type and acres."

# Mapping for chili types and soil types
chili_types = ["Guntur Sannam", "Guntur Teja", "334  Chili", "Byadgi Chili", "Ramnad Mundu"]
soil_types = ["Black Cotton", "Red Sandy Loam", "Well-Drained", "Well-Drained Clay"]
chili_types1 = ["Guntur Sannam Green", "Guntur Teja Green", "334 Green Chili", "Byadgi Green Chili", "Ramnad Green Mundu"]
# soil_types = ["Black Cotton", "Red Sandy Loam", "Well-Drained", "Well-Drained Clay"]

# Fertilizer suggestions based on chili type
fertilizer_suggestions = {
    "Guntur Sannam": ["NPK (10:20:20)", "Calcium Ammonium Nitrate (CAN)"],
    "Guntur Teja": ["Ammonium Sulphate (AS)", "Potassium Chloride (MOP)"],
    "334 Chili": ["Urea", "Diammonium Phosphate (DAP)"],
    "Byadgi Chili": ["Magnesium Sulphate (MgSO4)", "Micronutrient fertilizer (e.g. Boron, Copper, Zinc)"],
    "Ramnad Mundu": ["Single Super Phosphate (SSP)", "Ammonium Nitrate (AN)"]
}

fertilizer_suggestions1 = {
    "Guntur Sannam Green": ["Organic fertilizer (e.g. compost, manure)", "NPK (20:20:20)"],
    "Guntur Teja Green": ["Phosphorus-rich fertilizer (e.g. DAP, MAP)", "Potassium Nitrate (KNO3)"],
    "334 Green Chili": ["Nitrogen-rich fertilizer (e.g. Urea, Ammonium Nitrate)", "Micronutrient fertilizer (e.g. Iron, Manganese, Copper)"],
    "Byadgi Green Chili": ["Calcium-rich fertilizer (e.g. Calcium Nitrate, Lime)", "Sulphur-rich fertilizer (e.g. Ammonium Sulphate, Elemental Sulphur)"],
    "Ramnad Green Mundu": ["Balanced fertilizer (e.g. NPK 15:15:15)", "Foliar fertilizer (e.g. Urea, DAP)"]
}

# Fertilizer suggestions based on chili type
Pestisides_suggestions = {
    "Guntur Sannam": ["Chlorpyrifos", "Cypermethrin"],
    "Guntur Teja": ["Deltamethrin", "Profenofos"],
     "334 Chili": ["Quinalphos", "Lambda-cyhalothrin"],
    "Byadgi Chili": ["Monocrotophos", "Fenvalerate"],
    "Ramnad Mundu": ["Phosalone", "Triazophos"]
}
Pestisides_suggestions1 = {
     "Guntur Sannam Green": ["Neem oil","Imidacloprid"],
    "Guntur Teja Green": ["Thiamethoxam", "Dinotefuran"],
     "334 Green Chili": ["Clothianidin", "Acetamiprid"],
    "Byadgi Green Chili": ["Fipronil", "Spinosad"],
    "Ramnad Green Mundu": ["Emamectin benzoate", "Lufenuron"]

}

Disease_suggestions = {
    "Guntur Sannam": ["Powdery Mildew", "Fusarium Wilt"],
    "Guntur Teja": ["Bacterial Leaf Spot", "Cercospora Leaf Spot"],
    "334 Chili": ["Anthracnose", "Root Rot"],
    "Byadgi Chili": ["Leaf Curl", "Fruit Rot"],
    "Ramnad Mundu": ["Downy Mildew", "Bacterial Wilt"]
}
Disease_suggestions1 = {
    "Guntur Sannam Green": ["Tobacco Mosaic Virus", "Bacterial Leaf Spot"],
    "Guntur Teja Green": ["Powdery Mildew", "Leaf Miner"],
    "334 Green Chili": ["Cercospora Leaf Spot", "Fusarium Wilt"],
    "Byadgi Green Chili": ["Anthracnose", "Root Rot"],
    "Ramnad Green Mundu": ["Downy Mildew", "Leaf Curl"]
}
chili_type_images = {
    'Guntur Sannam': 'images/red_sanam.jpg',
    'Guntur Teja': 'images/red_teja.jpg',
    '334  Chili': 'images/red_334.jpg',
    'Byadgi Chili': 'images/red_byadgi.jpg',
    'Ramnad Mundu': 'images/red_ramnad.jpg'
}
chili_type_images1 = {
    'Guntur Sannam Green': 'images/green_sanam.jpg',
    'Guntur Teja Green': 'images/green_teja.jpg',
    '334 Green Chili': 'images/green_334.jpg',
    'Byadgi Green Chili': 'images/green_byadgi.jpg',
    'Ramnad Green Mundu': 'images/green_chili.jpg'
}
@app.route("/")
@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/passhome")
def passhome():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register",methods=["POST","GET"])
def register():
    
    if request.method=="POST":
        name=request.form["firstname"]
        lname=request.form["lastname"]
        uemail=request.form["email"]
        Password=request.form["password"]
        print(name,lname,uemail,Password)
        
        con=sqlite3.connect("test1.db")
        print(con)
        cur=con.cursor()
        a=f"select email from emp where email='{uemail}'"
        cur.execute(a)
        result=cur.fetchone()
        if result!=None:
            return "email alredy registered"
        else:
        #a="create table emp(name varchar(100),lastname varchar(100),email varchar(100),password varchar(100))"
            cur.execute("INSERT INTO emp('name', 'lastname', 'email', 'password') VALUES (?,?,?,?)",(name,lname,uemail,Password))
            con.commit()
            con.close()
            return render_template("login.html")
    return render_template("register.html")
 

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        uemail=request.form["email"]
        upassword=request.form["password"]
        print(uemail,upassword)
        import sqlite3
        con=sqlite3.connect("test1.db")
        cur=con.cursor()
        a=f"select * from emp where email='{uemail}' and password ='{upassword}'"
        cur.execute(a)
        result=cur.fetchone()
        print("database",result)
        sr=str(result[0])+" "+str(result[1])
        if result==None:
            return "please enter valid details"
        else:
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    return redirect(url_for("main"))
  
@app.route("/home")
def home():
	return render_template('home.html')

@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        acres = int(request.form['acres'])
        cost = int(request.form['cost'])
        soil_type = int(request.form['soil_type'])

        # Predict chili type
        chili_type_encoded = chili_type_model.predict([[acres, cost, soil_type]])[0]
        #[n] where n=(0,1,2,3)
        chili_type = chili_types[chili_type_encoded]

        # Predict yield
        yield_pred = yield_model.predict([[acres, cost, soil_type, chili_type_encoded]])[0]

        # Suggest fertilizers
        fertilizers = fertilizer_suggestions[chili_type]

        return render_template('predict_chili_type.html', chili_type=chili_type, fertilizers=fertilizers, title="Predicted Chili Type")

    return render_template('input.html', title="Input")

@app.route('/input1')
def input1():
    if request.method == 'POST':
        acres = int(request.form['acres'])
        cost = int(request.form['cost'])
        soil_type = int(request.form['soil_type'])

        # Predict chili type
        chili_type_encoded = chili_type_model.predict([[acres, cost, soil_type]])[0]
        chili_type = chili_types1[chili_type_encoded]

        # Predict yield
        yield_pred = yield_model.predict([[acres, cost, soil_type, chili_type_encoded]])[0]

        # Suggest fertilizers
        fertilizers = fertilizer_suggestions1[chili_type]

        return render_template('predict_chili_type.html', chili_type=chili_type, fertilizers=fertilizers, title="Predicted Chili Type")

    return render_template('input1.html', title="Input")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        print("okkkkkkkkkkk")
        acres = int(request.form['acres'])
        cost = int(request.form['cost'])
        soil_type = int(request.form['soil_type'])
        print(acres, cost, soil_type)
        # Predict chili type
        chili_type_encoded = chili_type_model.predict([[acres, cost, soil_type]])[0]
        print(chili_type_encoded)
        chili_type = chili_types[chili_type_encoded]
        print(chili_type)
        # Predict yield
        yield_pred = yield_model.predict([[acres, cost, soil_type, chili_type_encoded]])[0]
        yield_pred=round(yield_pred,2)
        # Suggest fertilizers
        fertilizers = fertilizer_suggestions[chili_type]
        Pestisides=Pestisides_suggestions[chili_type]
        print(Pestisides,"******************")
        Disease=Disease_suggestions[chili_type]
        print(Disease,"******************")
        chili_type_image = chili_type_images[chili_type]
        
        # Example usage
        
        result = get_nutrients(chili_type, acres)
        Ph=result[0]
        nitrogen=result[1]
        phosphorus=result[2]
        potassium=result[3]
        water=result[4]
        space=result[5]


        return render_template('predict_chili_type.html',ph=Ph,nitrogen=nitrogen, phosphorus=phosphorus, potassium=potassium,water=water,space=space,chili_type_image=chili_type_image, chili_type=chili_type,Pestisides=Pestisides,Disease=Disease, fertilizers=fertilizers,yield_pred=yield_pred, title="Predicted Chili Type")

    
    return render_template('input.html', title="Input")

@app.route('/predict1', methods=['GET', 'POST'])
def predict1():
    if request.method == 'POST':
        print("okkkkkkkkkkk")
        acres = int(request.form['acres'])
        cost = int(request.form['cost'])
        soil_type = int(request.form['soil_type'])
        print(acres, cost, soil_type)
        # Predict chili type
        chili_type_encoded = gchili_type_model.predict([[acres, cost, soil_type]])[0]
        print(chili_type_encoded)
        chili_type = chili_types1[chili_type_encoded]
        print(chili_type)
        # Predict yield
        yield_pred = gyield_model.predict([[acres, cost, soil_type, chili_type_encoded]])[0]
        yield_pred=round(yield_pred,2)
        # Suggest fertilizers
        fertilizers1 = fertilizer_suggestions1[chili_type]
        Pestisides1=Pestisides_suggestions1[chili_type]
        print(Pestisides1,"******************")
        Disease1=Disease_suggestions1[chili_type]
        print(Disease1,"******************")
        chili_type_image1 = chili_type_images1[chili_type]

        result = get_nutrients1(chili_type, acres)
        Ph=result[0]
        nitrogen=result[1]
        phosphorus=result[2]
        potassium=result[3]
        water=result[4]
        space=result[5]
        print(f"Ph: {result[0]}, Nitrogen: {result[1]}, Phosphorus: {result[2]}, Potassium: {result[3]},Water: {result[0]},Sace: {result[0]}")

        return render_template('predict_chili_type1.html',ph=Ph,nitrogen=nitrogen, phosphorus=phosphorus, potassium=potassium,water=water,space=space,chili_type_image1=chili_type_image1, chili_type=chili_type,Pestisides1=Pestisides1, fertilizers=fertilizers1,yield_pred=yield_pred, title="Predicted Chili Type",Disease1=Disease1)
            
    return render_template('input1.html', title="Input")


if __name__ == "__main__":
        app.run(debug=True)
 
