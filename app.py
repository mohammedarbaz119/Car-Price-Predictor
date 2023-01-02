from flask import Flask, render_template, redirect, url_for, request
import numpy as np
import pandas as pd
import json
from sklearn import metrics
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = "ARBAZuddin qureshi"

# dataset = pd.read_csv('./CarPrice_Assignment.csv')

# X = dataset.drop(['price'], axis=1)
# X = X.drop(['car_ID'], axis=1)
# X['Car_Company'] = X['CarName'].apply(lambda x: x.split(" ")[0])
# car_companies = set([i for i in X['Car_Company']])
# X = X.drop(['CarName'], axis=1)
# categorical_set = X.select_dtypes(include=['object'])
# dummies = pd.get_dummies(categorical_set)
# X = X.drop([*categorical_set], axis=1)
# X = pd.concat([X, dummies], axis=1)


# y = dataset['price']

# Xt, Xtest, yt, ytest = train_test_split(X, y, test_size=0.2, random_state=65)
# lr = LinearRegression()
# lr.fit(Xt, yt)
# print(ytest)

# c = lr.predict(Xtest)
# print(f"error is {metrics.r2_score(ytest,c)}")
# d = lr.predict([Xtest.iloc[1]])
# print(d)


class PriceForm(FlaskForm):
    company = SelectField("select the car company", choices=car_companies)
    horsepower = StringField("horsepower?", [DataRequired()])
    wheelbase = StringField("wheelbase ?", [DataRequired()])
    carlength = StringField("length of the car ?", [DataRequired()])
    carwidth = StringField("width of the car ?", [DataRequired()])
    carheight = StringField("car height ?", [DataRequired()])
    curbweight = StringField("curb weight of car ?", [DataRequired()])
    enginesize = StringField("size of engine ?", [DataRequired()])
    boreratio = StringField("bore ratio ?", [DataRequired()])
    stroke = StringField("stroke ?", [DataRequired()])
    compressionratio = StringField("compression ratio ?", [DataRequired()])
    peakrpm = StringField("peak RPM ?", [DataRequired()])
    citympg = StringField("city mileage ?", [DataRequired()])
    highwaympg = StringField("highway mileage ?", [DataRequired()])
    symboling = SelectField("select symboling of car?",
                            choices=[-1, -2, 1, 2, 3])
    fuel_type = SelectField("select the fuel type", choices=['diesel', 'gas'])
    doornumbers = SelectField("Select the no of doors of car", choices=[2, 4])
    aspiration = SelectField("aspiration type?", choices=['std', 'turbo'])
    carbody = SelectField("select the body type of car", choices=[
                          'hardtop', 'hatchback', 'sedan', 'wagon', 'convertible'])
    drivewheel = SelectField("select the drivewheel type",
                             choices=['4wd', 'fwd', 'rwd'])
    enginelocation = SelectField(
        "select the location of engine", choices=['front', 'rear'])
    enginetype = SelectField("select the engine type", choices=[
                             'dohc', 'dohcv', 'l', 'ohc', 'ohcf', 'ohcv', 'rotor'])
    cylindernumber = SelectField(
        'select the number opf cylinders in engine', choices=[2, 3, 4, 5, 6, 8, 12])
    fuelsystem = SelectField('select the fuel system', choices=[
                             '1bbl', '2bbl', '4bbl', 'idi', 'mfi', 'mpfi', 'spdi', 'spfi'])
    submit = SubmitField("submit")


floatcols = {'wheelbase', 'carlength', 'carwidth',
             'carheight', 'boreratio', 'stroke', 'compressionratio', 'enginesize', 'boreratio', 'peakrpm', 'citympg', 'highwaympg', 'horsepower', 'curbweight'}
selectnumcols = {'doornumbers': {2: 'two', 4: 'four'}, 'cylindernumber': {
    2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 8: 'eight', 12: 'twelve'}}


def is_int(n):
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n


def is_float(n):
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True

lr = pickle.load(open('LinearRegression.pkl','rb'))
@app.route('/', methods=['GET', 'POST'])
def pricer():
    form = PriceForm()

    if request.method == 'POST':
        l = {}
        for i in X.columns:
            l[i] = 0.0
        if form.validate_on_submit():

            for k, v in form.data.items():
                if (k == 'submit' or k == 'csrf_token'):
                    continue
                if (is_float(v)):
                    if (k in floatcols):
                        l[k] = float(v)
                    elif (k in list(selectnumcols.keys())[0]):
                        c = selectnumcols['doornumbers'][int(v)]
                        for i in range(18, 20):
                            if c in list(l.keys())[i]:
                                l[list(l.keys())[i]] = 1.0
                    elif (k in list(selectnumcols.keys())[1]):
                        c = selectnumcols['cylindernumber'][int(v)]
                        for i in range(37, 44):
                            if c in list(l.keys())[i]:
                                l[list(l.keys())[i]] = 1.0
                elif (is_int(v)):
                    l[k] = float(v)
                elif k == 'symboling':
                    l[k] = float(v)
                else:
                    for i in list(l.keys())[14:]:
                        if v in i:
                            l[i] = 1.0
                lrr = lr.predict([[*list(l.values())]])
            return render_template('index.html', form=PriceForm(), l=l, lrr=lrr)
    return render_template('index.html', form=form)
