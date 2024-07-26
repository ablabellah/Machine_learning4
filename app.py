from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Charger le modèle de prédiction sauvegardé
model = pickle.load(open('Customer_Churn_Prediction.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        CreditScore = int(request.form['CreditScore'])
        Age = int(request.form['Age'])
        Tenure = int(request.form['Tenure'])
        Balance = float(request.form['Balance'])
        NumOfProducts = int(request.form['NumOfProducts'])
        HasCrCard = int(request.form['HasCrCard'])
        IsActiveMember = int(request.form['IsActiveMember'])
        EstimatedSalary = float(request.form['EstimatedSalary'])
        
        # Gestion des données catégorielles
        Geography = request.form['Geography']
        if Geography == 'Germany':
            Geography_Germany = 1
            Geography_Spain = 0
            Geography_France = 0
        elif Geography == 'Spain':
            Geography_Germany = 0
            Geography_Spain = 1
            Geography_France = 0
        else:
            Geography_Germany = 0
            Geography_Spain = 0
            Geography_France = 1

        Gender = request.form['Gender']
        if Gender == 'Male':
            Gender_Male = 1
            Gender_Female = 0
        else:
            Gender_Male = 0
            Gender_Female = 1

        # Prédire le churn
        prediction = model.predict([[CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Geography_Germany, Geography_Spain, Gender_Male]])
        
        if prediction == 1:
            return render_template('index.html', prediction_text="The Customer will leave the bank")
        else:
            return render_template('index.html', prediction_text="The Customer will not leave the bank")

if __name__ == "__main__":
    app.run(debug=True)
