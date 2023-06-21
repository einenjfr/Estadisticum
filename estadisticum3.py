import mysql.connector
from mysql.connector import Error

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import math

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, Flowable, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib import randomtext
from reportlab import platypus


#### CONSTANTS ####
DIM = 5     # num d'individus a analitzar


def drawPageFrame(canvas, doc):
    canvas.saveState()
    canvas.drawImage("regresio.jpg",50,50,57,57)
    canvas.restoreState()

#### CORRECIO OUTSIDERS I ETAPES ####
# no detecta outsiders ni en pos=0 ni en pos=sizeof(vals)-1
def outsidersCO2 (mostra):
    outs = []
    auxpiccolo = 0
    auxgrande = 0
    aux = []
    aux.append(mostra[0])
    dt = 0
    for j in range (1, 10):
        auxpiccolo, auxgrande = (mostra[j-1],mostra[j]) if mostra[j-1] < mostra[j] else (mostra[j],mostra[j-1])
        if auxpiccolo + 500 >= auxgrande:
            aux.append(mostra[j])
    dt = math.sqrt(var(aux,media(aux)))
    for j in range (1,len(mostra)-1):
        if abs(mostra[j]-mostra[j-1]) > dt * 10 and abs(mostra[j]-mostra[j+1]) > dt * 10:
            outs.append(j)
    return outs
                
            
def novaNorma (mostra):
    outs = []
    auxpiccolo = 0
    auxgrande = 0
    aux = []
    aux.append(mostra[0])

    posNormes = []

    for j in range (1, 10):
        auxpiccolo, auxgrande = (mostra[j-1],mostra[j]) if mostra[j-1] < mostra[j] else (mostra[j],mostra[j-1])
        if auxpiccolo + 500 >= auxgrande:
            aux.append(mostra[j])
    dt = math.sqrt(var(aux,media(aux)))
    for j in range (1,len(mostra)-1):
        if abs(mostra[j]-mostra[j-1]) > dt * 10 and abs(mostra[j]-mostra[j+1]) <= dt * 10:
            posNormes.append(j)
    print(posNormes)
    return posNormes







#### PART CALCULS ####

def media (vals):
    return sum(vals) / len(vals)

def var (vals, media, tipus=True):
    n = len(vals) if tipus else len(vals)-1
    suma = 0
    for i in vals:
        suma = suma + pow(i - media,2)
    return suma / n

def covar (x, y, tipus=True):
    n = len(x) if tipus else len(x)-1
    medX = media(x)
    medY = media(y)

    varX = 0
    varY = 0

    for i in range(n):
        varX = varX + x[i]-medX
        varY = varY + y[i]-medY

    return varX*varY/n


def pearson (x, y):
    Sx = math.sqrt(var(x,False))
    Sy = math.sqrt(var(y,False))
    S2xy = covar(x,y,False)

    return S2xy/(Sx*Sy)

def rquadrat (x,y):
    estY = []
    b0 = regre_b0(x,y)
    b1 = regre_b1(x,y)
    medY = media(y)

    for i in range (len(y)):
        estY.append(b0 + b1 * x[i])
    medEstY = media(estY)

    varY = 0
    varEstY = 0

    for i in range (len(y)):
        varEstY = varEstY + pow(estY[i] - medEstY,2)
        varY = varY + pow(y[i] - medY,2)

    return 1 - varEstY / varY

def regre_b0 (x,y):
    return media(y) - regre_b1(x,y) * media(x)

def regre_b1 (x,y):
    medX = media(x)
    medY = media(y)

    varXY = 0
    varX2 = 0

    for i in range(len(x)):
        varXY = (x[i]-medX)*(y[i]-medY)
        varX2 = pow(x[i]-medX,2)

    return varXY / varX2






#### PART GRAFICS ####

