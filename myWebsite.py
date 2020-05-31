from flask import Flask, render_template, jsonify, redirect, url_for, request
import json
import joblib
import plotly
import plotly.graph_objs as go
import chart_studio.plotly as csp
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

## Visualize
@app.route('/analysis') 
def analysis():
    # Total Custemer Churn
    key = telco["Churn"].value_counts().keys().tolist()
    val = telco["Churn"].value_counts().values.tolist()
    trace = go.Pie(labels = key ,values = val ,
                marker = {'colors' :  [ '#54b6c8' ,'#969696']}, hole = .6)
    layout = go.Layout(dict(title = "Customer Churn in data"),
                            plot_bgcolor  = "rgba(0,0,0,0)",
                            paper_bgcolor = "rgba(0,0,0,0)",
                            annotations = [{'text' : f"Churning Customer",'font' : {'size' : 18},
                                                    'showarrow' : False}])
    fig  = go.Figure(data = trace,layout = layout)
    Plot = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    ## gender
    male = telco[telco['gender'] == 'Male']
    female = telco[telco['gender'] == 'Female']
    m = round(telco['gender'].value_counts()['Male']/telco['gender'].value_counts().sum() * 100,2)
    f = round(telco['gender'].value_counts()['Female']/telco['gender'].value_counts().sum() * 100,2)
        
    trace1 = go.Pie(values  = male['Churn'].value_counts().values.tolist(),
                        labels  = male['Churn'].value_counts().keys().tolist(),
                        hole=.6,name    = "Male",marker  = {'colors' :  [ '#54b6c8' ,'#969696']},
                        domain  = {'column':0,'row':0})
    trace2 = go.Pie(values  = female['Churn'].value_counts().values.tolist(),
                        labels  = female['Churn'].value_counts().keys().tolist(),
                        hole=.6,name    = "Female",marker  = {'colors' :  [ '#54b6c8' ,'#969696']},
                        domain  = {'column':1,'row':0})
    layout = go.Layout(dict(title = f"Churning rate based on Gender",
                                grid= {"rows": 1, "columns": 2},
                                plot_bgcolor  = "rgba(0,0,0,0)", paper_bgcolor = "rgba(0,0,0,0)",
                                annotations = [dict(text = f"Male : {m}% ",font = dict(size = 13),
                                                    showarrow = False,x = .18, y = .5),
                                            dict(text = f"Female : {f}%",font = dict(size = 13),
                                                    showarrow = False, x = .83,y = .5)]))
    fig1 = go.Figure(data = [trace1,trace2],layout = layout)
    Plot1 = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)

    ### Visualize Based on Personal Info
    bin_cols= ['SeniorCitizen','Partner','Dependents']
    def pie(column) :
        Yes = telco[telco[column] == 1]
        No = telco[telco[column] == 0]
        x = round(telco[column].value_counts()[1]/telco[column].value_counts().sum() * 100,2)
        y = round(telco[column].value_counts()[0]/telco[column].value_counts().sum() * 100,2)
        
        trace1 = go.Pie(values  = Yes['Churn'].value_counts().values.tolist(),
                        labels  = Yes['Churn'].value_counts().keys().tolist(),
                        hole=.6,name    = f"{column}",marker  = {'colors' :  [ '#54b6c8' ,'#969696']},
                        domain  = {'column':0,'row':0})
        trace2 = go.Pie(values  = No['Churn'].value_counts().values.tolist(),
                        labels  = No['Churn'].value_counts().keys().tolist(),
                        hole=.6,name    = f"Not{column}",marker  = {'colors' :  [ '#54b6c8' ,'#969696']},
                        domain  = {'column':1,'row':0})
        layout = go.Layout(dict(title = f"Churning rate based on {column} ", grid= {"rows": 1, "columns": 2},
                                plot_bgcolor  = "rgba(0,0,0,0)", paper_bgcolor = "rgba(0,0,0,0)",
                                annotations = [dict(text = f"{column}: {x}%",font = dict(size = 13),
                                                    showarrow = False,x = .15, y = .5),
                                            dict(text = f"No {column}: {y}%",font = dict(size = 13),
                                                    showarrow = False, x = .88, y = .5)]))
        data = [trace1,trace2]
        fig  = go.Figure(data = data,layout = layout)
        return fig
    y = []
    for i in bin_cols:
        x = pie(i)
        y.append(x)
    Plot2 = json.dumps(y[0],cls=plotly.utils.PlotlyJSONEncoder)
    Plot3 = json.dumps(y[1],cls=plotly.utils.PlotlyJSONEncoder)
    Plot4 = json.dumps(y[2],cls=plotly.utils.PlotlyJSONEncoder)

    ## MultipleLine
    churn     = telco[telco["Churn"] == "Yes"]
    not_churn = telco[telco["Churn"] == "No"]
    ch = churn['MultipleLines'].value_counts()
    nch = not_churn['MultipleLines'].value_counts()

    df1 = pd.DataFrame(ch)  
    df1.rename(columns={'MultipleLines':'ch'},inplace=True)
    df2 = pd.DataFrame(nch)
    df2.rename(columns={'MultipleLines':'no_ch'},inplace=True)
    df = pd.concat([df1,df2],axis=1)
    df['ch%']  = df.apply(lambda x:f"{round((x['ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)
    df['no_ch%'] = df.apply(lambda x:f"{round((x['no_ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)

    trace1 = go.Bar(y = df.index  , x = df['ch'],
                    name = "Churn", marker = {'color':  '#969696'},
                    text = df['ch%'], textposition = 'auto', orientation = 'h')

    trace2 = go.Bar(y = df.index , x = df['no_ch'],
                    name = "Non Churn", marker = {'color' : '#54b6c8'},
                    text = df['no_ch%'],textposition = 'auto', orientation = 'h')

    layout = go.Layout(dict(title = "Customer Churn Based MultipleLines",
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = {'title' : 'Count'}, yaxis = {'title' : 'Multiple Lines'}))
    data = [trace1,trace2]
    fig  = go.Figure(data=data,layout=layout)
    Plot5 = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

    ## Based on Subscription
    phone = telco[telco['PhoneOnly']==1].pivot_table(index='Churn',aggfunc='count')[['PhoneOnly']]
    dsl = telco[telco['DSLOnly']==1].pivot_table(index='Churn',aggfunc='count')[['DSLOnly']]
    phoneDSL = telco[telco['Phone&DSL']==1].pivot_table(index='Churn',aggfunc='count')[['Phone&DSL']]
    phoneFiber = telco[telco['Phone&FiberOptic']==1].pivot_table(index='Churn',aggfunc='count')[['Phone&FiberOptic']]
    df = pd.concat([phone,dsl,phoneDSL,phoneFiber],axis=1).T
    df['%ch'] = df.apply(lambda i: f"{round((i['Yes']/(i['Yes']+i['No']))*100,2)}%",axis=1)
    df['%no_ch'] = df.apply(lambda i: f"{round((i['No']/(i['Yes']+i['No']))*100,2)}%",axis=1)
                            
    trace1 = go.Bar(y = df.index  , x = df['Yes'],
                    name = "Churn", marker = {'color':  '#969696'},
                    text = df['%ch'], textposition = 'auto', orientation = 'h')

    trace2 = go.Bar(y = df.index , x = df['No'],
                    name = "Non Churn", marker = {'color' :  '#54b6c8'},
                    text = df['%no_ch'], textposition = 'auto',orientation = 'h')

    layout = go.Layout(dict(title = "Customer Churn based on Subcription",
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = {'title' : 'Count'}, yaxis = {'title' : 'Subcription'}))
    data = [trace1,trace2]
    fig  = go.Figure(data=data,layout=layout)
    Plot6 = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)  
    ###
    cols = ['OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies']
    churn = telco['Churn'] == 'Yes'
    no_churn = telco['Churn'] == 'No'
    ch = []
    no_ch = []
    for i in cols:
        ya = telco[telco[i] == 'Yes'][i][churn].value_counts().values[0]
        no = telco[telco[i] == 'Yes'][i][no_churn].value_counts().values[0]
        ch.append(ya)
        no_ch.append(no)

    df = pd.DataFrame({'ch': ch, 'no_ch': no_ch},index= cols)    
        
    df['ch%']  = df.apply(lambda x:f"{round((x['ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)
    df['no_ch%'] = df.apply(lambda x:f"{round((x['no_ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)

    trace1 = go.Bar(y = cols  , x = ch,
                    name = "Churn", marker = {'color':  '#969696'},
                    text = df['ch%'],textposition = 'auto', orientation = 'h')
    trace2 = go.Bar(y = cols , x = no_ch,
                    name = "Non Churn",marker = {'color' :  '#54b6c8'},
                    text = df['no_ch%'], textposition = 'auto',orientation = 'h')
    layout = go.Layout(dict(title = "Customer Churn based on Subcription",
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = {'title' : 'Count'}, yaxis = {'title' : 'Subcription'}))
    data = [trace1,trace2]
    fig  = go.Figure(data=data,layout=layout)
    Plot7 = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

    # PaperlessBilling
    figx = pie('PaperlessBilling')
    Plot8 = json.dumps(figx,cls=plotly.utils.PlotlyJSONEncoder)
    ## Contract
    churn     = telco[telco["Churn"] == "Yes"]
    not_churn = telco[telco["Churn"] == "No"]
    ch = churn['Contract'].value_counts()
    nch = not_churn['Contract'].value_counts()
    df1 = pd.DataFrame(ch)  
    df1.rename(columns={'Contract':'ch'},inplace=True)
    df2 = pd.DataFrame(nch)
    df2.rename(columns={'Contract':'no_ch'},inplace=True)
    df = pd.concat([df1,df2],axis=1)
    df['ch%']  = df.apply(lambda x:f"{round((x['ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)
    df['no_ch%'] = df.apply(lambda x:f"{round((x['no_ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)
    trace1 = go.Bar(y = df.index  , x = df['ch'],
                    name = "Churn", marker = { 'color':  '#969696'},
                    text = df['ch%'],textposition = 'auto', orientation = 'h')
    trace2 = go.Bar(y = df.index , x = df['no_ch'],
                    name = "Non Churn", marker = { 'color': '#54b6c8'},
                    text = df['no_ch%'], textposition = 'auto', orientation = 'h')
    layout = go.Layout(dict(title = "Customer Churn based on Contract",
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = {'title' : 'Count'}, yaxis = {'title' : 'Contract'}))
    data = [trace1,trace2]
    fig  = go.Figure(data=data,layout=layout)
    Plot9 = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    ## Payment Method
    ch = churn['PaymentMethod'].value_counts()
    nch = not_churn['PaymentMethod'].value_counts()

    df1 = pd.DataFrame(ch)  
    df1.rename(columns={'PaymentMethod':'ch'},inplace=True)
    df2 = pd.DataFrame(nch)
    df2.rename(columns={'PaymentMethod':'no_ch'},inplace=True)
    df = pd.concat([df1,df2],axis=1)
    df['ch%']  = df.apply(lambda x:f"{round((x['ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)
    df['no_ch%'] = df.apply(lambda x:f"{round((x['no_ch']/(x['ch']+x['no_ch']))*100,2)}%",axis=1)

    trace1 = go.Bar(y = df.index  , x = df['ch'],
                    name = "Churn", marker = {'color' : '#969696'},
                    text = df['ch%'], textposition = 'auto', orientation = 'h')
    trace2 = go.Bar(y = df.index , x = df['no_ch'],
                    name = "Non Churn", marker = {'color': '#54b6c8'},
                    text = df['no_ch%'], textposition = 'auto',orientation = 'h')
    layout = go.Layout(dict(title = "Customer Churn based on PaymentMethod",
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = {'title' : 'Count'}, yaxis = {'title' : 'Payment Method'}))
    data = [trace1,trace2]
    fig  = go.Figure(data=data,layout=layout)
    Plot10 = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    ## tenure group
    piv = telco.pivot_table(index='tenure_col',columns='Churn',aggfunc='count')[['customerID']]
    piv = piv['customerID']
    piv['ch%'] = piv.apply(lambda i: f"{round((i['Yes']/(i['No']+i['Yes']))*100,2)}%",axis=1)
    piv['no_ch%'] = piv.apply(lambda i: f"{round((i['No']/(i['No']+i['Yes']))*100,2)}%",axis=1)
    trace1 = go.Bar(y = piv.index  , x = piv['Yes'],
                    name = "Churn",marker = {'color' :  '#969696'},
                    text = piv['ch%'], textposition = 'auto', orientation = 'h')
    trace2 = go.Bar(y = piv.index, x = piv['No'],
                    name = "Non Churn", marker = {'color':  '#54b6c8'},
                    text = piv['no_ch%'], textposition = 'auto', orientation = 'h')

    layout = go.Layout(dict(title = "Customer Churn in tenure groups",
                        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
                            xaxis = dict(title = "Count"),
                            yaxis = dict(title = "Tenure (month)")))
    data = [trace1,trace2]
    fig  = go.Figure(data=data,layout=layout)
    Plot11 = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    ##histogram
    def histogram(column) :
        churn = telco[telco["Churn"] == "Yes"]
        not_churn = telco[telco["Churn"] == "No"]
        trace1 = go.Histogram(x  = churn[column],name = "Churn",
                            marker = {'color' :  '#969696'}, opacity = .9)   
        trace2 = go.Histogram(x  = not_churn[column], name = "Not churn",
                            marker = {'color':  '#54b6c8'},opacity = .9)
        trace3 = go.Histogram(x  = telco[column],name = "All Customers",opacity = .9)
        
        data = [trace1,trace2,trace3]
        layout = go.Layout(dict(title =column + " distribution",
                                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                xaxis = dict(title = column),
                                yaxis = dict(title = "count")))
        fig  = go.Figure(data=data,layout=layout)
        return fig

    hist_ten = histogram('tenure')
    hist_month = histogram('MonthlyCharges')
    hist_tot = histogram('TotalCharges')
    Plot12 = json.dumps(hist_ten,cls=plotly.utils.PlotlyJSONEncoder)
    Plot13 = json.dumps(hist_month,cls=plotly.utils.PlotlyJSONEncoder)
    Plot14 = json.dumps(hist_tot,cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('analysis.html', Plot=Plot,Plot1=Plot1,Plot2=Plot2,Plot3=Plot3,Plot4=Plot4,Plot5=Plot5,
                    Plot6=Plot6,Plot7=Plot7, Plot8=Plot8, Plot9=Plot9,Plot10=Plot10,Plot11=Plot11,
                    Plot12=Plot12,Plot13=Plot13,Plot14=Plot14)

@app.route('/predik', methods = ['GET','POST'])
def predik():
    if request.method == 'POST':
        seniorCitizen = int(request.form['SeniorCitizen'])
        partner = int(request.form['Partner'])
        dependent = int(request.form['Dependents'])
        tenure = scaler.transform([[int(request.form['tenure'])]])[0][0] 
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
       
        combine = [seniorCitizen] + [partner] + [dependent] + [phoneService] + [paperlessBilling] + choice4[f'{gender}'] + choice1[f'{multiple}'] + choice2[f'{internetService}'] + choice2[f'{contract}'] + choice3[f'{paymentMethod}'] + choice1[f'{onlineSecurity}'] + choice1[f'{onlineBackup}'] + choice1[f'{deviceProtection}'] + choice1[f'{techSupport}'] + choice1[f'{streamingTV}'] + choice1[f'{streamingMovie}'] + [tenure]
        # combine2 = ({'hasil': combine})
        predict = model.predict([combine])[0]
        proba0 = round((model.predict_proba([combine])[0][0])*100,2)
        proba1 = round((model.predict_proba([combine])[0][1])*100,2)
        if predict == 0:
            churn = f'Not Churn with probabilities {proba0} %   '
        else: 
            churn = f'Churn with probabilities {proba1} %   '

        proba = model.predict_proba([combine])[0]
        ## grafik for probability
        trace = go.Pie(labels=['Not Churn','Churn'],values=proba,hole=0.6,
                        hoverinfo = "label+value+text",
                        marker = dict(colors =  [ '#54b6c8' ,'#969696'],
                                        line = dict(color = "white", width =  0.5)))
        layout = go.Layout(dict(plot_bgcolor  = "rgba(0,0,0,0)", paper_bgcolor = "rgba(0,0,0,0)"))
        fig = go.Figure(data=trace,layout=layout)
        # convert figure to JSON format use plotly.utils.PlotlyJSONEncoder 
        churnPlot = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

        ## Description Customer

        if seniorCitizen == 1:
            sC = 'Yes'
        else :
            sC = 'No'
        if partner == 1:
            prT = 'Yes'
        else :
            prT = 'No'
        if dependent == 1:
            dpD = 'Yes'
        else :
            dpD = 'No'
        if phoneService == 1:
            phnS = 'Yes'
        else :
            phnS = 'No'
        if paperlessBilling == 1:
            ppB = 'Yes'
        else :
            ppB = 'No'
        if gender == 'a':
            gnd = 'Male'
        else :
            gnd = 'Female'
        if multiple == 'a':
            mltp = 'Yes'
        elif multiple == 'b':
            mltp = 'No'
        else :
            mltp = 'No PhoneService'
        if internetService == 'a':
            itrS = 'DSL'
        elif internetService == 'b':
            itrS = 'Fiber Optic'
        else :
            itrS = 'No Internet Service'
        if contract == 'a':
            ctrc = 'Month to month' 
        elif contract == 'b':
            ctrc = 'One year'
        else :
            ctrc = 'Two year'
        if paymentMethod == 'a':
            payM = 'Bank Transfer (automatic)'
        elif paymentMethod =='b':
            payM = 'Credit Card (automatic)'
        elif paymentMethod == 'c':
            payM = 'Electronic Check'
        else:
            payM = 'Mailed Check'
        if onlineSecurity == 'a':
            oSec = 'Yes'
        elif onlineSecurity == 'b':
            oSec = 'No'
        else :
            oSec = 'No Internet Service'
        if onlineBackup == 'a':
            oBac = 'Yes'
        elif onlineBackup == 'b':
            oBac = 'No'
        else :
            oBac = 'No Internet Service' 
        if deviceProtection == 'a':
            dProt = 'Yes'
        elif deviceProtection == 'b':
            dProt = 'No'
        else :
            dProt = 'No Internet Service'
        if techSupport == 'a':
            tSup = 'Yes'
        elif techSupport == 'b':
            tSup = 'No'
        else :
            tSup = 'No Internet Service'   
        if streamingTV == 'a':
            strTV = 'Yes'
        elif streamingTV == 'b':
            strTV = 'No'
        else :
            strTV = 'No Internet Service'
        if streamingMovie == 'a':
            strMov = 'Yes'
        elif streamingMovie == 'b':
            strMov = 'No'
        else :
            strMov = 'No Internet Service'
        tnr = request.form['tenure']

        return render_template('result.html', churn = churn, combine=combine,churnPlot=churnPlot,
                        sC=sC,prT=prT,dpD=dpD,phnS=phnS,ppB=ppB,gnd=gnd,mltp=mltp,itrS=itrS,ctrc=ctrc,
                        payM=payM,oSec=oSec,oBac=oBac,dProt=dProt,tSup=tSup,strTV=strTV,strMov=strMov,tnr=tnr)
        # return render_template('result.html',combine2=combine2) #cek value
    else :
        return render_template('predict.html')


if __name__ == '__main__':
    ## load dataset for visualization
    telco = pd.read_csv('telcom_vis.csv')
    ## define scaler
    scaler = StandardScaler()
    scaler.fit_transform(telco[['tenure']])
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

    ## load model ML
    model = joblib.load('lr_best_model')
    app.run(debug=True, host='127.0.0.1')


