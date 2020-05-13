## html : myWebsite,signup,login,error_login
## css : style,login
## font awesome : ==> in folder static
## database : database.json
# https://code.tutsplus.com/tutorials/charting-using-plotly-in-python--cms-30286
from flask import Flask, render_template, jsonify, redirect, url_for, request
import json
import joblib
import plotly
import plotly.graph_objs as go
import chart_studio.plotly as csp
import plotly.offline as py
import numpy as np
import pandas as pd

app = Flask(__name__)

with open('database.json') as dataku:
    data = json.load(dataku)

@app.route('/')
def home():
   return render_template('myWebsite.html')

## default GET
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        nam_l = request.form['nama_login']
        pwd_l = request.form['pass_login']
        
        for a in range(len(data)):
            if nam_l == data[a]['nama'] and pwd_l == data[a]['pass']:
                return redirect(url_for('main')) ##direct ke def main 
            elif a == len(data) - 1:
                return render_template('login.html')
            else:
                continue
    else:
        return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nam_s = request.form['nama_signup']
        pwd_s1 = request.form['pass_signup1']
        pwd_s2 = request.form['pass_signup2']
        if pwd_s1 == pwd_s2 :
            data.append({'nama': nam_s, 'pass': pwd_s1})
            y = json.dumps(data)
            json_data = open('database.json', 'w')
            json_data.write(y)
            return redirect(url_for('login'))
        else :
            return render_template('signup.html')

    else:
        return render_template('signup.html')