def regre (xlist, ylist, nom="0"):

    x = np.array(xlist)
    y = np.array(ylist)


    #y = np.array([np.nan,2,np.nan,3])

    # Initialize layout
    fig, ax = plt.subplots(figsize = (9, 9))

    # Add scatterplot
    ax.scatter(x, y, s=60, alpha=0.7, edgecolors="k")

    # Fit linear regression via least squares with numpy.polyfit
    # It returns an slope (b) and intercept (a)
    # deg=1 means linear fit (i.e. polynomial of degree 1)
    b, a = np.polyfit(x, y, deg=1)

    # Create sequence of 100 numbers from 0 to 100 
    xseq = np.linspace(min(xlist), max(xlist), num=100)

    # Plot regression line
    ax.plot(xseq, a + b * xseq, color="k", lw=2.5);

    plt.savefig('regresio_' + nom + '.png')
    plt.show()


    print("p")


def evol(idd, temp, co2, humetat, medT, medC, medH, nom="0"):
    # create data
    x = np.array(idd)
    y = np.array(temp)
    y2 = np.array(co2)
    y3 = np.array(humetat)

    mT = np.full(len(y), medT, dtype=int)
    mC = np.full(len(y), medC, dtype=int)
    mH = np.full(len(y), medH, dtype=int)
      
    # plot lines
    plt.plot(x, y, label = "Temperatura")
    plt.plot(x, y2, label = "CO2")
    plt.plot(x, y3, label = "Humetat")

    #Linies mitjanes
    plt.plot(x, mT, label = "Mitja temperatura")
    plt.plot(x, mC, label = "Mitja CO2")
    plt.plot(x, mH, label = "Mitja humetat")
    plt.savefig('evolucio_' + nom + '.png')
    plt.legend()
    plt.show()



def evol2(vals):
    # DataFrame to represent opening , closing, high 
    # and low prices of a stock for a week
    maxx = 0
    loww = 0
    op = []
    cl = []
    ma = []
    lo = []
    print("vals")

    for i in range(0,len(vals)):
        val = vals[i]
        print(idd)
        if i % 5 == 0:
            op.append(val)
            maxx = val
            loww = val
        elif i % 5 == 4:
            cl.append(val)
            if maxx < val:
                ma.append(val)
            else:
                ma.append(maxx)
            if loww > val:
                lo.append(val)
            else:
                lo.append(loww)
            
        else:
            if maxx < val:
                maxx = val
            if loww > val:
                loww = val
    print(op)
    print(cl)
    print(ma)
    print(lo)
    stock_prices = pd.DataFrame({'open': op,
                                 'close': cl,
                                 'high': ma,
                                 'low': lo},
                                index=pd.date_range(
                                  "2021-11-10", periods=4, freq="d"))
    #stock_prices = pd.DataFrame({'open': [36, 56, 45, 29, 65, 66, 67],
    #                             'close': [29, 72, 11, 4, 23, 68, 45],
    #                             'high': [42, 73, 61, 62, 73, 56, 55],
    #                             'low': [22, 11, 10, 2, 13, 24, 25]},
    #                            index=pd.date_range(
    #                              "2021-11-10", periods=7, freq="d"))
      
      
    plt.figure()
      
    # "up" dataframe will store the stock_prices 
    # when the closing stock price is greater
    # than or equal to the opening stock prices
    up = stock_prices[stock_prices.close >= stock_prices.open]
      
    # "down" dataframe will store the stock_prices
    # when the closing stock price is
    # lesser than the opening stock prices
    down = stock_prices[stock_prices.close < stock_prices.open]
      
    # When the stock prices have decreased, then it
    # will be represented by blue color candlestick
    col1 = 'red'
      
    # When the stock prices have increased, then it 
    # will be represented by green color candlestick
    col2 = 'green'
      
    # Setting width of candlestick elements
    width = .3
    width2 = .03
      
    # Plotting up prices of the stock
    plt.bar(up.index, up.close-up.open, width, bottom=up.open, color=col1)
    plt.bar(up.index, up.high-up.close, width2, bottom=up.close, color=col1)
    plt.bar(up.index, up.low-up.open, width2, bottom=up.open, color=col1)
      
    # Plotting down prices of the stock
    plt.bar(down.index, down.close-down.open, width, bottom=down.open, color=col2)
    plt.bar(down.index, down.high-down.open, width2, bottom=down.open, color=col2)
    plt.bar(down.index, down.low-down.close, width2, bottom=down.close, color=col2)
      
    # rotating the x-axis tick labels at 30degree 
    # towards right
    plt.xticks(rotation=30, ha='right')
      
    # displaying candlestick chart of stock data 
    # of a week
    plt.show()




