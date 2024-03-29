# DAS library revision 1
# Written by Andrew Kettle
# Last Revision: Sept 4th, 2020

import matplotlib


import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import sys 
import argparse
import mpld3 #allows for creation of interactive plot for web app


####### INPUT & FILTERING FUNCTIONS ########

def getargs():
    parser = argparse.ArgumentParser(description = "Data anaylsis script for the EV racecar program")
    parser.add_argument('--csv', dest="csvfile", action='store', help="CSV file name with .csv extension")
    parser.add_argument('--sensor', dest="sensor", action='store', help="Available options: all, accel, gyro, temp, or wheelspeed")
    parser.add_argument('--function', dest="function", action='store', help="Available options: raw, absmax, absmin, avg, relmax, relmin")
    parser.add_argument('--view', dest="view", action='store', help="Available options: standard") #maybe add items to this later

    if(len(sys.argv) < 9):
        print(len(sys.argv))
        print("Incorrect command line usage, the correct usage is on the line below\n")
        print("python3 das.py --csv <file> --sensor <SENSOR> --function <FUNCTION> --view <VIEW>\n")
        print("An example would be: python3 das.py --csv file --sensor accel --function raw --view standard")
        exit() #quits if the arguments are invalid
    else:
        args = parser.parse_args()
        return args

def getdf(filename, headernames):
    df = pd.read_csv(filename, names=headernames)
    return df
   
def filterSensor(df, sensor):
    if(sensor=='all'):
        return df #leaves df unchagned 
    elif(sensor=='accel'):
        return df[["Accel_X", "Accel_Y", "Accel_Z"]] #filters for accelerometer 
    elif(sensor=='gyro'):
        return df[["Gyro_X", "Gyro_Y", "Gyro_Z"]] #filters for gyro 
    elif(sensor=='temp'):
        return df[["IR_1", "IR_2", "IR_3"]] #filters for temp sensors
    elif(sensor=='wheelspeed'):
        return df[["Wheelspeed"]] #filters for wheelspeed 

####### END INPUT & FILTERING   ########

####### DATA ANALYSIS FUNCTIONS ########

def avg(df): 
    return df.mean()

def relmax(df):
    mx = pd.DataFrame() #empty dataframe
    pct = df.pct_change() #calulating percent change and storing in pct
    for col in df.columns: #iterates over pct to find relative max indecies
        max_data = (df[col]).index[((pct[col]) > 0) & ((pct[col]).shift(-1) < 0)].tolist() #finds relative maxima
        mx = pd.concat([mx, pd.Series(max_data).rename(col)], axis=1, sort=False) #appends to current dataframe
    return mx

def relmin(df):
    mn = pd.DataFrame() #empty dataframe
    pct = df.pct_change() #calulating percent change and storing in pct
    for col in df.columns: #iterates over pct to find relative max indecies
        max_data = (df[col]).index[((pct[col]) < 0) & ((pct[col]).shift(-1) > 0)].tolist() #finds relative minima
        mn = pd.concat([mn, pd.Series(max_data).rename(col)], axis=1, sort=False)
    return mn
    
def absExtremum(data, extype):
    if(extype=="min"):
        return data.min()
    elif(extype=="max"):
        return data.max()
    else:
        return -1

####### END DATA ANALYSIS #######

####### BEGIN VISUALIZATION FUCNTIONS #######

def plotGraph(df, units, cl = False, *args): #optional parameter expressed in args
    
    if (not cl):
        # only needs to be called when running the web appication version
        matplotlib.use('Agg') #prevents error "main thread is not in main loop"

    # Define some CSS to control our custom labels
    css = """
    text span
    {
    color: black;
    background-color: white; 
    }
    
    """
    fig, ax = plt.subplots()

    indecies = []           #default value
    if(args):               #an optional argument exists
        indecies = args[0]  #index for relmax, relmin, max, min

    
    
    if(not (type(indecies) == list)): #creating different plots based on the provided logic
        
        for col, ind in zip(df.columns, indecies):
            labels = []
            htmllabels = []

            plt.plot(df[col], label=col) 
            uplist = indecies[ind].dropna().astype('int32').tolist() #drops NANs and converts floats to ints to allow for indexing
            dots, = plt.plot(uplist, round(df[col][uplist], 3), marker='o', linestyle='None')

            labels = round(df[col][uplist], 3).T #create Series object of data

            labels = list(labels.to_frame().to_records()) #convert Series object into list of tuples
            
            #build list of HTML labels given list of tuples
            for val in labels:
                htmllabels.append("<text><span>{val}</span></text>".format(val=val))

            #create tooltip: text which hovers over points.
            tooltip = mpld3.plugins.PointHTMLTooltip(dots, htmllabels, hoffset = 10, css = css)
            mpld3.plugins.connect(fig, tooltip)

    else:
        for name in df.columns:
            plt.plot(df[name], label=name)

    
    plt.title("Time vs Output Graph")
    plt.xlabel("Samples")		
    plt.ylabel(units)
    plt.legend(loc="best")

    # Previously used for static image but replaced by dynamic graph
    # fig.savefig('./static/images/plot.png') # Embed the result in the html output.

    # convert matplot figure into dynamic html code using mpld3
    html_str = mpld3.fig_to_html(fig, figid="graph")
    html_file = open('./templates/plot.html', 'w')
    html_file.write(html_str)
    html_file.close()

    if (cl):
        plt.show() #no longer needed because of web application

    return fig
    

def get_avg(df):
    averages = []
    f_data = avg(df)
    for col, ind in zip(df.columns, f_data):
        averages.append((col,ind))
    return averages


def get_absmin(df):
    absmins = []
    f_data = absExtremum(df, "min")
    for col, ind in zip(df.columns, f_data):
        absmins.append((col,ind))
    return absmins

def get_absmax(df):
    absmaxes = []
    f_data = absExtremum(df, "max")
    for col, ind in zip(df.columns, f_data):
        absmaxes.append((col,ind))
    return absmaxes

####### END VISUALIZATION FUCNTIONS #######