@app.route('/main')
def main():
    # Total Custemer Churn
    lab = telcom["Churn"].value_counts().keys().tolist()
    val = telcom["Churn"].value_counts().values.tolist()

    trace = go.Pie(labels = lab ,
                values = val ,
                marker = dict(colors =  [ '#54b6c8' ,'#969696'],
                line = dict(color = "white", width =  1.3)),
                hoverinfo = "label+value+text",
                hole = .6              
                )
    layout = go.Layout(dict(title = "Customer Churn in data"),
                            plot_bgcolor  = "rgba(0,0,0,0)",
                            paper_bgcolor = "rgba(0,0,0,0)",
                            annotations = [dict(text = f"Churning Customer",
                                                    font = dict(size = 15),
                                                    showarrow = False,
                                                    x = .5, y = .5)])
    ## gender
    male = telcom[telcom['gender'] == 'Male']
    female = telcom[telcom['gender'] == 'Female']
    x = round(telcom['gender'].value_counts()['Male']/telcom['gender'].value_counts().sum() * 100,2)
    y = round(telcom['gender'].value_counts()['Female']/telcom['gender'].value_counts().sum() * 100,2)
    
    trace1 = go.Pie(values  = male['Churn'].value_counts().values.tolist(),
                    labels  = male['Churn'].value_counts().keys().tolist(),
                    hoverinfo = "label+value+name",
                    domain  = dict(x = [0,.48]),
                    name    = "Male",
                    marker  = dict(line = dict(width = 2,color = "rgb(243,243,243)"),
                                   colors = ['#54b6c8','#969696']),
                    hole    = .6
                   )
    trace2 = go.Pie(values  = female['Churn'].value_counts().values.tolist(),
                    labels  = female['Churn'].value_counts().keys().tolist(),
                    hoverinfo = "label+value+name",
                    marker  = dict(line = dict(width = 2,color = "rgb(243,243,243)"),
                                   colors = ['#54b6c8','#969696']),
                    domain  = dict(x = [.52,1]),
                    hole    = .6,
                    name    = "Female" 
                   )


    layout1 = go.Layout(dict(title = f"Churning rate based on Gender",
                            plot_bgcolor  = "rgba(0,0,0,0)",
                            paper_bgcolor = "rgba(0,0,0,0)",
                            annotations = [dict(text = f"Male : {x}% ",
                                                font = dict(size = 13),
                                                showarrow = False,
                                                x = .18, y = .5),
                                           dict(text = f"Female : {y}%",
                                                font = dict(size = 13),
                                                showarrow = False,
                                                x = .83,y = .5
                                               )
                                          ]
                           )
                      ) 
    fig  = go.Figure(data = trace,layout = layout)
    fig1 = go.Figure(data = [trace1,trace2],layout = layout1)
    Plot = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    Plot1 = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)

    ### Visualize Based on Personal Info
    bin_cols= ['SeniorCitizen','Partner','Dependents','PaperlessBilling']
    def plot_pie2(column) :
        Yes = telcom[telcom[column] == 1]
        No = telcom[telcom[column] == 0]
        x = round(telcom[column].value_counts()[1]/telcom[column].value_counts().sum() * 100,2)
        y = round(telcom[column].value_counts()[0]/telcom[column].value_counts().sum() * 100,2)
        
        trace1 = go.Pie(values  = Yes['Churn'].value_counts().values.tolist(),
                        labels  = Yes['Churn'].value_counts().keys().tolist(),
                        hoverinfo = "label+value+name",
                        domain  = dict(x = [0,.48]),
                        name    = f"{column}",
                        marker  = dict(line = dict(width = 2,color = "rgb(243,243,243)"),
                                    colors = ['#54b6c8','#969696']),
                        hole    = .6
                    )
        trace2 = go.Pie(values  = No['Churn'].value_counts().values.tolist(),
                        labels  = No['Churn'].value_counts().keys().tolist(),
                        hoverinfo = "label+value+name",
                        marker  = dict(line = dict(width = 2,color = "rgb(243,243,243)"),
                                    colors = ['#54b6c8','#969696']),
                        domain  = dict(x = [.52,1]),
                        hole    = .6,
                        name    = f"Not{column}" 
                    )


        layout = go.Layout(dict(title = f"Churning rate based on {column} ",
                                plot_bgcolor  = "rgba(0,0,0,0)",
                                paper_bgcolor = "rgba(0,0,0,0)",
                                annotations = [dict(text = f"{column}: {x}%",
                                                    font = dict(size = 13),
                                                    showarrow = False,
                                                    x = .15, y = .5),
                                            dict(text = f"No {column}: {y}%",
                                                    font = dict(size = 13),
                                                    showarrow = False,
                                                    x = .88, y = .5
                                                )
                                            ]
                            )
                        )
        data = [trace1,trace2]
        fig = go.Figure(data = data,layout = layout)
        return fig
    y = []
    for i in bin_cols:
        x = plot_pie2(i)
        y.append(x)
    Plot2 = json.dumps(y[0],cls=plotly.utils.PlotlyJSONEncoder)
    Plot3 = json.dumps(y[1],cls=plotly.utils.PlotlyJSONEncoder)
    Plot4 = json.dumps(y[2],cls=plotly.utils.PlotlyJSONEncoder)
    Plot5 = json.dumps(y[3],cls=plotly.utils.PlotlyJSONEncoder)

    ## Based on Subscription
    telcom['PhoneOnly'] = telcom.apply(lambda i: 1 if (i['PhoneService'] == 1) and (i['InternetService'] == 'No') else 0,axis=1)
    telcom['DSLOnly'] = telcom.apply(lambda i: 1 if (i['PhoneService'] == 0) and (i['InternetService'] == 'DSL') else 0,axis=1)
    telcom['FiberOnly'] = telcom.apply(lambda i: 1 if (i['PhoneService'] == 0) and (i['InternetService'] == 'Fiber optic') else 0,axis=1)
    telcom['PhoneDSL'] = telcom.apply(lambda i: 1 if (i['PhoneService'] == 1) and (i['InternetService'] == 'DSL') else 0,axis=1)
    telcom['PhoneFiber'] = telcom.apply(lambda i: 1 if (i['PhoneService'] == 1) and (i['InternetService'] == 'Fiber optic') else 0,axis=1)

    phone = telcom[telcom['PhoneOnly']==1].pivot_table(index='Churn',aggfunc='count')[['PhoneOnly']]
    dsl = telcom[telcom['DSLOnly']==1].pivot_table(index='Churn',aggfunc='count')[['DSLOnly']]
    phoneDSL = telcom[telcom['PhoneDSL']==1].pivot_table(index='Churn',aggfunc='count')[['PhoneDSL']]
    phoneFiber = telcom[telcom['PhoneFiber']==1].pivot_table(index='Churn',aggfunc='count')[['PhoneFiber']]
    df = pd.concat([phone,dsl,phoneDSL,phoneFiber],axis=1,sort=False).T
    df['%ch'] = df.apply(lambda i: f"{round((i['Yes']/(i['Yes']+i['No']))*100,2)}%",axis=1)
    df['%no_ch'] = df.apply(lambda i: f"{round((i['No']/(i['Yes']+i['No']))*100,2)}%",axis=1)
                            
    trace1 = go.Bar(y = df.index  , x = df['Yes'],
                    name = "Churn",
                    marker = dict(color =  '#969696'),
                    text = df['%ch'],
                    textposition = 'auto',
                    orientation = 'h')

    #bar - not churn
    trace2 = go.Bar(y = df.index , x = df['No'],
                    name = "Non Churn",
                    marker = dict(color =  '#54b6c8'),
                    text = df['%no_ch'],
                    textposition = 'auto',
                    orientation = 'h')


    layout = go.Layout(dict(title = "Customer attrition in Subcription",
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = {'title' : 'Count'},
                            yaxis = {'title' : 'Subcription'}
                        )
                    )
    data = [trace1,trace2]
    fig6  = go.Figure(data=data,layout=layout)
    Plot6 = json.dumps(fig6,cls=plotly.utils.PlotlyJSONEncoder)

    ####
    cols = ['OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies']
    churn = telcom['Churn'] == 'Yes'
    no_churn = telcom['Churn'] == 'No'
    ch = []
    no_ch = []
    for i in cols:
        ya = telcom[telcom[i] == 'Yes'][i][churn].value_counts().values[0]
        no = telcom[telcom[i] == 'Yes'][i][no_churn].value_counts().values[0]
        ch.append(ya)
        no_ch.append(no)

    df = pd.DataFrame({
        'ch': ch, 'no_ch': no_ch
        },index= cols)    
        
    df['ch%']  = df.apply(lambda x:f"{round((x['ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)
    df['no_ch%'] = df.apply(lambda x:f"{round((x['no_ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)

    trace1 = go.Bar(y = cols  , x = ch,
                    name = "Churn",
                    marker = dict(color =  '#969696'),
                    text = df['ch%'],
                    textposition = 'auto',
                    orientation = 'h')

    #bar - not churn
    trace2 = go.Bar(y = cols , x = no_ch,
                    name = "Non Churn",
                    marker = dict(color =  '#54b6c8'),
                    text = df['no_ch%'],
                    textposition = 'auto',
                    orientation = 'h')


    layout = go.Layout(dict(title = "Customer attrition in Subcription",
                        paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = {'title' : 'Count'},
                            yaxis = {'title' : 'Subcription'}
                        )
                    )
    data = [trace1,trace2]
    fig8  = go.Figure(data=data,layout=layout)
    Plot8 = json.dumps(fig8,cls=plotly.utils.PlotlyJSONEncoder)
    ##
    churn     = telcom[telcom["Churn"] == "Yes"]
    not_churn = telcom[telcom["Churn"] == "No"]
    ch = churn['Contract'].value_counts()
    nch = not_churn['Contract'].value_counts()

    df1 = pd.DataFrame(ch)  
    df1.rename(columns={'Contract':'ch'},inplace=True)
    df2 = pd.DataFrame(nch)
    df2.rename(columns={'Contract':'no_ch'},inplace=True)
    df = pd.concat([df1,df2],axis=1,sort=False)
    df['ch%']  = df.apply(lambda x:f"{round((x['ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)
    df['no_ch%'] = df.apply(lambda x:f"{round((x['no_ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)


    trace1 = go.Bar(y = df.index  , x = df['ch'],
                    name = "Churn",
                    marker = dict(color =  '#969696'),
                    text = df['ch%'],
                    textposition = 'auto',
                    orientation = 'h')

    #bar - not churn
    trace2 = go.Bar(y = df.index , x = df['no_ch'],
                    name = "Non Churn",
                    marker = dict(color =  '#54b6c8'),
                    text = df['no_ch%'],
                    textposition = 'auto',
                    orientation = 'h')


    layout = go.Layout(dict(title = "Customer attrition in Contract",
                        paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = {'title' : 'Count'},
                            yaxis = {'title' : 'Contract'}
                        )
                    )
    data = [trace1,trace2]
    fig9  = go.Figure(data=data,layout=layout)
    Plot9 = json.dumps(fig9,cls=plotly.utils.PlotlyJSONEncoder)
    ##
    churn     = telcom[telcom["Churn"] == "Yes"]
    not_churn = telcom[telcom["Churn"] == "No"]
    ch = churn['PaymentMethod'].value_counts()
    nch = not_churn['PaymentMethod'].value_counts()

    df1 = pd.DataFrame(ch)  
    df1.rename(columns={'PaymentMethod':'ch'},inplace=True)
    df2 = pd.DataFrame(nch)
    df2.rename(columns={'PaymentMethod':'no_ch'},inplace=True)
    df = pd.concat([df1,df2],axis=1,sort=False)
    df['ch%']  = df.apply(lambda x:f"{round((x['ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)
    df['no_ch%'] = df.apply(lambda x:f"{round((x['no_ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)


    trace1 = go.Bar(y = df.index  , x = df['ch'],
                    name = "Churn",
                    marker = dict(color =  '#969696'),
                    text = df['ch%'],
                    textposition = 'auto',
                    orientation = 'h')

    #bar - not churn
    trace2 = go.Bar(y = df.index , x = df['no_ch'],
                    name = "Non Churn",
                    marker = dict(color =  '#54b6c8'),
                    text = df['no_ch%'],
                    textposition = 'auto',
                    orientation = 'h')


    layout = go.Layout(dict(title = "Customer attrition in PaymentMethod",
                        paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = {'title' : 'Count'},
                            yaxis = {'title' : 'Payment Method'}
                        )
                    )
    data = [trace1,trace2]
    fig10  = go.Figure(data=data,layout=layout)
    Plot10 = json.dumps(fig10,cls=plotly.utils.PlotlyJSONEncoder)

    ##
    def tenure_lab(telcom) :
        if telcom["tenure"] <= 12 :
            return "0-12"
        elif (telcom["tenure"] > 12) & (telcom["tenure"] <= 24 ):
            return "12-24"
        elif (telcom["tenure"] > 24) & (telcom["tenure"] <= 36) :
            return "24-36"
        elif (telcom["tenure"] > 36) & (telcom["tenure"] <= 48) :
            return "36-48"
        elif (telcom["tenure"] > 48) & (telcom["tenure"] <= 60) :
            return "48-60"
        elif telcom["tenure"] > 60 :
            return "60-72"
    telcom["tenure_group"] = telcom.apply(lambda telcom:tenure_lab(telcom),axis = 1)

    piv = telcom.pivot_table(index='tenure_group',columns='Churn',aggfunc='count')[['customerID']]
    piv = piv['customerID']
    piv['ch%'] = piv.apply(lambda i: f"{round((i['Yes']/(i['No']+i['Yes']))*100,2)}%",axis=1)
    piv['no_ch%'] = piv.apply(lambda i: f"{round((i['No']/(i['No']+i['Yes']))*100,2)}%",axis=1)

    #bar - churn
    trace1 = go.Bar(y = piv.index  , x = piv['Yes'],
                    name = "Churn",
                    marker = dict(color =  '#969696'),
                    text = piv['ch%'],
                    textposition = 'auto',
                    orientation = 'h')

    #bar - not churn
    trace2 = go.Bar(y = piv.index, x = piv['No'],
                    name = "Non Churn",
                    marker = dict(color =  '#54b6c8'),
                    text = piv['no_ch%'],
                    textposition = 'auto',
                    orientation = 'h')

    layout = go.Layout(dict(title = "Customer attrition in tenure groups",
                        paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = dict(title = "Count"),
                            yaxis = dict(title = "Tenure (month)")
                        )
                    )
    data = [trace1,trace2]
    fig11  = go.Figure(data=data,layout=layout)
    Plot11 = json.dumps(fig11,cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('analysis.html', Plot=Plot,Plot1=Plot1,Plot2=Plot2,Plot3=Plot3,Plot4=Plot4,Plot5=Plot5,
                    Plot6=Plot6, Plot8=Plot8, Plot9=Plot9,Plot10=Plot10,Plot11=Plot11)

@app.route('/hasil', methods = ['GET','POST'])
def hasil():
    if request.method == 'POST':
        seniorCitizen = int(request.form['SeniorCitizen'])
        partner = int(request.form['Partner'])
        dependent = int(request.form['Dependents'])
        tenure = int(request.form['tenure']) 
        phoneService = int(request.form['PhoneService'])
        paperlessBilling = int(request.form['PaperlessBilling'])
        gender = request.form['gender']
        multiple = request.form['MultipleLines']
        internetService = request.form['InternetService']
        contract = request.form['Contract']
        paymentMethod = request.form['PaymentMethod']
        onlineSecurity = request.form['OnlineSecurity']
        onlineBackup = request.form['OnlineBackup']
        deviceProtection = request.form['DeviceProtection']
        techSupport = request.form['TechSupport']
        streamingTV = request.form['StreamingTV']
        streamingMovie = request.form['StreamingMovies']
       
        combine = [seniorCitizen] + [partner] + [dependent] + [tenure] + [phoneService] + [paperlessBilling] + choice4[f'{gender}'] + choice1[f'{multiple}'] + choice2[f'{internetService}'] + choice2[f'{contract}'] + choice3[f'{paymentMethod}'] + choice1[f'{onlineSecurity}'] + choice1[f'{onlineBackup}'] + choice1[f'{deviceProtection}'] + choice1[f'{techSupport}'] + choice1[f'{streamingTV}'] + choice1[f'{streamingMovie}']
        predict = model.predict([combine])[0]
        if predict == 0:
            churn = 'Not Churn'
        else: 
            churn = 'Churn'

        proba = model.predict_proba([combine])[0]
        ## grafik for probability
        trace = go.Pie(labels=['Not Churn','Churn'],values=proba,hole=0.6,
                        hoverinfo = "label+value+text",
                        marker = dict(colors =  [ '#54b6c8' ,'#969696'],
                                        line = dict(color = "white", width =  0.5)))
        layout = go.Layout(dict(title = f"Probability of Customer Churn ",
                            plot_bgcolor  = "rgba(0,0,0,0)",
                            paper_bgcolor = "rgba(0,0,0,0)"),
                            annotations = [dict(text = f"{churn}",
                                                    font = dict(size = 15),
                                                    showarrow = False,
                                                    x = .5, y = .5)])
        fig = go.Figure(data=trace,layout=layout)
        # convert figure to JSON format use plotly.utils.PlotlyJSONEncoder 
        churnPlot = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('result.html', churn = churn, combine=combine,churnPlot=churnPlot)
    else :
        return render_template('mainpage.html')


if __name__ == '__main__':
        ## load dataset
    telcom = pd.read_csv('telcom_clean.csv')

    ## for col : MultipleLines,OnlineSecurity,Backup,DevProtection,TechSupport,StreamTV,StreamMovies
    choice1 = {
        'a' : [0,0,1],
        'b' : [1,0,0],
        'c' : [0,1,0]}

    ## for col : Internet Service,Contract
    choice2 = {
        'a' : [1,0,0],
        'b' : [0,1,0],
        'c' : [0,0,1]}

    ## for col : Payment Method
    choice3 = {
        'a' : [1,0,0,0],
        'b' : [0,1,0,0],
        'c' : [0,0,1,0],
        'd' : [0,0,0,1]}
    ## for col : Gender
    choice4 = {
        'a' : [0,1],
        'b' : [1,0]}

    ## upload model
    model = joblib.load('rf_best_model')
    app.run(debug=True, host='127.0.0.1')


