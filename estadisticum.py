import mysql.connector
from mysql.connector import Error

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def media (vals):
    return sum(vals) / len(vals)

def var (vals,media):
    suma = 0
    for i in vals:
        suma = suma + pow(i - media,2)
    return suma / len(vals)


def regre (xlist,ylist):

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

    plt.savefig('regresio.png')
    plt.show()


    print("p")


def evol(idd,temp,co2,medT,medC):
    # create data
    x = np.array(idd)
    y = np.array(temp)
    y2 = np.array(co2)

    mT = np.full(len(y), medT, dtype=int)
    mC = np.full(len(y), medC, dtype=int)
      
    # plot lines
    plt.plot(x, y, label = "Temperatura")
    plt.plot(x, y2, label = "CO2")

    #Linies mitjanes
    plt.plot(x, mT, label = "Mitjana Temp")
    plt.plot(x, mC, label = "Mitjana CO2")
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



try:
    connection = mysql.connector.connect(host='192.168.3.10',
                                         database='juanreptem3',
                                         user='juan',
                                         password='juan')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("select DadesID,Temperatura,CO2 from Dades;")
        aux = cursor.fetchall()
        idd = []
        temp = []
        co2 = []
        vals = []
        for d in aux:
            idd.append(d["DadesID"])
            temp.append(d["Temperatura"])
            co2.append(d["CO2"])
        vals.append(idd)
        vals.append(temp)
        vals.append(co2)
        print(vals)
        print("Temperaturas: ", temp)
        print("CO2: ", co2)
        medT = media(temp)
        medC = media(co2)
        print("medias (temp,co2): (" + str(medT) + ", " + str(medC) + ")")
        print("varianza (temp,co2): (" + str(var(temp,medT)) + ", " + str(var(co2,medC)) + ")")
        regre(temp,co2)
        evol(idd,temp,co2,medT,medC)

        evol2(co2)
        
        
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