#### INIT PROGRAMA ####

try:
    connection = mysql.connector.connect(host='192.168.3.10',
                                         database='juanreptem3',
                                         user='juan',
                                         password='juan')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select DadesID,Temperatura,CO2,Humetat, TVOC from Dades;")
        aux = cursor.fetchall()
        idd = []
        temp = []
        co2 = []
        humetat = []
        tvoc = []
        vals = []

        # prenem totes les dades
        for d in aux:
            idd.append(d["DadesID"])
            temp.append(d["Temperatura"])
            co2.append(d["CO2"])
            humetat.append(d["Humetat"])
            tvoc.append(d["TVOC"])

        # vals és una llista que agrupa totes les llistes, no és quasi utilitzat, però podria servir en cas d'haver d'enviar dades a altre funció, mòdul o SGDB
        vals.append(idd)
        vals.append(temp)
        vals.append(co2)
        vals.append(humetat)
        vals.append(tvoc)

        # cerquem posicions dels outsiders
        ael = outsidersCO2(co2)


        # procedim a eliminar-los
        for j in range(len(ael)-1,-1,-1):
            del idd[ael[j]]
            del temp[ael[j]]
            del co2[ael[j]]
            del humetat[ael[j]]
            del tvoc[ael[j]]

        # si prenem mesures a diferents llocs o a diferents hores els valors canvien molt i no són pràcticament associables
        # com ens interessa evaluar mostres de proves individuals i les seves relacions, només en prendrem la primera situació
        # com a possible millora, es podria prendre una llista de situacions i fer proves d'hipòtesis amb distribucions o amb ANOVA
        ael = novaNorma(co2)



        for j in range(len(ael)-1,-1,-1):
            idd = idd[:ael[j]]
            temp = temp[:ael[j]]
            co2 = co2[:ael[j]]
            humetat = humetat[:ael[j]]
            tvoc = tvoc[:ael[j]]

        #print(co2)
        
        
        medT = media(temp)
        medC = media(co2)
        medH = media(humetat)
        medV = media(tvoc)

        varT = var(temp,medT)
        varC = var(co2,medC)
        varH = var(humetat,medH)
        varV = var(tvoc,medV)

        desT = math.sqrt(varT)
        desC = math.sqrt(varC)
        desH = math.sqrt(varH)
        desV = math.sqrt(varV)

        covTC = covar(temp,co2)
        covTH = covar(temp,humetat)
        covCV = covar(co2,tvoc)

        prsTC = pearson(temp,co2)
        prsTH = pearson(temp,humetat)
        prsCV = pearson(co2,tvoc)

        rqtTC = rquadrat(temp,co2)
        rqtTH = rquadrat(temp,humetat)
        rqtCV = rquadrat(co2,tvoc)
        
        print("mitges (temperatura, humetat, CO2, TVOC): (" + str(medT) + ", " + str(medC) + ")")
        print("variabilitat (temperatura, humetat, CO2, TVOC): (" + str(var(temp,medT)) + ", " + str(varC) + ")")
        print("desviacio tipica (temperatura, humetat, CO2, TVOC): (" + str(var(humetat,medH)) + ", " + str(varH) + ")")

        print("covariabilitat (temperatura, humetat) = " + str(covTC))
        print("covariabilitat (temperatura, CO2) = " + str(covTH))
        print("covariabilitat (CO2, TVOC) = " + str(covCV))

        print("coeficient de correlació de Pearson (temperatura, humetat): " + str(prsTH))
        print("coeficient de correlació de Pearson (temperatura, CO2): " + str(prsTC))
        print("coeficient de correlació de Pearson (CO2, TVOC): " + str(prsCV))
        
        print("R2 (temperatura, humetat): " + str(rqtTH))
        print("R2 (temperatura, CO2): " + str(rqtTC))
        print("R2 (CO2, TVOC): " + str(rqtCV))
      
        regre(temp,co2,"TempCo2_1")
        regre(temp,humetat,"TempHumetat_1")
        regre(co2,tvoc,"Co2Tvoc_1")
        evol(idd,temp,co2,humetat,medT,medC,medH,"tot")

        #evol2(co2)


        my_canvas = canvas.Canvas("analisis_resultats.pdf", pagesize=letter)
        my_canvas.setLineWidth(.3)
        my_canvas.setFont('Helvetica', 12)
        my_canvas.drawString(30, 750, 'ERIC TORRONTERA & JUAN FORNIS')
        my_canvas.drawString(500, 750, "06/2022")
        my_canvas.line(480, 747, 580, 747)
        my_canvas.drawString(275, 725, 'OBJECTE')
        my_canvas.drawString(500, 725, "ESTADÍSTICA")
        my_canvas.line(378, 723, 580, 723)
        my_canvas.drawString(30, 703, 'VARIABLES')
        my_canvas.line(120, 700, 580, 700)
        my_canvas.drawString(120, 703, "DATA, TEMPERATURA, HUMETAT, CO2, TVOC")


        my_canvas.drawString(30, 680, 'TEMPERATURA')
        my_canvas.drawString(30, 660, 'MITJA: ' + str(medT))
        my_canvas.drawString(30, 640, 'VARIABILITAT: ' + str(varT))
        my_canvas.drawString(30, 620, 'DESVIACIO TIPICA: ' + str(desT))
        
        my_canvas.drawString(30, 580, 'HUMETAT')
        my_canvas.drawString(30, 560, 'MITJA: ' + str(medH))
        my_canvas.drawString(30, 540, 'VARIABILITAT: ' + str(varH))
        my_canvas.drawString(30, 520, 'DESVIACIO TIPICA: ' + str(desH))

        my_canvas.drawString(30, 480, 'CO2')
        my_canvas.drawString(30, 460, 'MITJA: ' + str(medC))
        my_canvas.drawString(30, 440, 'VARIABILITAT: ' + str(varC))
        my_canvas.drawString(30, 420, 'DESVIACIO TIPICA: ' + str(desC))

        my_canvas.drawString(30, 380, 'TVOC')
        my_canvas.drawString(30, 360, 'MITJA: ' + str(medV))
        my_canvas.drawString(30, 340, 'VARIABILITAT: ' + str(varV))
        my_canvas.drawString(30, 320, 'DESVIACIO TIPICA: ' + str(desV))

        my_canvas.drawString(30, 280, '=== RELACIONS ===')

        my_canvas.drawString(30, 240, 'TEMPERATURA & HUMETAT')
        my_canvas.drawString(30, 220, 'COVARIABILITAT: ' + str(covTH))
        my_canvas.drawString(30, 200, 'PEARSON: ' + str(prsTH))
        my_canvas.drawString(30, 180, 'R QUADRAT: ' + str(rqtTH))

        my_canvas.drawString(30, 140, 'TEMPERATURA & CO2')
        my_canvas.drawString(30, 120, 'COVARIABILITAT: ' + str(covTC))
        my_canvas.drawString(30, 100, 'PEARSON: ' + str(prsTC))
        my_canvas.drawString(30, 80, 'R QUADRAT: ' + str(rqtTC))

        my_canvas.drawString(30, 40, 'CO2 & TVOC')
        my_canvas.drawString(30, 30, 'COVARIABILITAT: ' + str(covCV))
        my_canvas.drawString(30, 20, 'PEARSON: ' + str(prsCV))
        my_canvas.drawString(30, 10, 'R QUADRAT: ' + str(rqtCV))


        my_canvas.save()




        
        
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
